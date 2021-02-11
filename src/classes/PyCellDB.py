from sqlalchemy.engine.url import URL
from sqlalchemy.exc import InternalError
from classes.CellModels import Base, Sector, Node
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class PyCellDB:

	cell_ids = {}

	def __init__(self, **kwargs):
		if 'driver' in kwargs:
			self.url = URL(kwargs['driver'], kwargs['user'], kwargs['password'], kwargs['host'], kwargs['port'], kwargs['db'])

			# Hack to establish SSL connection (see #231)
			try:
				self._engine = create_engine(self.url, echo=False, connect_args={'ssl': {'activate': True}})
				self._engine.connect().close()
			except InternalError:
				self._engine = create_engine(self.url, echo=False)
		else:
			self._engine = create_engine('sqlite:///pycell.db', echo=False)

		self._Session = sessionmaker(bind=self._engine)
		self._db = self._Session()

		# Create the schema on the database. It won't replace any existing schema
		Base.metadata.create_all(self._engine)

	def commit(self):
		print('Saving changes to db')
		self._db.commit()

	def insert_cells(self, cell_ids):
		self.cell_ids = cell_ids
		self.insert_data()

	def insert_data(self):
		for mcc in self.cell_ids:
			for mnc in self.cell_ids[mcc]:
				print('Inserting %s eNBs for %s-%s' % (len(self.cell_ids[mcc][mnc]), mcc, mnc))
				for enb in self.cell_ids[mcc][mnc]:
					self.__insert_node(mcc, mnc, enb)

	def __insert_sector(self, mcc, mnc, enb, sector):
		self._db.add(Sector(
			mcc=mcc,
			mnc=mnc,
			node_id=enb,
			sector_id=sector.sector_id,

			pci=sector.pci,

			lat=sector.lat,
			lng=sector.lng,
			range=sector.range,

			samples=sector.samples,
			created=sector.created,
			updated=sector.updated
		))

	def __insert_node(self, mcc, mnc, enb):
		node = self.cell_ids[mcc][mnc][enb]

		# Add all sectors for a node
		for sector in node.sectors:
			self.__insert_sector(mcc, mnc, enb, node.sectors[sector])

		# Add the node itself
		self._db.add(Node(
			mcc=mcc,
			mnc=mnc,
			node_id=enb,

			lat=node.lat,
			lng=node.lng,
			mean_lat=node.sectors_mean_lat,
			mean_lng=node.sectors_mean_lng
		))
