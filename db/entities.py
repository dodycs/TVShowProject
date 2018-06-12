from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, UniqueConstraint

from db.base import Base, inverse_relationship, create_tables 

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    
    username = Column(String, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class TVShow(Base):
    __tablename__ = 'tvshow'
    id = Column(Integer, primary_key=True)
    api_url = Column(String, unique=True)
    api_id = Column(Integer, unique=True)

    name = Column(String)
    image = Column(String)

    def parse_json(self, data):
        self.api_url = data['_links']['self']['href']
        self.api_id = data['id']
        self.name = data['name']

        try:
            self.image = data['image']['original']
        except:
            self.image = 'http://via.placeholder.com/210x295'

class Like(Base):
    __tablename__ = 'tvshow_like'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=inverse_relationship('likes'))

    tvshow_id = Column(Integer, ForeignKey('tvshow.id'))
    tvshow = relationship(TVShow, backref=inverse_relationship('like_by'))

if __name__ != '__main__':
    create_tables()