import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship('StreamLog', backref='user', lazy='dynamic')


class StreamLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<StreamLog {}.{}>'.format(self.user_id, self.content_id)


class NetflixMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.String(64))
    location = db.Column(db.String(64))
    rank = db.Column(db.Integer)
    request_id=db.Column(db.String(64))
    row = db.Column(db.Integer)
    track_id=db.Column(db.String(64))
    video_id=db.Column(db.Integer)
    image_key=db.Column(db.String(64))
    supp_video_id=db.Column(db.Integer)
    lolomo_id=db.Column(db.String(64))
    maturityMisMatchEdgy=db.Column(db.Boolean)
    maturityMisMatchNonEdgy=db.Column(db.Boolean)
    appView=db.Column(db.String(64))
    usePresentedEvent=db.Column(db.Boolean)
    json_object = db.Column(db.String(64))
    streamlog_id = db.Column(db.Integer, db.ForeignKey("stream_log.id"))


class NetflixWatchMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.String(64))
    list_id = db.Column(db.String(64))
    rank = db.Column(db.Integer)
    request_id = db.Column(db.String(64))
    row = db.Column(db.Integer)
    lolomo_id = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
