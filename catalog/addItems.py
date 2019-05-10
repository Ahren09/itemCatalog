from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Kind, Item
engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()

kind1 = Kind(id=1, name="Cycling")
session.add(kind1)
session.commit()

kind2 = Kind(id=2, name="Swimming")
session.add(kind2)
session.commit()

item1 = Item(id=1, name="Helmet", description="The helmet that worths 1000$", kind=kind1)
session.add(item1)
session.commit()

item2 = Item(id=2, name="Goggles", description="A must for butterfly stroke", kind=kind2)
session.add(item2)
session.commit()

item3 = Item(id=3, name="Pedals", description="There are 2 catagories for pedals", kind=kind1)
session.add(item3)
session.commit()

item4 = Item(id=4, name="Trunks", description="Swimming shorts as you call it", kind=kind2)
session.add(item4)
session.commit()

print "Catalog Added!"
