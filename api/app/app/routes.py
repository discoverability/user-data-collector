
from app.models import StreamLog, User, NetflixSuggestMetadata, NetflixWatchMetadata, Lolomo, UserMetaData, AuthorizedIP
import json
from flask import request, make_response, render_template, abort
import logging
import sqlalchemy
from app.main import app, db
CONSENT_WATCHES = "consent-watches"
CONSENT_LOGS = "consent-logs"




def guard_ip(ip):
    #ip = db.session.query(AuthorizedIP).filter(AuthorizedIP.ip == ip).first()
    #if ip is None:
    #    abort(403, "Your IP is not authorized to use this feature. Contact Admin")
    pass


def guard_log_consent(u):
    for metadata in u.user_metadata:
        if metadata.key == CONSENT_LOGS:
            if metadata.value != "true":
                abort(400, "Can't save your data without your consent. Update your privacy configuration")
            else:
                return
    logging.warn("user " + u.extension_id + " tried to submit log without consent")
    abort(400, "Can't save your data without your consent. Update your privacy configuration")


def guard_watch_consent(u):
    for metadata in u.user_metadata:
        if metadata.key == CONSENT_WATCHES:
            if metadata.value != "true":
                abort(400, "Can't save your data without your consent. Update your privacy configuration")
            else:
                return
    logging.warn("user" + u.extension_id + " tried to submit watch without consent")
    abort(400, "Can't save your data without your consent. Update your privacy configuration")


def guard_user_consent(user):
    consent = db.session.query(UserMetaData).filter(UserMetaData.user_id == user.id).filter(
        UserMetaData.key == "consent-logs").first()
    if consent is not None and consent.value == "false":
        abort(200)


