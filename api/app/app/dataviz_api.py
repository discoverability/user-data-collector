import json
from flask import request
from app.main import app as api, db, cache
from app.models import User, NetflixSuggestMetadata, NetflixWatchMetadata
from app.routes import SetEncoder


@api.route("/api/users", methods=['GET'])
@cache.cached(timeout=3600)
def get_dataviz_users():
    users = db.session.query(User).all()
    res = []
    for u in users:
        user_data = {}
        user_data["user_id"] = u.extension_id
        user_data["creation_date"] = u.creation_date.timestamp()
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
                link_data["href"] = "/dataviz-api/v1/thumbnails/%s/%s" % (u.extension_id, l)

                watch_link = {}
                watch_link["name"] = "watches"
                watch_link["href"] = "/dataviz-api/v1/thumbnails/%s/%s/watches" % (u.extension_id, l)
                session_data["links"] = [link_data, watch_link]
                user_data["sessions"].append(session_data)
        if len(user_data["sessions"]) > 0:
            res.append(user_data)

    return json.dumps(res, cls=SetEncoder), 200, {'Content-Type': 'application/json'}


@api.route("/api/thumbnails/<user_id>/<session_id>", methods=['GET'])
@cache.cached(timeout=3600)
def get_thumbnails_data(user_id, session_id):
    data = []

    suggests = (db.session.query(User, NetflixSuggestMetadata).order_by(NetflixSuggestMetadata.timestamp)
                .filter(User.id == NetflixSuggestMetadata.user_id)
                .filter(User.extension_id == user_id)
                .filter(NetflixWatchMetadata.single_page_session_id == session_id)
                .order_by(NetflixSuggestMetadata.timestamp, NetflixSuggestMetadata.row, NetflixSuggestMetadata.rank)
                .all())

    suggests = {"%s/%03d/%03d" % (s.timestamp.strftime("%m%d%H%M"), s.row, s.rank): s for _, s in suggests}

    # listings = [list(g) for  g in groupby(suggests, attrgetter('timestamp','row','rank'))]

    res = "<html><body>#timestamp;ip;content_id;location;row;rank;app_view<br>"
    for k_suggest in sorted(suggests):
        suggest = suggests[k_suggest]
        item = {}
        item["content_id"] = suggest.video_id
        item["row"] = suggest.row
        item["col"] = suggest.rank
        data.append(item)
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


@api.route("/api/thumbnails/<user_id>/<session_id>/watches", methods=['GET'])
@cache.cached(timeout=3600)
def get_user_watch_for_session(user_id, session_id):
    data = []

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

    data = {"watches": {watch.video_id: {"timestamp": watch.timestamp.timestamp()} for user, watch in watches},
            "links": [

                {
                    "name": "thumbnails",
                    "href":  "/dataviz-api/v1/thumbnails/%s/%s" % (user_id, session_id)
                },
                {
                    "name": "user",
                    "href": "/" + "%s" % (user_id)
                },
                {
                    "name": "all_watches",
                    "href": "/" + "%s/netflix/watches" % (user_id)
                }
            ]}

    return json.dumps(data), 200, {'Content-Type': 'application/json'}
