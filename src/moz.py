class MozSector:
	def __init__(self, sector_id, pci, tac, lat, lng, cellrange, samples, created, updated):
		self.sector_id = sector_id
		self.pci = pci
		self.tac = tac

		self.lat = float(lat)
		self.lng = float(lng)

		self.range = int(cellrange)
		self.samples = int(samples)
		self.created = created
		self.updated = updated


class MozNode:
	def __init__(self, mcc, mnc, node_id):
		self.mcc = mcc
		self.mnc = mnc
		self.node_id = node_id

		self.lat = 0
		self.lng = 0

		self.sectors = {}

	def update_sector(self, sector):
		if sector.sector_id in self.sectors:
			# print('Duplicate sector, %s-%s-> %s:%s' % (self.mcc, self.mnc, self.node_id, sector.sector_id))
			pass
		else:
			self.sectors[sector.sector_id] = sector

		self.calc_loc()

	def calc_loc(self):
		slat = slng = 0
		scount = len(self.sectors)

		for sector in self.sectors:
			slat += self.sectors[sector].lat
			slng += self.sectors[sector].lng

		self.lat = slat / scount
		self.lng = slng / scount
