from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

fav_characters = Table(
    "fav_characters", db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

fav_vehicles = Table(
    "fav_vehicles", db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicle.id"), primary_key=True),
)

fav_planets = Table(
    "fav_planets", db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    lastname: Mapped[Optional[str]] = mapped_column(String(50))

    fav_characters: Mapped[List["Character"]] = relationship(secondary=fav_characters, back_populates="fav_by_users")
    fav_vehicles: Mapped[List["Vehicle"]] = relationship(secondary=fav_vehicles, back_populates="fav_by_users")
    fav_planets: Mapped[List["Planet"]] = relationship(secondary=fav_planets, back_populates="fav_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname,
            "fav_characters": [character.serialize() for character in self.fav_characters],
            "fav_vehicles": [vehicle.serialize() for vehicle in self.fav_vehicles],
            "fav_planets": [planet.serialize() for planet in self.fav_planets]
        }

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(120))
    attributes: Mapped[Optional[dict]] = mapped_column(JSONB)

    fav_by_users: Mapped[List[User]] = relationship(secondary=fav_characters, back_populates="fav_characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "attributes": self.attributes
        }

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(120))
    attributes: Mapped[Optional[dict]] = mapped_column(JSONB)

    fav_by_users: Mapped[List[User]] = relationship(secondary=fav_vehicles, back_populates="fav_vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "attributes": self.attributes
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(120))
    attributes: Mapped[Optional[dict]] = mapped_column(JSONB)

    fav_by_users: Mapped[List[User]] = relationship(secondary=fav_planets, back_populates="fav_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "attributes": self.attributes
        }