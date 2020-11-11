import os
import json
from datetime import datetime, timedelta
import dateparser
from anonymizeip import anonymize_ip
from sqlalchemy import func
from flask import request, abort, redirect
from app.main import app as api, db, cache
from app.models import User, NetflixSuggestMetadata, NetflixWatchMetadata, Lolomo

from functools import wraps

from app.set_encoder import SetEncoder

is_callable = lambda o: hasattr(o, '__call__')


def get_api_root():
    return os.getenv("API_ROOT", "dummy://")


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


@api.route("/", methods=['GET'])
def server_root():
    return redirect(get_api_root() + "api")


# @api.route('/<path:path>')
# def hello(path):
#    return make_response("hello " +path+" "+ str(request.path))


@api.route("/api", methods=['GET'])
@cache.cached(timeout=3600)
def api_root():
    watch_link = {}
    watch_link["rel"] = "users"
    watch_link["href"] = get_api_root() + "api/users"
    links = {"links": [watch_link, {"rel": "latest-watches",
                                    "href": get_api_root() + "api/watches/latest",
                                    "doc": "You can use date_from and date_to query params to specify range. Defaults to from=last week to=today",
                                    "examples": [
                                        get_api_root() + "api/watches/latest?date_from=2020-10-01&date_to=2020-11-01",
                                        get_api_root() + "api/watches/latest?date_from=last+week&date_to=today"]},
                       {"rel": "latest-thumbnails",
                        "href": get_api_root() + "api/thumbnails/latest",
                        "doc": "You can use date_from and date_to query params to specify range: Defaults to from=last week to=today",
                        "examples": [get_api_root() + "api/thumbnails/latest?date_from=2020-10-01&date_to=2020-11-01",
                                     get_api_root() + "api/thumbnails/latest?date_from=last+week&date_to=today"]},

                       {"rel": "latest-users",
                        "href": get_api_root() + "api/users/latest"},
                       {"rel": "custom",
                        "href": get_api_root() + "api/custom"},
                       {"rel": "stats",
                        "href": get_api_root() + "api/stats"}
                       ]}
    return json.dumps(links, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/users/latest", methods=['GET'])
@query_args(limit=20)
@cache.memoize(timeout=3600)
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
                {"rel": "self", "href": get_api_root() + f"api/user/{user.extension_id}"},
                {"rel": "watches", "href": get_api_root() + f"api/user/{user.extension_id}/watches"},
                {"rel": "sessions", "href": get_api_root() + f"api/user/{user.extension_id}/sessions"},
                {"rel": "thumbnails", "href": get_api_root() + f"api/user/{user.extension_id}/thumbnails"}
            ]}

        for user in users}
    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/thumbnails/latest", methods=['GET'])
@query_args(limit=9999, date_from="last week", date_to="now")
@cache.memoize(timeout=3600)
def get_latest_logs(limit, date_from, date_to):
    from_date = dateparser.parse(date_from)
    to_date = dateparser.parse(date_to)
    logs = db.session.query(NetflixSuggestMetadata).filter(NetflixSuggestMetadata.timestamp >= from_date) \
        .filter(NetflixSuggestMetadata.timestamp <= to_date) \
        .order_by(
        NetflixSuggestMetadata.timestamp.desc())
    if limit != -1:
        logs = logs.limit(limit)

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
                 "href": get_api_root() + f"api/user/{log.user.extension_id}/session/{log.single_page_session_id}"},
                {"rel": "user", "href": get_api_root() + f"api/user/{log.user.extension_id}"},
                {"rel": "content",
                 "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{log.video_id}", }
            ]
        } for
        log in logs]
    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/watches/latest", methods=['GET'])
