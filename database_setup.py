from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'user-email': self.email,
            'user-id': self.id
        }


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    hours = Column(String(60))
    phone_number = Column(String(20))
    image = Column(String(100))
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'shop-name': self.name,
            'shop-image': self.image,
            'id': self.id,
            'shop-hours': self.hours,
            'shop-phone_number': self.phone_number,
            'owner_id': self.owner_id
        }


class Product(Base):
    __tablename__ = 'product'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    image = Column(String(100))
    shop_id = Column(Integer, ForeignKey('shop.id'))
    soldIn = relationship(Shop)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'product-name': self.name,
            'product-image': self.image,
            'id': self.id,
            'product-description': self.description,
            'product-price': self.price,
            'shop_id': self.shop_id
        }


engine = create_engine('sqlite:///shopData.db')


Base.metadata.create_all(engine)
