import os
import json
import struct, ctypes
from anonymizeip import anonymize_ip
from sqlalchemy import func
from flask import request, make_response, abort, redirect, url_for
from app.main import app as api, db, cache
from app.models import User, NetflixSuggestMetadata, NetflixWatchMetadata, Lolomo

from functools import wraps

is_callable = lambda o: hasattr(o, '__call__')


def query_args(*names, **values):
    user_args = ([{"key": name} for name in names] +
                 [{"key": key, "value": value}
                  for (key, value) in values.items()])

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            final_args, final_kwargs = args_from_request(user_args, args, kwargs)
            return f(*final_args, **final_kwargs)

        return wrapper

    return decorator if len(names) < 1 or not is_callable(names[0]) else decorator(names[0])


def args_from_request(to_extract, provided_args, provided_kwargs):
    # Ignoring provided_* here - ideally, you'd merge them
    # in whatever way makes the most sense for your application
    results = {}
    for arg in to_extract:

        extracted_value = request.args.get(arg["key"])
        try:
            if is_callable(arg["value"]):

                results[arg["key"]] = arg["value"](extracted_value)
            else:
                if extracted_value is None:
                    results[arg["key"]] = arg["value"]
                else:
                    results[arg["key"]] = type(arg["value"])(extracted_value)
        except ValueError:
            return abort(404, f" {arg['key']} argument should be {type(arg['value']).__name__}")
    return provided_args, results


API_ROOT = os.getenv("API_ROOT", "")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


@api.route("/", methods=['GET'])
def server_root():
    return redirect(API_ROOT+"/api")
# @api.route('/<path:path>')
# def hello(path):
#    return make_response("hello " +path+" "+ str(request.path))


