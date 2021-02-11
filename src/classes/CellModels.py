from sqlalchemy import Column, Integer, SmallInteger, Sequence
from sqlalchemy.types import DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sector(Base):
	__tablename__ = 'sectors'

	id = Column(Integer, Sequence('sector_id_seq'), primary_key=True)

	mcc = Column(SmallInteger)
	mnc = Column(SmallInteger, index=True)

	node_id = Column(Integer, index=True)
	sector_id = Column(SmallInteger)
	pci = Column(SmallInteger)

	lat = Column(DECIMAL(8, 6))
	lng = Column(DECIMAL(9, 6))
	range = Column(Integer)

	samples = Column(Integer)
	created = Column(Integer)
	updated = Column(Integer)

	def __repr__(self):
		return "<Sectors(id='%s', enb='%s', sector='%s')>" % (self.id, self.node_id, self.sector_id)


class Node(Base):
	__tablename__ = 'nodes'

	id = Column(Integer, Sequence('node_id_seq'), primary_key=True)

	mcc = Column(SmallInteger)
	mnc = Column(SmallInteger, index=True)

	node_id = Column(Integer, index=True)

	lat = Column(DECIMAL(8, 6))
	lng = Column(DECIMAL(9, 6))
	mean_lat = Column(DECIMAL(8, 6))
	mean_lng = Column(DECIMAL(9, 6))

	def __repr__(self):
		return "<Node(id='%s', enb='%s')>" % (self.id, self.node_id)
