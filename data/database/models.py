from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from sqlite_base import Base


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    address = Column(String(50), nullable=False)

    reviews = relationship("Review", back_populates="restaurant")


class Review(Base):
    __tablename__ = "review"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    context = Column(Text, nullable=False)

    restaurant = relationship("Restaurant", back_populates="reviews")