@api.route("/api", methods=['GET'])
@cache.cached(timeout=3600)
def api_root():
    watch_link = {}
    watch_link["rel"] = "users"
    watch_link["href"] = API_ROOT + "/api/users"
    links = {"links": [watch_link, {"rel": "latest-watches",
                                    "href": API_ROOT + "/api/watches/latest"},
                       {"rel": "latest-thumbnails",
                        "href": API_ROOT + "/api/thumbnails/latest"},
                       {"rel": "latest-users",
                        "href": API_ROOT + "/api/users/latest"}
                       ]}
    return json.dumps(links, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/users/latest", methods=['GET'])
@query_args(limit=20)
def get_latest_users(limit):
    users = db.session.query(User).order_by(User.creation_date.desc()).limit(limit)

    res = {
        user.extension_id: {
            "id": user.extension_id,
            "creation_date": user.creation_date.timestamp(),
            "creation_date_human": str(user.creation_date),
            "log_count": len(user.suggestions),
            "watch_count": len(user.watches),
            "links": [
                {"rel": "self", "href": API_ROOT + f"/api/user/{user.extension_id}"},
                {"rel": "watches", "href": API_ROOT + f"/api/user/{user.extension_id}/watches"},
                {"rel": "sessions", "href": API_ROOT + f"/api/user/{user.extension_id}/sessions"},
                {"rel": "thumbnails", "href": API_ROOT + f"/api/user/{user.extension_id}/thumbnails"}
            ]}

        for user in users}
    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/thumbnails/latest", methods=['GET'])
@query_args(limit=20)
def get_latest_logs(limit):
    logs = db.session.query(NetflixSuggestMetadata).order_by(NetflixSuggestMetadata.timestamp.desc()).limit(limit)

    res = [
        {
            "user": log.user.extension_id,
            "pseudo_ip": anonymize_ip(log.ip),
            "timestamp": log.timestamp.timestamp(),
            "timestamp_human": str(log.timestamp),
            "video_id": log.video_id,
            "track_id": log.track_id,

            "links": [
                {"rel": "session",
                 "href": API_ROOT + f"/api/user/{log.user.extension_id}/session/{log.single_page_session_id}"},
                {"rel": "user", "href": API_ROOT + f"/api/user/{log.user.extension_id}"},
                {"rel": "content", "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{log.video_id}", }
            ]
        } for
        log in logs]
    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/watches/latest", methods=['GET'])
@query_args(limit=20)
def get_latest_watches(limit):
    watches = db.session.query(NetflixWatchMetadata).order_by(NetflixWatchMetadata.timestamp.desc()).limit(limit)

    res = [
        {"video_id": w.video_id,
         "timestamp": w.timestamp.timestamp(),
         "timestamp_human": str(w.timestamp),
         "track_id": w.track_id,
         "pseudo_ip": anonymize_ip(w.ip),
         "links": [

             {"rel": "session",
              "href": API_ROOT + f"/api/user/{w.user.extension_id}/session/{w.single_page_session_id}"},
             {"rel": "user", "href": API_ROOT + f"/api/user/{w.user.extension_id}"},
             {"rel": "content", "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{w.video_id}", }
         ]
         } for
        w in watches]
    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/users", methods=['GET'])
@cache.cached(timeout=3600)
def get_dataviz_users():
    users = db.session.query(User).all()
    res = []
    for u in users:
        user_data = get_user_data(u)
        user_data["sessions"] = []
        visited_sessions = []
        for suggestions in {l for l in u.suggestions}:
            l = suggestions.single_page_session_id
            if l not in visited_sessions:
                visited_sessions.append(l)
                session_data = {}
                session_data["session_id"] = l
                creation_date = [ll.timestamp for ll in u.lolomos if ll.single_page_session_id == l]
                if len(creation_date)==0:
                    continue #hot fix
                else:
                    creation_date=creation_date[0]

                session_data["creation_date"] = creation_date.timestamp()

                link_data = {}
                link_data["name"] = "thumbnails"
                link_data["href"] = API_ROOT + "/api/user/%s/thumbnails/%s" % (u.extension_id, l)

                watch_link = {}
                watch_link["name"] = "watches"
                watch_link["href"] = API_ROOT + "/api/user/%s/watches/%s" % (u.extension_id, l)
                session_data["links"] = [link_data, watch_link]
                user_data["sessions"].append(session_data)
        if len(user_data["sessions"]) > 0:
            res.append(user_data)

    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/session/<session_id>", methods=['GET'])
def get_session_for_user(user_id, session_id):
    res = {
        "links": get_sessions_links(user_id, session_id)
    }

    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/thumbnails/<session_id>", methods=['GET'])
@cache.cached(timeout=10)
def get_thumbnails_data(user_id, session_id):
    data = {}
    data["thumbnails"] = []

    suggests = (
        db.session.query(NetflixSuggestMetadata.row, NetflixSuggestMetadata.rank, NetflixSuggestMetadata.video_id,
                         func.max(NetflixSuggestMetadata.track_id), func.max(NetflixSuggestMetadata.timestamp),
                         func.max(NetflixSuggestMetadata.user_id)).join(User)
            .filter(User.id == NetflixSuggestMetadata.user_id)
            .filter(User.extension_id == user_id)
            .filter(NetflixWatchMetadata.single_page_session_id == session_id)
            .order_by(NetflixSuggestMetadata.row, NetflixSuggestMetadata.rank)
            .group_by(NetflixSuggestMetadata.row, NetflixSuggestMetadata.rank, NetflixSuggestMetadata.video_id)
            .all())

    for row, rank, video_id, track_id, timestamp, _ in suggests:
        item = {}

        item["row"] = row
        item["col"] = rank
        item["video_id"] = video_id
        item["track_id"] = track_id
        item["timestamp"] = timestamp.timestamp()
        item["timestamp_human"] = str(timestamp)
        item["links"] = [
            {"rel": "content", "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{video_id}"}]
        data["thumbnails"].append(item)
    data["links"] = get_user_links(user_id) + get_sessions_links(user_id, session_id)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/thumbnails", methods=['GET'])
@cache.cached(timeout=10)
def get_user_thumbnails(user_id):
    thumbnails = db.session.query(NetflixSuggestMetadata).join(User).filter(User.extension_id == user_id).filter(
        User.id == NetflixSuggestMetadata.user_id).all()

    t = {thumbnail.video_id: {
        "request_id": thumbnail.request_id,
        "timestamp": thumbnail.timestamp.timestamp(),
        "track_id": thumbnail.track_id,
        "links": get_sessions_links(user_id, thumbnail.single_page_session_id)} for thumbnail in thumbnails}
    return json.dumps(t), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/watches", methods=['GET'])
@cache.cached(timeout=10)
def get_user_watch(user_id):
    watches = db.session.query(NetflixWatchMetadata).join(User).filter(User.extension_id == user_id).filter(
        User.id == NetflixWatchMetadata.user_id).all()

    w = {}
    w["watches"] = [{
        "video_id": watch.video_id,
        "track_id": watch.track_id,
        "request_id": watch.request_id,
        "timestamp": watch.timestamp.timestamp(),
        "track_id": watch.track_id,
        "links": get_sessions_links(user_id, watch.single_page_session_id)} for watch in watches]

    w["links"] = get_user_links(user_id)

    return json.dumps(w), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/watches/<session_id>", methods=['GET'])
@cache.cached(timeout=10)
def get_user_watch_for_session(user_id, session_id):
    suggests = (db.session.query(User, NetflixSuggestMetadata).order_by(NetflixSuggestMetadata.timestamp)
                .filter(User.id == NetflixSuggestMetadata.user_id)
                .filter(User.extension_id == user_id)
                .filter(NetflixWatchMetadata.single_page_session_id == session_id)
                .order_by(NetflixSuggestMetadata.timestamp)
                .all())

    min_timestamp = suggests[0][1].timestamp
    max_timestamp = suggests[-1][1].timestamp

    suggests = (db.session.query(User, NetflixSuggestMetadata).order_by(NetflixSuggestMetadata.timestamp)
                .filter(User.id == NetflixSuggestMetadata.user_id)
                .filter(User.extension_id == user_id)
                .filter(NetflixSuggestMetadata.timestamp > max_timestamp)
                .order_by(NetflixSuggestMetadata.timestamp)
                .all())

    watches = db.session.query(User, NetflixWatchMetadata) \
        .filter(User.id == NetflixWatchMetadata.user_id) \
        .filter(User.extension_id == user_id) \
        .filter(NetflixWatchMetadata.timestamp >= min_timestamp)

    if len(suggests) > 0:
        next_timestamp = suggests[0][1].timestamp
        watches = watches.filter(NetflixWatchMetadata.timestamp < next_timestamp)

    watches = watches.all()

    data = get_watches_data(session_id, user_id, watches)

    return json.dumps(data), 200, {'Content-Type': 'application/json'}


def get_watches_data(session_id, user_id, watches):
    return {
        "watches": {watch.video_id: {"timestamp": watch.timestamp.timestamp(), "timestamp_human": str(watch.timestamp)}
                    for user, watch in watches},
        "links": [

            {
                "rel": "thumbnails",
                "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{session_id}"
            },
            {
                "rel": "user",
                "href": API_ROOT + f"/api/user/{user_id}"
            },
            {
                "rel": "self",
                "href": API_ROOT + f"/api/user/{user_id}/watches/{session_id}"
            },
            {
                "rel": "user_gui",
                "href": API_ROOT + "/" + "%s" % (user_id)
            },
            {
                "rel": "watches_gui",
                "href": API_ROOT + "/" + "%s/netflix/watches" % (user_id)
            }
        ]}


@api.route("/api/user/<user_id>", methods=['GET'])
@cache.cached(timeout=10)
def get_user(user_id):
    user = db.session.query(User).filter(User.extension_id == user_id).first()

    res = get_user_data(user)
    return json.dumps(res), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/sessions", methods=['GET'])
@cache.cached(timeout=10)
def get_sessions_for_user(user_id):
    lolomos = db.session.query(Lolomo.single_page_session_id, func.max(Lolomo.timestamp)).join(User).filter(
        User.id == Lolomo.user_id).filter(
        User.extension_id == user_id).group_by(Lolomo.single_page_session_id).all()

    res = {lolomo[0]: {"creation_date": lolomo[1].timestamp(),
                       "creation_date_human": str(lolomo[1]), "links": [
            {
                "rel": "thumbnails",
                "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{lolomo[0]}"
            },
            {
                "rel": "watches",
                "href": API_ROOT + f"/api/user/{user_id}/watches/{lolomo[0]}"
            }
        ]} for lolomo in lolomos}
    return json.dumps(res), 200, {'Content-Type': 'application/json'}


def get_user_data(user):
    return {"user": {"creation_date": user.creation_date.timestamp(), "creation_date_human": str(user.creation_date),
                     "user_id": user.extension_id}, "links": get_user_links(user.extension_id)}


def get_sessions_links(user_id, session_id):
    return [
        {
            "rel": "session",
            "href": API_ROOT + f"/api/user/{user_id}/session/{session_id}"
        }
        ,
        {
            "rel": "watches",
            "href": API_ROOT + f"/api/user/{user_id}/watches/{session_id}"
        }
        ,
        {
            "rel": "thumbnails",
            "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{session_id}"
        }

    ]


def get_user_links(user_id):
    return [

        {
            "rel": "all-sessions",
            "href": API_ROOT + f"/api/user/{user_id}/sessions"
        },
        {
            "rel": "self",
            "href": API_ROOT + f"/api/user/{user_id}"
        },
        {
            "rel": "all-watches",
            "href": API_ROOT + f"/api/user/{user_id}/watches"
        },
        {
            "rel": "all-thumbnails",
            "href": API_ROOT + f"/api/user/{user_id}/thumbnails"
        }
    ]
