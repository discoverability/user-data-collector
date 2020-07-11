import os
import json
from sqlalchemy import func
from flask import request, make_response
from app.main import app as api, db, cache
from app.models import User, NetflixSuggestMetadata, NetflixWatchMetadata, Lolomo

API_ROOT = os.getenv("API_ROOT", "")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


# @api.route('/', defaults={'path': ''})
# @api.route('/<path:path>')
# def hello(path):
#    return make_response("hello " +path+" "+ str(request.path))


@api.route("/api", methods=['GET'])
@cache.cached(timeout=3600)
def api_root():
    watch_link = {}
    watch_link["name"] = "users"
    watch_link["href"] = API_ROOT + "/api/users"
    links = {"links": [watch_link]}
    return json.dumps(links, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


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
                creation_date = next((ll.timestamp for ll in u.lolomos if ll.single_page_session_id == l))
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


@api.route("/api/user/<user_id>/thumbnails/<session_id>", methods=['GET'])
@cache.cached(timeout=10)
def get_thumbnails_data(user_id, session_id):
    data = {}

    suggests = (db.session.query(NetflixSuggestMetadata).join(User).order_by(NetflixSuggestMetadata.timestamp)
                .filter(User.id == NetflixSuggestMetadata.user_id)
                .filter(User.extension_id == user_id)
                .filter(NetflixWatchMetadata.single_page_session_id == session_id)
                .order_by(NetflixSuggestMetadata.timestamp, NetflixSuggestMetadata.row, NetflixSuggestMetadata.rank)
                .all())

    suggests = {"%s/%03d/%03d" % (s.timestamp.strftime("%m%d%H%M"), s.row, s.rank): s for s in suggests}

    # listings = [list(g) for  g in groupby(suggests, attrgetter('timestamp','row','rank'))]

    res = "<html><body>#timestamp;ip;content_id;location;row;rank;app_view<br>"
    for k_suggest in sorted(suggests):
        suggest = suggests[k_suggest]
        item = {}

        item["row"] = suggest.row
        item["col"] = suggest.rank
        item["timestamp"] = suggest.timestamp.timestamp()
        item["timestamp_human"] = str(suggest.timestamp)
        data[suggest.video_id] = item
    data["links"] = get_user_links(user_id)
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
        "links": [

            {
                "name": "thumbnails",
                "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{thumbnail.single_page_session_id}"
            },
            {
                "name": "watches",
                "href": API_ROOT + f"/api/user/{user_id}/watches/{thumbnail.single_page_session_id}"
            }
        ]} for thumbnail in thumbnails}
    return json.dumps(t), 200, {'Content-Type': 'application/json'}


@api.route("/api/user/<user_id>/watches", methods=['GET'])
@cache.cached(timeout=10)
def get_user_watch(user_id):
    watches = db.session.query(NetflixWatchMetadata).join(User).filter(User.extension_id == user_id).filter(
        User.id == NetflixWatchMetadata.user_id).all()

    w = {watch.video_id: {
        "request_id": watch.request_id,
        "timestamp": watch.timestamp.timestamp(),
        "track_id": watch.track_id,
        "links": [

            {
                "name": "thumbnails",
                "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{watch.single_page_session_id}"
            },
            {
                "name": "watches",
                "href": API_ROOT + f"/api/user/{user_id}/watches/{watch.single_page_session_id}"
            }
        ]} for watch in watches}

    add_user_links(w, user_id)

    return json.dumps(w), 200, {'Content-Type': 'application/json'}


def add_user_links(w, user_id):
    w["links"] = [
        {
            "name": "user",
            "href": API_ROOT + f"/api/user/{user_id}"
        },
        {
            "name": "thumbnails",
            "href": API_ROOT + f"/api/user/{user_id}/thumbnails"
        },
        {
            "name": "self",
            "href": API_ROOT + f"/api/user/{user_id}/watches"
        }
    ]


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
                "name": "thumbnails",
                "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{session_id}"
            },
            {
                "name": "user",
                "href": API_ROOT + f"/api/user/{user_id}"
            },
            {
                "name": "self",
                "href": API_ROOT + f"/api/user/{user_id}/watches/{session_id}"
            },
            {
                "name": "user_gui",
                "href": API_ROOT + "/" + "%s" % (user_id)
            },
            {
                "name": "watches_gui",
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
def get_session_for_user(user_id):
    lolomos = db.session.query(Lolomo.single_page_session_id, func.max(Lolomo.timestamp)).join(User).filter(
        User.id == Lolomo.user_id).filter(
        User.extension_id == user_id).group_by(Lolomo.single_page_session_id).all()

    res = {lolomo[0]: {"creation_date": lolomo[1].timestamp(),
                       "creation_date_human": str(lolomo[1]), "links": [
            {
                "name": "thumbnails",
                "href": API_ROOT + f"/api/user/{user_id}/thumbnails/{lolomo[0]}"
            },
            {
                "name": "watches",
                "href": API_ROOT + f"/api/user/{user_id}/watches/{lolomo[0]}"
            }
        ]} for lolomo in lolomos}
    return json.dumps(res), 200, {'Content-Type': 'application/json'}


def get_user_data(user):
    return {"user": {"creation_date": user.creation_date.timestamp(), "creation_date_human": str(user.creation_date),
                     "user_id": user.extension_id}, "links": get_user_links(user.extension_id)}


def get_user_links(user_id):
    return [

        {
            "name": "sessions",
            "href": API_ROOT + f"/api/user/{user_id}/sessions"
        },
        {
            "name": "self",
            "href": API_ROOT + f"/api/user/{user_id}"
        },
        {
            "name": "watches",
            "href": API_ROOT + f"/api/user/{user_id}/watches"
        },
        {
            "name": "thumbnails",
            "href": API_ROOT + f"/api/user/{user_id}/thumbnails"
        }
    ]