@app.route("/<extension_id>/privacy", methods=['GET'])
def privacy_form(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return abort(404, "not such user")

    return render_template('privacy.html', user=u)


@app.route("/<extension_id>/netflix", methods=['GET'])
def list_netflix_for_user(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    res = "<a href='" + request.url + "/logs'>suggestions</a> or <a href='" + request.url + "/watches'>watches</a>"

    return make_response(res, 200)


@app.route("/<extension_id>/netflix/logs", methods=['GET'])
def list_netflix_logs_for_user(extension_id):
    suggests = (db.session.query(User, NetflixSuggestMetadata).order_by(NetflixSuggestMetadata.timestamp)
                .filter(User.id == NetflixSuggestMetadata.user_id)
                .filter(User.extension_id == extension_id)
                .order_by(NetflixSuggestMetadata.timestamp, NetflixSuggestMetadata.row, NetflixSuggestMetadata.rank)
                .all())

    suggests = {"%s/%03d/%03d" % (s.timestamp.strftime("%m%d%H%M"), s.row, s.rank): s for _, s in suggests}

    # listings = [list(g) for  g in groupby(suggests, attrgetter('timestamp','row','rank'))]

    res = "<html><body>#timestamp;ip;content_id;location;row;rank;app_view<br>"
    for k_suggest in sorted(suggests):
        suggest = suggests[k_suggest]
        res += "".join([("{};\t" * 8 + "<a href='{}'>{}</a>;" + "<br>").format(suggest.timestamp,
                                                                               # suggest.ip,
                                                                               "unknown",
                                                                               suggest.video_id, suggest.track_id,
                                                                               suggest.location,
                                                                               suggest.row, suggest.rank,
                                                                               suggest.appView,
                                                                               "/" + extension_id + "/netflix/lolomos/" + suggest.single_page_session_id,
                                                                               suggest.single_page_session_id)])
    res += "</body></html>"

    return make_response(res, 200)


@app.route("/<extension_id>/netflix/lolomos", methods=['GET'])
def list_netflix_lolomo_for_user(extension_id):
    q = (db.session.query(User, Lolomo).order_by(Lolomo.timestamp)
         .filter(User.id == Lolomo.user_id)
         .filter(User.extension_id == extension_id)).order_by(Lolomo.timestamp, Lolomo.rank)

    lolomos = {"%s/%03d/%s" % (s.timestamp.strftime("%m%d%H%M"), s.rank, s.single_page_session_id): s for _, s in
               q.all()}

    # listings = [list(g) for  g in groupby(suggests, attrgetter('timestamp','row','rank'))]

    res = "#timestamp;ip;rank;type;associated_content;full_text_description;single_page_session_id<br>"
    for lolomo_k in sorted(lolomos):
        lolomo = lolomos[lolomo_k]

        res += "".join([("{};\t" * 7 + "<br>").format(lolomo.timestamp,
                                                      # lolomo.ip,
                                                      "unknown",
                                                      lolomo.rank,
                                                      lolomo.type,
                                                      lolomo.associated_content,
                                                      lolomo.full_text_description.encode('utf-8').strip(),
                                                      lolomo.single_page_session_id)

                        ])

    return make_response(res, 200)


@app.route("/<extension_id>/netflix/lolomos/latest", methods=['GET'])
def list_netflix_lolomo_latest_for_user(extension_id):
    lolo = db.session.query(User, Lolomo).order_by(Lolomo.timestamp.desc()).filter(User.id == Lolomo.user_id).filter(
        User.extension_id == extension_id).first()[1]

    q = db.session.query(Lolomo).filter(Lolomo.single_page_session_id == lolo.single_page_session_id).order_by(
        Lolomo.timestamp, Lolomo.rank)

    res = "#timestamp;ip;rank;type;associated_content;full_text_description;single_page_session_id<br>"
    for lolomo in q.all():
        res += "".join([("{};\t" * 7 + "<br>").format(lolomo.timestamp,
                                                      "unknown",
                                                      lolomo.rank,
                                                      lolomo.type,
                                                      lolomo.associated_content,
                                                      lolomo.full_text_description.encode('utf-8').strip(),
                                                      lolomo.single_page_session_id)

                        ])

    return make_response(res, 200)


@app.route("/<extension_id>/netflix/lolomos/<single_page_session_id>", methods=['GET'])
def list_netflix_lolomo_for_user_for_lolomo_id(extension_id, single_page_session_id):
    q = (db.session.query(User, Lolomo).order_by(Lolomo.timestamp)
         .filter(User.id == Lolomo.user_id)
         .filter(User.extension_id == extension_id)
         .filter(Lolomo.single_page_session_id == single_page_session_id)
         .order_by(Lolomo.timestamp, Lolomo.rank)
         )

    res = "#timestamp;ip;rank;type;associated_content;full_text_description;single_page_session_id<br>"
    for _, lolomo in q.all():
        res += "".join([("{};\t" * 6 + "<br>").format(lolomo.timestamp, "X.X.X.X",  # lolomo.ip,
                                                      lolomo.rank,
                                                      lolomo.type,
                                                      lolomo.associated_content,
                                                      lolomo.full_text_description.encode("utf-8").strip()
                                                      )

                        ])

    return make_response(res, 200)


@app.route("/<extension_id>/netflix/watches", methods=['GET'])
def list_netflix_watches_for_user(extension_id):
    q = (db.session.query(User, NetflixWatchMetadata)
         .filter(User.id == StreamLog.user_id)
         .filter(User.extension_id == extension_id))

    res = "#timestamp;ip;video_id;track_id;rank;row;list_id;request_id;lolomo_id<br>"
    for (user, watch) in q.all():
        res += "%s;\t%s\t%s\t;%s;\t%s\t;%s\t;%s\t;%s\t;%s\t;<br>" % (
            watch.timestamp,
            # watch.ip,
            "unknown",
            str(watch.video_id), str(watch.track_id), str(watch.rank), str(watch.row),
            watch.list_id, watch.request_id, watch.lolomo_id)

    return make_response(res, 200)


@app.route("/admin/users", methods=['GET'])
def list_active_users():
    guard_ip(request.remote_addr)
    q = db.session.query(User).order_by(User.creation_date.desc())
    q = q.limit(request.args.get("limit", 10))
    u = [u for u in q.all()]
    return render_template('users.html', users=u)




@app.route("/<extension_id>", methods=['GET'])
def get_user_data(extension_id):
    u = (db.session.query(User).filter(User.extension_id == extension_id).first())
    if u is None:
        return abort(404)
    else:
        return render_template('user.html', user=u)


@app.route("/<extension_id>", methods=['POST'])
def create_user(extension_id):
    u = User(extension_id=extension_id)
    db.session.add(u)

    consent_logs = UserMetaData(user=u, key=CONSENT_LOGS, value="true")
    consent_watches = UserMetaData(user=u, key=CONSENT_WATCHES, value="true")

    db.session.add(consent_logs)
    db.session.add(consent_watches)

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
    guard_log_consent(u)
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
                               json_object=payload.get("json_object", None),
                               single_page_session_id=payload.get("single_page_session_id", None))

    db.session.add(n)

    db.session.commit()
    return make_response("CREATED {} {}".format(n.track_id, u.extension_id), 201)


@app.route("/<extension_id>/netflix/lolomo", methods=['POST'])
def add_netflix_lolomo_log(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)

    guard_log_consent(u)
    payload = request.get_json()

    n = Lolomo(ip=request.remote_addr, user=u,
               rank=payload.get("rank", None),
               type=payload.get("type", None),
               associated_content=payload.get("associated_content", None),
               full_text_description=payload.get("full_text_description", None),
               single_page_session_id=payload.get("single_page_session_id", None)

               )

    db.session.add(n)

    db.session.commit()
    return make_response("CREATED", 201)


@app.route("/<extension_id>/netflix/watch/<video_id>", methods=['POST'])
def add_netflix_watch_log(extension_id, video_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)

    guard_watch_consent(u)
    payload = request.get_json()

    n = NetflixWatchMetadata(video_id=video_id,
                             track_id=payload.get("track_id"),
                             rank=payload.get("rank", None),
                             row=payload.get("row", None),
                             list_id=payload.get("list_id", None),
                             request_id=payload.get("request_id", None),
                             lolomo_id=payload.get("lolomo_id", None),
                             ip=request.remote_addr,
                             user=u,
                             single_page_session_id=payload.get("single_page_session_id", None))

    db.session.add(n)

    db.session.commit()
    return make_response("CREATED", 201)


@app.route("/<extension_id>", methods=['DELETE'])
def del_logs(extension_id):
    guard_ip(request.remote_addr)
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    db.session.delete(u)
    db.session.commit()
    return make_response("DELETED", 200)


@app.route("/<extension_id>/netflix/logs", methods=['DELETE'])
def del_netflix_logs(extension_id):
    guard_ip(request.remote_addr)
    qs = db.session.query(User, StreamLog) \
        .filter(User.extension_id == extension_id) \
        .filter(StreamLog.user_id == User.id) \
        .all()

    counter = 0
    for user, log in qs:
        counter += 1
        db.session.delete(log)

    db.session.commit()
    return make_response("DELETED %d entries" % counter, 200)


@app.route("/<extension_id>/netflix/lolomos", methods=['DELETE'])
def del_netflix_lolomos(extension_id):
    guard_ip(request.remote_addr)
    qs = db.session.query(User, Lolomo) \
        .filter(User.extension_id == extension_id) \
        .filter(Lolomo.user_id == User.id) \
        .all()

    counter = 0
    for user, lolomo in qs:
        db.session.delete(lolomo)
        counter += 1

    db.session.commit()
    return make_response("DELETED %d entries" % counter, 200)


@app.route("/", methods=['DELETE'])
def del_users():
    guard_ip(request.remote_addr)
    for u in db.session.query(User).all():
        db.session.delete(u)
    db.session.commit()
    return make_response("DELETED", 200)


@app.route("/<extension_id>/<content_id>", methods=['POST'])
def add_log_for_user(extension_id, content_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        logging.error("Unknown User " + extension_id + " tried to log data")
        return make_response("NO SUCH extension_id REGISTERED", 404)
    guard_log_consent(u)
    s = StreamLog(content_id=content_id, ip=request.remote_addr, user=u)
    db.session.add(s)
    db.session.commit()
    return make_response("CREATED {} {}".format(s.content_id, u.extension_id), 201)


@app.route("/<extension_id>/metadata", methods=["POST", "GET"])
def add_user_metadata(extension_id):
    u = db.session.query(User).filter_by(extension_id=extension_id).first()
    if u is None:
        return make_response("NO SUCH extension_id REGISTERED", 404)
    for key in request.args:
        already_present_meta = db.session.query(UserMetaData).filter_by(user_id=u.id).filter_by(key=key).first()
        if already_present_meta is not None:
            already_present_meta.value = request.args.get(key)
        else:
            m = UserMetaData(user=u, key=key, value=request.args.get(key))
            db.session.add(m)
    db.session.commit()
    return make_response("ADDED Metadata", 201)


@app.route("/set_robot", methods=["GET"])
def set_robot_plugin_hack():
    return make_response("robot", 200)


@app.route("/prune_empty_users", methods=["DELETE"])
def prune_empty_users():
    guard_ip(request.remote_addr)
    users = db.session.query(User).all()
    for u in users:
        if len(u.suggestions) == 0:
            db.session.delete(u)
    db.session.commit()
    return make_response("DELETED", 200)
