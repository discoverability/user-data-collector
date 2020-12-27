from app.main import db
import datetime
from sqlalchemy.sql import func


class AuthorizedIP(db.Model):
    __tablename__ = "authorized_ip"
    ip = db.Column(db.String(15), primary_key=True)


class DirectSchedule(db.Model):
    __tablename__ = "DIRECT_SCHEDULE"
    video_id = db.Column(db.Integer, primary_key=True)
    airing_time = db.Column(db.DateTime, primary_key=True)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    extension_id = db.Column(db.String(64), index=True, unique=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, server_default=None)

    suggestions = db.relationship(
        "NetflixSuggestMetadata", back_populates="user", cascade="all, delete-orphan"
    )

    watches = db.relationship(
        "NetflixWatchMetadata", back_populates="user", cascade="all, delete-orphan"
    )

    lolomos = db.relationship(
        "Lolomo", back_populates="user", cascade="all, delete-orphan"
    )

    user_metadata = db.relationship(
        "UserMetaData", back_populates="user", cascade="all, delete-orphan"
    )


class UserMetaData(db.Model):
    __tablename = "user_metadata"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    value = db.Column(db.String(64), index=True)
    key = db.Column(db.String(64), index=True)
    user = db.relationship("User", back_populates="user_metadata")


class Session(db.Model):
    __tablename__ = "session"
    single_page_session_id = db.Column(db.String(64), primary_key=True)

    lolomos = db.relationship(
        "Lolomo", back_populates="session", cascade="save-update"
    )

    thumbnails = db.relationship(
        "NetflixSuggestMetadata", back_populates="session", cascade="save-update"
    )

    watches = db.relationship(
        "NetflixWatchMetadata", back_populates="session", cascade="save-update"
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
    full_text_description = db.Column(db.String(512))
    single_page_session_id = db.Column(db.String(64), db.ForeignKey("session.single_page_session_id"), default="",
                                       server_default='')
    user = db.relationship("User", back_populates="lolomos", cascade="save-update")
    session = db.relationship("Session", back_populates="lolomos", cascade="save-update")


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
    single_page_session_id = db.Column(db.String(64), db.ForeignKey("session.single_page_session_id"), )

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
    user = db.relationship("User", back_populates="suggestions", )
    session = db.relationship("Session", back_populates="thumbnails", cascade="save-update")

    __mapper_args__ = {"polymorphic_identity": "suggest"}

    def __eq__(self, other):
        return self.row == other.row and self.rank == other.rank and self.video_id == other.video_id \
               and self.track_id == other.track_id and self.user_id == other.user_id

    def __hash__(self):
        return hash(('r', self.row, "rank", self.rank, "v", self.video_id, "t", self.track_id, "u", self.user_id))


class NetflixWatchMetadata(StreamLog):
    __tablename__ = "watch"
    id = db.Column(db.ForeignKey("log.id"), primary_key=True)

    user = db.relationship("User", back_populates="watches")
    session = db.relationship("Session", back_populates="watches", cascade="save-update")
    stop_time = db.Column(db.DateTime, default=None, nullable=True)
    __mapper_args__ = {"polymorphic_identity": "watch"}
