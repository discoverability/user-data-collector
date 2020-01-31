from app.models import StreamLog, User, NetflixSuggestMetadata, NetflixWatchMetadata
from flask import request, make_response
from app import app
from app import db
import sqlalchemy


@app.route("/<extension_id>/netflix", methods=['GET'])
def list_netflix_for_user(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    res = "<a href='" + request.url + "/logs'>suggestions</a> or <a href='" + request.url + "/watches'>watches</a>"

    return make_response(res, 200)



@app.route("/<extension_id>/netflix/logs", methods=['GET'])
def list_netflix_logs_for_user(extension_id):
    q = (db.session.query(User, NetflixSuggestMetadata)
         .filter(User.id == NetflixSuggestMetadata.user_id)
         .filter(User.extension_id == extension_id))

    res = "#timestamp;ip;content_id;location;row;rank;app_view<br>"
    for _, suggest in q.all():
        res += "".join([("{};\t" * 8 + "<br>").format(suggest.timestamp, suggest.ip, suggest.video_id,suggest.track_id, suggest.location,
                                                      suggest.row, suggest.rank, suggest.appView)])

    return make_response(res, 200)


@app.route("/<extension_id>/netflix/watches", methods=['GET'])
def list_netflix_watches_for_user(extension_id):
    q = (db.session.query(User, NetflixWatchMetadata)
         .filter(User.id == StreamLog.user_id)
         .filter(User.extension_id == extension_id))

    res = "#timestamp;ip;video_id;track_id;rank;row;list_id;request_id;lolomo_id<br>"
    for (user, watch) in q.all():
        res += "%s;\t%s\t%s\t;%s;\t%s\t;%s\t;%s\t;%s\t;%s\t;<br>" % (
            watch.timestamp,watch.ip, str(watch.video_id), str(watch.track_id), str(watch.rank), str(watch.row), watch.list_id, watch.request_id, watch.lolomo_id)

    return make_response(res, 200)


@app.route("/", methods=['GET'])
def list_active_users():
    out = "\n".join(
        ["<a href='" + u.extension_id + "/netflix/logs' > " + u.extension_id +"("+str(len(u.suggestions))+" entries)"+ "</a><br>" for u in
         db.session.query(User).all() if len(u.suggestions)>0])
    return make_response(out, 200)

@app.route("/users", methods=['GET'])
def list_users():
    out = "\n".join(
        ["<a href='" + u.extension_id + "/netflix/logs' > " + u.extension_id +"("+str(len(u.suggestions))+" entries)"+ "</a><br>" for u in
         db.session.query(User).all() ])
    return make_response(out, 200)


@app.route("/<extension_id>", methods=['POST'])
def create_user(extension_id):
    u = User(extension_id=extension_id)
    db.session.add(u)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return make_response("This extension_id already exists", 409)

    return make_response("CREATED", 201)


@app.route("/<extension_id>/netflix", methods=['POST'])
def add_netflix_suggest_log(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)
    payload = request.get_json()

    n = NetflixSuggestMetadata(ip=request.remote_addr, user=u, list_id=payload.get("list_id", None),
                               location=payload.get("location", None),
                               rank=payload.get("rank", None), request_id=payload.get("request_id", None),
                               row=payload.get("row", None), track_id=payload.get("track_id", None),
                               video_id=payload.get("video_id", None), image_key=payload.get("image_key", None),
                               supp_video_id=payload.get("supp_video_id", None),
                               lolomo_id=payload.get("lolomo_id", None),
                               maturityMisMatchEdgy=payload.get("maturityMisMatchEdgy", None),
                               maturityMisMatchNonEdgy=payload.get("maturityMisMatchNonEdgy", None),
                               appView=payload.get("appView", None),
                               usePresentedEvent=payload.get("usePresentedEvent", None),
                               json_object=payload.get("json_object", None))

    db.session.add(n)

    db.session.commit()
    return make_response("CREATED {} {}".format(n.track_id, u.extension_id), 201)


@app.route("/<extension_id>/netflix/watch/<video_id>", methods=['POST'])
def add_netflix_watch_log(extension_id, video_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)
    payload = request.get_json()

    n = NetflixWatchMetadata(video_id=video_id,
                             track_id=payload.get("track_id"),
                             rank=payload.get("rank", None),
                             row=payload.get("row", None),
                             list_id=payload.get("list_id", None),
                             request_id=payload.get("request_id", None),
                             lolomo_id=payload.get("lolomo_id", None),
                             ip=request.remote_addr,
                             user=u)

    db.session.add(n)

    db.session.commit()
    return make_response("CREATED", 201)


@app.route("/<extension_id>", methods=['DELETE'])
def del_logs(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    db.session.delete(u)
    db.session.commit()
    return make_response("DELETED", 200)


@app.route("/<extension_id>/netflix/logs", methods=['DELETE'])
def del_netflix_logs(extension_id):
    qs = db.session.query(User, StreamLog) \
        .filter(User.extension_id == extension_id) \
        .filter(StreamLog.user_id == User.id) \
        .all()

    for user, log in qs:
        db.session.delete(log)
        db.session.commit()

    db.session.commit()
    return make_response("DELETED", 200)


@app.route("/", methods=['DELETE'])
def del_users():
    for u in db.session.query(User).all():
        db.session.delete(u)
    db.session.commit()
    return make_response("DELETED", 200)


@app.route("/<extension_id>/<content_id>", methods=['POST'])
def add_log_for_user(extension_id, content_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)
    s = StreamLog(content_id=content_id, ip=request.remote_addr, user=u)
    db.session.add(s)
    db.session.commit()
    return make_response("CREATED {} {}".format(s.content_id, u.extension_id), 201)
