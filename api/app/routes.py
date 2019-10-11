from app.models import StreamLog, User, NetflixSuggestMetadata, NetflixWatchMetadata
from flask import request, make_response
from app import app
from app import db
import sqlalchemy


@app.route("/<extension_id>/logs", methods=['GET'])
def list_logs_for_user(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    res = "#ip;content_id;date<br>"
    res += "<br>".join(["{};<a href='https://www.youtube.com/watch?v={}'>{}</a>;{}".format(p.ip, p.content_id,
                                                                                           p.content_id, p.timestamp)
                        for p in u.posts])
    return make_response(res, 200)


@app.route("/<extension_id>/netflix/logs", methods=['GET'])
def list_netflix_logs_for_user(extension_id):
    q = (db.session.query(User, StreamLog, NetflixSuggestMetadata)
         .filter(User.id == StreamLog.user_id)
         .filter(StreamLog.id == NetflixSuggestMetadata.streamlog_id)
         .filter(User.extension_id == extension_id))

    res = "#timestamp;ip;content_id;location;row;rank;app_view<br>"
    for x in q.all():
        res += "".join([("{};\t" * 7 + "<br>").format(x[1].timestamp, x[1].ip, x[1].content_id, x[2].location, x[2].row,
                                                      x[2].rank, x[2].appView)])

    return make_response(res, 200)


@app.route("/", methods=['GET'])
def list_users():
    out = "\n".join(
        ["<a href='" + u.extension_id + "/netflix/logs' > " + u.extension_id + "</a><br>" for u in db.session.query(User).all()])
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
    content_id = str(payload["video_id"])
    s = StreamLog(content_id=content_id, ip=request.remote_addr, user=u)
    db.session.add(s)

    db.session.commit()

    n = NetflixSuggestMetadata(list_id=payload.get("list_id", None), location=payload.get("location", None),
                               rank=payload.get("rank", None), request_id=payload.get("request_id", None),
                               row=payload.get("row", None), track_id=payload.get("track_id", None),
                               video_id=payload.get("video_id", None), image_key=payload.get("image_key", None),
                               supp_video_id=payload.get("supp_video_id", None), lolomo_id=payload.get("lolomo_id", None),
                               maturityMisMatchEdgy=payload.get("maturityMisMatchEdgy", None),
                               maturityMisMatchNonEdgy=payload.get("maturityMisMatchNonEdgy", None),
                               appView=payload.get("appView", None), usePresentedEvent=payload.get("usePresentedEvent", None),
                               json_object=payload.get("json_object", None),
                               streamlog_id=s.id)

    db.session.add(n)

    db.session.commit()
    return make_response("CREATED {} {}".format(s.content_id, u.extension_id), 201)


@app.route("/<extension_id>/netflix/watch/<track_id>", methods=['POST'])
def add_netflix_watch_log(extension_id, track_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)
    payload = request.get_json()

    n = NetflixWatchMetadata(track_id=track_id,
                             rank=payload.rank,
                             row=payload.row,
                             list_id=payload.list_id,
                             request_id=payload.request_id,
                             lolomo_id=payload.lolomo_id,
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
    qs = db.session.query(User, NetflixSuggestMetadata, StreamLog).filter(User.extension_id == extension_id).filter(
        User.id == StreamLog.user_id).filter(StreamLog.id == NetflixSuggestMetadata.streamlog_id).all()
    for q in qs:
        u, n, s = q
        db.session.delete(n)
        db.session.delete(s)
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
