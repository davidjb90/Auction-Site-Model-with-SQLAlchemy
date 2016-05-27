from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    item_bid = relationship("Bid", backref="item_bid")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    bid = relationship("Bid", backref="bidder")
    item = relationship("Item", backref="auctioner")
    
class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    bidder_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

Base.metadata.create_all(engine)

david = User(username="david1", password="password1")
john = User(username="john1", password="password2")
donald = User(username="donald1", password="password3")

session.add_all([david, john, donald])
session.commit()

#auctioned baseball
baseball = Item(name="Home Run Ball", description="World Series Winning Home Run Baseball", auctioner=david)

session.add(baseball)
session.commit()

bid1 = Bid(price=10000, bidder=john, item_bid=baseball)
bid2 = Bid(price=12000, bidder=donald, item_bid=baseball)

session.add_all([bid1, bid2])
session.commit()

print(session.query(User.id, User.username, User.password).all())
print(session.query(Item.id, Item.name, Item.user_id).all())
print(session.query(Bid.price, Bid.bidder_id).first())

#gives the highest bid and the user id # associated with the bid
print(max(session.query(Bid.price, Bid.bidder_id).all()))
    
    