@query_args(limit=9999, date_from="last week", date_to="now")
@cache.memoize(timeout=3600)
def get_latest_watches(limit, date_from, date_to):
    from_date = dateparser.parse(date_from)
    to_date = dateparser.parse(date_to)

    watches = db.session.query(NetflixWatchMetadata) \
        .filter(NetflixWatchMetadata.timestamp >= from_date) \
        .filter(NetflixWatchMetadata.timestamp <= to_date) \
        .order_by(NetflixWatchMetadata.timestamp.desc())

    if limit != -1:
        watches = watches.limit(limit)

    res = [
        {"video_id": w.video_id,
         "timestamp": w.timestamp.timestamp(),
         "timestamp_human": str(w.timestamp),
         "track_id": w.track_id,
         "pseudo_ip": anonymize_ip(w.ip),

         "links": [

             {"rel": "session",
              "href": get_api_root() + f"api/user/{w.user.extension_id}/session/{w.single_page_session_id}"},
             {"rel": "user", "href": get_api_root() + f"api/user/{w.user.extension_id}"},
             {"rel": "content",
              "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{w.video_id}", }
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
                if len(creation_date) == 0:
                    continue  # hot fix
                else:
                    creation_date = creation_date[0]

                session_data["creation_date"] = creation_date.timestamp()

                link_data = {}
                link_data["name"] = "thumbnails"
                link_data["href"] = get_api_root() + "api/user/%s/session/%s/thumbnails" % (u.extension_id, l)

                session_link = {}
                session_link["name"] = "session"
                session_link["href"] = get_api_root() + "api/user/%s/session/%s" % (u.extension_id, l)

                watch_link = {}
                watch_link["name"] = "watches"
                watch_link["href"] = get_api_root() + "api/user/%s/session/%s/watches" % (u.extension_id, l)

                lolomo_link = {}
                lolomo_link["name"] = "lolomos"
                lolomo_link["href"] = get_api_root() + "api/user/%s/session/%s/lolomos" % (u.extension_id, l)

                session_data["links"] = [link_data, watch_link, lolomo_link, session_link]
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


@api.route("/api/user/<user_id>/session/<session_id>/thumbnails", methods=['GET'])
@cache.cached(timeout=10)
def get_thumbnails_data(user_id, session_id):
    data = {}

    suggests = (
        db.session.query(NetflixSuggestMetadata).join(User)
            .filter(User.id == NetflixSuggestMetadata.user_id)
            .filter(User.extension_id == user_id)
            .filter(NetflixWatchMetadata.single_page_session_id == session_id)
            .all())

    data["thumbnails"] = extract_thumbnails_data(suggests)
    data["links"] = get_user_links(user_id) + get_sessions_links(user_id, session_id)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/lolomo/<lolomo_id>", methods=['GET'])
@cache.cached(timeout=10)
def get_thumnails_for_lolomo(user_id, lolomo_id):
    data = {}

    suggests = (
        db.session.query(NetflixSuggestMetadata).join(User).join(Lolomo)
            .filter(User.id == NetflixSuggestMetadata.user_id)
            .filter(User.extension_id == user_id)
            .filter(Lolomo.id == lolomo_id)
            .filter(NetflixWatchMetadata.row == Lolomo.rank)

            .all())

    data["lolomo_info"] = extract_lolomo_data([db.session.query(Lolomo).get(lolomo_id)])[0]
    data["thumbnails"] = extract_thumbnails_data(sorted(set(suggests), key=lambda x: x.rank), include_lolomo=False)
    data["links"] = get_user_links(user_id)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


def extract_lolomo_data(lolomos):
    lolomo_data = []

    for l in lolomos:
        lolomo_data.append({"rank": l.rank, "associated_content": l.associated_content, "type": l.type,
                            "full_text_description": l.full_text_description, "timestamp": l.timestamp.timestamp(),
                            "timestamp_human": str(l.timestamp), "links": {"rel": "thumbnails-for-lolomo",
                                                                           "href": get_api_root() + f"api/user/{l.user.extension_id}/lolomo/{l.id}"

                                                                           }})

    return lolomo_data


@api.route("/api/user/<user_id>/session/<session_id>/lolomos", methods=['GET'])
@cache.cached(timeout=10)
def get_lolomo_data(user_id, session_id):
    data = {}

    lolomos = (
        db.session.query(Lolomo).join(User)
            .filter(User.id == Lolomo.user_id)
            .filter(Lolomo.single_page_session_id == session_id)
            .order_by(Lolomo.rank)
            .all())

    data["lolomos"] = extract_lolomo_data(lolomos)
    data["links"] = get_user_links(user_id) + get_sessions_links(user_id, session_id)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


def extract_thumbnails_data(suggests, include_lolomo=True):
    thumbnails_data = []
    for log in suggests:
        row = log.row
        rank = log.rank
        video_id = log.video_id
        track_id = log.track_id
        timestamp = log.timestamp

        item = {"row": row, "col": rank, "video_id": video_id, "track_id": track_id, "timestamp": timestamp.timestamp(),
                "timestamp_human": str(timestamp), "links": [
                {"rel": "content",
                 "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{video_id}"}]}
        if include_lolomo:
            lolomo_info = [
                {"type": l.type, "content": l.associated_content, "desc": l.full_text_description, "row": l.rank}
                for l in
                log.session.lolomos if l.rank == row]
            if len(lolomo_info) > 0:
                lolomo_info = lolomo_info[0]
            else:
                lolomo_info = ""
            item["lolomo_info"] = lolomo_info

        thumbnails_data.append(item)
    return thumbnails_data


@api.route("/api/user/<user_id>/thumbnails", methods=['GET'])
@cache.cached(timeout=10)
def get_user_thumbnails(user_id):
    data = {}

    suggests = (
        db.session.query(NetflixSuggestMetadata).join(User)
            .filter(User.id == NetflixSuggestMetadata.user_id)
            .filter(User.extension_id == user_id)
            .all())

    data["thumbnails"] = extract_thumbnails_data(suggests)
    data["links"] = get_user_links(user_id)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/lolomos", methods=['GET'])
@cache.cached(timeout=10)
def get_user_lolomos(user_id):
    data = {}
    data["lolomos"] = []
    lolomos = (
        db.session.query(Lolomo).join(User)
            .filter(User.id == Lolomo.user_id)
            .order_by(Lolomo.timestamp.desc())
            .all())

    data["lolomos"] = extract_lolomo_data(lolomos)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


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
        "row": watch.row,
        "rank": watch.rank,
        "lolomo_info": [
            {"type": l.type, "content": l.associated_content, "desc": l.full_text_description, "row": l.rank}
            for l in
            watch.session.lolomos if l.rank == watch.row],
        "links": get_sessions_links(user_id, watch.single_page_session_id)} for watch in watches]

    w["links"] = get_user_links(user_id)

    return json.dumps(w), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/session/<session_id>/watches", methods=['GET'])
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
        "watches": {watch.video_id: {"timestamp": watch.timestamp.timestamp(), "timestamp_human": str(watch.timestamp),
                                     "row": watch.row, "rank": watch.rank}
                    for user, watch in watches},
        "links": [

            {
                "rel": "thumbnails",
                "href": get_api_root() + f"api/user/{user_id}/session/{session_id}/thumbnails"
            },
            {
                "rel": "user",
                "href": get_api_root() + f"api/user/{user_id}"
            },
            {
                "rel": "self",
                "href": get_api_root() + f"api/user/{user_id}/session/{session_id}/watches"
            },
            {
                "rel": "lolomos",
                "href": get_api_root() + f"api/user/{user_id}/session/{session_id}/lolomos"
            },
            {
                "rel": "user_gui",
                "href": get_api_root() + "%s" % (user_id)
            },
            {
                "rel": "watches_gui",
                "href": get_api_root() + "%s/netflix/watches" % (user_id)
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

    res = [{lolomo[0]: {"creation_date": lolomo[1].timestamp(),
                       "creation_date_human": str(lolomo[1]), "links": [
            {
                "rel": "thumbnails",
                "href": get_api_root() + f"api/user/{user_id}/session/{lolomo[0]}/thumbnails"
            },
            {
                "rel": "watches",
                "href": get_api_root() + f"api/user/{user_id}/session/{lolomo[0]}/watches"
            },
            {
                "rel": "lolomos",
                "href": get_api_root() + f"api/user/{user_id}/session/{lolomo[0]}/lolomos"
            }
        ]}} for lolomo in lolomos]

    res = sorted(res, key=lambda x: -list(x.items())[0][1]["creation_date"])
    return json.dumps(res), 200, {'Content-Type': 'application/json'}


def get_user_data(user):
    return {"user": {"creation_date": user.creation_date.timestamp(), "creation_date_human": str(user.creation_date),
                     "user_id": user.extension_id}, "links": get_user_links(user.extension_id)}


def get_sessions_links(user_id, session_id):
    return [
        {
            "rel": "session",
            "href": get_api_root() + f"api/user/{user_id}/session/{session_id}"
        }
        ,
        {
            "rel": "watches",
            "href": get_api_root() + f"api/user/{user_id}/session/{session_id}/watches"
        }
        ,
        {
            "rel": "thumbnails",
            "href": get_api_root() + f"api/user/{user_id}/session/{session_id}/thumbnails"
        },
        {
            "rel": "lolomos",
            "href": get_api_root() + f"api/user/{user_id}/session/{session_id}/lolomos"
        }

    ]


def get_session_and_content_link(user_id, session_id, video_id):
    res = get_sessions_links(user_id, session_id)
    res.append({
        "rel": "content",
        "href": f"https://platform-api.vod-prime.space/api/emns/provider/4/identifier/{video_id}"
    })
    return res


def get_user_links(user_id):
    return [

        {
            "rel": "all-sessions",
            "href": get_api_root() + f"api/user/{user_id}/sessions"
        },
        {
            "rel": "self",
            "href": get_api_root() + f"api/user/{user_id}"
        },
        {
            "rel": "all-watches",
            "href": get_api_root() + f"api/user/{user_id}/watches"
        },
        {
            "rel": "all-thumbnails",
            "href": get_api_root() + f"api/user/{user_id}/thumbnails"
        },
        {
            "rel": "all-lolomos",
            "href": get_api_root() + f"api/user/{user_id}/lolomos"
        }

    ]


@api.route("/api/stats")
def get_stats():
    return {"rel": "stats-dataviz", f"href": f"{get_api_root() + 'api/stats/dataviz'}"}


@api.route("/api/stats/dataviz")
@query_args(delta=7)
def get_stats_dataviz(delta):
    some_days_ago = datetime.utcnow() - timedelta(days=delta)
    weekly_new_users = db.session.query(User.id).join(NetflixSuggestMetadata).filter(
        User.creation_date > some_days_ago).filter(
        NetflixSuggestMetadata.timestamp > some_days_ago).group_by(User.id).having(
        func.count(NetflixSuggestMetadata.id) >= 1).all()

    weekly_new_watches = db.session.query(NetflixWatchMetadata.id).order_by(
        NetflixWatchMetadata.timestamp.desc()).filter(
        NetflixWatchMetadata.timestamp > some_days_ago).all()
    weekly_new_thumbnails = db.session.query(NetflixSuggestMetadata.id).order_by(
        NetflixSuggestMetadata.timestamp.desc()).filter(
        NetflixSuggestMetadata.timestamp > some_days_ago).all()
    active_users = db.session.query(User.id).join(NetflixSuggestMetadata).filter(
        NetflixSuggestMetadata.timestamp > some_days_ago).group_by(User.id).having(
        func.count(NetflixSuggestMetadata.id) >= 1).all()

    res = {"time_delta_days": delta, "new_users": len(weekly_new_users),
           "new_watches": len(weekly_new_watches),
           "new_thumbnails": len(weekly_new_thumbnails),
           "active_users": len(active_users),
           "avg_thumbnails_per_active_user": len(weekly_new_thumbnails) / len(active_users),
           "avg_watches_per_active_user": len(weekly_new_watches) / len(active_users)}
    return res
