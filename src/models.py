from sqlalchemy import Column, Integer, SmallInteger, Sequence
from sqlalchemy.types import DECIMAL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sectors.db', echo=True)

Base = declarative_base()


class Sector(Base):
	__tablename__ = 'sectors'

	id = Column(Integer, Sequence('sector_id_seq'), primary_key=True)

	mcc = Column(SmallInteger)
	mnc = Column(SmallInteger)

	node_id = Column(Integer)
	sector_id = Column(SmallInteger)
	pci = Column(SmallInteger)

	lat = Column(DECIMAL(8, 6))
	lng = Column(DECIMAL(9, 6))

	samples = Column(Integer)
	created = Column(Integer)
	updated = Column(Integer)

	def __repr__(self):
		return "<Sectors(id='%s', enb='%s', sector='%s')>" % (self.id, self.node_id, self.sector_id)


class Node(Base):
	__tablename__ = 'nodes'

	id = Column(Integer, Sequence('node_id_seq'), primary_key=True)

	mcc = Column(SmallInteger)
	mnc = Column(SmallInteger)

	node_id = Column(Integer)

	lat = Column(DECIMAL(8, 6))
	lng = Column(DECIMAL(9, 6))

	def __repr__(self):
		return "<Node(id='%s', enb='%s')>" % (self.id, self.node_id)


if __name__ == '__main__':
	print('Creating tables')
	Base.metadata.create_all(engine)
