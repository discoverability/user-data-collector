import datetime
from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    extension_id = db.Column(db.String(64), index=True, unique=True)

    suggestions = db.relationship(
        "NetflixSuggestMetadata", back_populates="user", cascade="all, delete-orphan"
    )

    watches = db.relationship(
        "NetflixWatchMetadata", back_populates="user", cascade="all, delete-orphan"
    )

    lolomos = db.relationship(
        "Lolomo", back_populates="user", cascade="all, delete-orphan"
    )

class Lolomo(db.Model):
    __tablename__ = "lolomo"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(54))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    rank = db.Column(db.Integer)
    type = db.Column(db.String(64))
    associated_content = db.Column(db.String(64))
    full_text_description= db.Column(db.String(512))
    single_page_session_id = db.Column(db.String(64),default="",server_default='')
    user = db.relationship("User", back_populates="lolomos", )

class StreamLog(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True)

    list_id = db.Column(db.String(512))
    track_id = db.Column(db.String(64))
    rank = db.Column(db.Integer)
    row = db.Column(db.Integer)
    request_id = db.Column(db.String(512))
    lolomo_id = db.Column(db.String(512))
    video_id = db.Column(db.Integer)

    ip = db.Column(db.String(54))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    type = db.Column(db.String(50))
    single_page_session_id = db.Column(db.String(64),default="",server_default='')

    __mapper_args__ = {
        "polymorphic_identity": "stream_log",
        "polymorphic_on": type,
    }


class NetflixSuggestMetadata(StreamLog):
    __tablename__ = "suggest"
    id = db.Column(db.ForeignKey("log.id"), primary_key=True)

    location = db.Column(db.String(512))
    image_key = db.Column(db.String(256))
    supp_video_id = db.Column(db.Integer)

    maturityMisMatchEdgy = db.Column(db.Boolean)
    maturityMisMatchNonEdgy = db.Column(db.Boolean)
    appView = db.Column(db.String(512))
    usePresentedEvent = db.Column(db.Boolean)
    json_object = db.Column(db.String(1024))
    user = db.relationship("User", back_populates="suggestions",)

    __mapper_args__ = {"polymorphic_identity": "suggest"}


class NetflixWatchMetadata(StreamLog):
    __tablename__ = "watch"
    id = db.Column(db.ForeignKey("log.id"), primary_key=True)

    user = db.relationship("User", back_populates="watches")

    __mapper_args__ = {"polymorphic_identity": "watch"}
