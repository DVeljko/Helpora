from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import  UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer , primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    campaigns: Mapped[list["Campaign"]] = relationship('Campaign',backref='user' , lazy=True)
    donations: Mapped[list["Donation"]] = relationship('Donation', backref='donator', lazy=True)


class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    goal_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    donations: Mapped[list["Donation"]] = relationship('Donation', backref='campaign', lazy=True)

class Donation(db.Model):
    __tablename__ = 'donations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    donated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    donator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    campaign_id: Mapped[int] = mapped_column(ForeignKey('campaigns.id'))
