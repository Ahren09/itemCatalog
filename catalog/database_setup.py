from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Kind(Base):
    __tablename__ = 'kind'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable = False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
    }

class Item(Base):
    __tablename__ = "Item"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    kind = relationship(Kind)
    kind_id = Column(Integer, ForeignKey('kind.id'))

    @property
    def serialize(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'kind' : self.kind,
        }

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.create_all(engine)
print "Database set!"