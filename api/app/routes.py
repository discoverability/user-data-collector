from app.models import StreamLog, User, NetflixMetadata, NetflixWatchMetadata
from flask import request, make_response
from app import app
from app import db
import sqlalchemy


@app.route("/<email>/logs", methods=['GET'])
def list_logs_for_user(email):
    u = db.session.query(User).filter_by(email=email).first()
    res = "#ip;content_id;date<br>"
    res += "<br>".join(["{};<a href='https://www.youtube.com/watch?v={}'>{}</a>;{}".format(p.ip, p.content_id,
                                                                                           p.content_id, p.timestamp)
                        for p in u.posts])
    return make_response(res, 200)


@app.route("/<email>/netflix/logs", methods=['GET'])
def list_netflix_logs_for_user(email):
    q = (db.session.query(User, StreamLog, NetflixMetadata)
         .filter(User.id == StreamLog.user_id)
         .filter(StreamLog.id == NetflixMetadata.streamlog_id)
         .filter(User.email == email))

    res = "#timestamp;ip;content_id;location;row;rank;app_view<br>"
    for x in q.all():
        res += "".join([("{};\t" * 7 + "<br>").format(x[1].timestamp, x[1].ip, x[1].content_id, x[2].location, x[2].row,
                                                      x[2].rank, x[2].appView)])

    return make_response(res, 200)


@app.route("/", methods=['GET'])
def list_users():
    out = "\n".join(
        ["<a href='" + u.email + "/netflix/logs' > " + u.email + "</a><br>" for u in db.session.query(User).all()])
    return make_response(out, 200)


@app.route("/<email>", methods=['POST'])
def create_user(email):
    u = User(email=email)
    db.session.add(u)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return make_response("This email already exists", 409)

    return make_response("CREATED", 201)


@app.route("/<email>/netflix", methods=['POST'])
def add_netflix_log(email):
    u = db.session.query(User).filter_by(email=email).first()
    if u is None:
        return make_response("NO SUCH EMAIL REGISTERED", 404)
    payload = request.get_json()
    content_id = str(payload["video_id"])
    s = StreamLog(content_id=content_id, ip=request.remote_addr, user=u)
    db.session.add(s)

    db.session.commit()

    n = NetflixMetadata(list_id=payload.get("list_id", None), location=payload.get("location", None),
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
    return make_response("CREATED {} {}".format(s.content_id, u.email), 201)


@app.route("/<email>/netflix/watch/<track_id>", methods=['POST'])
def add_netflix_log(email, track_id):
    u = db.session.query(User).filter_by(email=email).first()
    if u is None:
        return make_response("NO SUCH EMAIL REGISTERED", 404)
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


@app.route("/<email>", methods=['DELETE'])
def del_logs(email):
    u = db.session.query(User).filter_by(email=email).first()
    db.session.delete(u)
    db.session.commit()
    return make_response("DELETED", 200)


@app.route("/<email>/netflix/logs", methods=['DELETE'])
def del_netflix_logs(email):
    qs = db.session.query(User, NetflixMetadata, StreamLog).filter(User.email == email).filter(
        User.id == StreamLog.user_id).filter(StreamLog.id == NetflixMetadata.streamlog_id).all()
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


@app.route("/<email>/<content_id>", methods=['POST'])
def add_log_for_user(email, content_id):
    u = db.session.query(User).filter_by(email=email).first()
    if u is None:
        return make_response("NO SUCH EMAIL REGISTERED", 404)
    s = StreamLog(content_id=content_id, ip=request.remote_addr, user=u)
    db.session.add(s)
    db.session.commit()
    return make_response("CREATED {} {}".format(s.content_id, u.email), 201)
