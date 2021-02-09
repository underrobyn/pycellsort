from models import engine, Sector, Node
from moz import MozSector, MozNode
from sqlalchemy.orm import sessionmaker
import pickle

cell_ids = {}
with open('../exports/dump-enblocs.pickle', 'rb') as fp:
	cell_ids = pickle.loads(fp.read())

print(cell_ids.keys())

Session = sessionmaker(bind=engine)
session = Session()

for mcc in cell_ids:
	for mnc in cell_ids[mcc]:
		for enb in cell_ids[mcc][mnc]:
			ntmp = cell_ids[mcc][mnc][enb]

			# Add all sectors for a node
			for sector in ntmp.sectors:
				tmp = ntmp.sectors[sector]
				session.add(Sector(
					mcc=mcc,
					mnc=mnc,
					node_id=enb,
					sector_id=sector,

					pci=tmp.pci,

					lat=tmp.lat,
					lng=tmp.lng,

					samples=tmp.samples,
					created=tmp.created,
					updated=tmp.updated
				))

			# Add node itself
			session.add(Node(
				mcc=mcc,
				mnc=mnc,
				node_id=enb,

				lat=ntmp.lat,
				lng=ntmp.lng
			))

print('All data added. Saving...')
session.commit()