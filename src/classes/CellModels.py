from sqlalchemy import Column, Integer, SmallInteger, Sequence, Index, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.types import DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sector(Base):
	__tablename__ = 'sectors'

	id = Column(Integer, Sequence('sector_id_seq'), primary_key=True)

	mcc = Column(SmallInteger, nullable=False)
	mnc = Column(SmallInteger, nullable=False)

	node_id = Column(Integer, nullable=False)
	sector_id = Column(SmallInteger, nullable=False)
	pci = Column(SmallInteger, nullable=False)

	lat = Column(DECIMAL(8, 6))
	lng = Column(DECIMAL(9, 6))
	range = Column(Integer)

	samples = Column(Integer)
	created = Column(Integer)
	updated = Column(Integer)

	def __repr__(self):
		return "<Sector(id='%s', enb='%s', sector='%s')>" % (self.id, self.node_id, self.sector_id)

	__table_args__ = (
		Index('sectors_index', 'mcc', 'mnc', 'node_id', 'sector_id'),
		UniqueConstraint('mcc', 'mnc', 'node_id', 'sector_id', name='unique_sector'),
    	# ForeignKeyConstraint(['mcc', 'mnc', 'node_id',], ['nodes.mcc', 'nodes.mnc', 'nodes.node_id'])
	)


class Node(Base):
	__tablename__ = 'nodes'

	id = Column(Integer, Sequence('node_id_seq'), primary_key=True)

	mcc = Column(SmallInteger, nullable=False)
	mnc = Column(SmallInteger, nullable=False)

	node_id = Column(Integer, nullable=False)

	lat = Column(DECIMAL(8, 6), nullable=False)
	lng = Column(DECIMAL(9, 6), nullable=False)

	mean_lat = Column(DECIMAL(8, 6))
	mean_lng = Column(DECIMAL(9, 6))

	samples = Column(Integer)
	created = Column(Integer)
	updated = Column(Integer)

	def __repr__(self):
		return "<Node(mcc='%s', mnc='%s' id='%s', enb='%s')>" % (self.mcc, self.mnc, self.id, self.node_id)

	__table_args__ = (
		Index('nodes_index', 'mcc', 'mnc', 'node_id'),
		UniqueConstraint('mcc', 'mnc', 'node_id', name='unique_node')
	)
