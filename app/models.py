from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class Plants(db.Model):
    __tablename__ = "plants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    species = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    lighting = db.Column(db.String(64))
    foto = db.Column(db.String(128), unique=True)

    plants_users = db.relationship(
        "UsersPlants", backref="plant_users", lazy=True
    )

    plant_comments = db.relationship(
        "Comments", back_populates="comm_plant", lazy=True
    )


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Связь с Comments (обновляем с back_populates)
    user_comments = db.relationship(
        "Comments", back_populates="author", lazy=True
    )

    # Связь с UsersPlants
    users_plants = db.relationship(
        "UsersPlants", backref="user_plants", lazy=True
    )


class UsersPlants(db.Model):
    __table_args__ = (db.UniqueConstraint("user_id", "plant_id"),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    plant_id = db.Column(
        "plant_id",
        db.Integer,
        db.ForeignKey("plants.id", ondelete="CASCADE"),
        nullable=False,
    )


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    plant_id = db.Column(
        "plant_id",
        db.Integer,
        db.ForeignKey("plants.id", ondelete="CASCADE"),
        nullable=False,
    )
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())

    # Обновляем двустороннюю связь с Users и Plants
    author = db.relationship(
        "Users", foreign_keys=[user_id], back_populates="user_comments"
    )
    comm_plant = db.relationship(
        "Plants", foreign_keys=[plant_id], back_populates="plant_comments"
    )

    @classmethod
    def get_sorted_comments(cls):
        # Вернет комментарии, отсортированные по timestamp по убыванию
        return cls.query.order_by(cls.timestamp.desc())


class Chats(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    users = db.Column(db.String(32), unique=True, nullable=False)


class PrivateMessage(db.Model):
    __tablename__ = "private_messages"

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    recipient_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    is_readed = db.Column(db.Boolean, default=False)

    sender = db.relationship("Users", foreign_keys=[sender_id])
    recipient = db.relationship("Users", foreign_keys=[recipient_id])

    def __init__(self, chat_id, sender_id, recipient_id, message, timestamp):
        self.chat_id = chat_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message = message
        self.timestamp = timestamp
