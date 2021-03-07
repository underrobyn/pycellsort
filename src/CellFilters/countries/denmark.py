class Filter:
	mnc_filters = {}

	def __repr__(self):
		return "<CellFilter(DK)>"

	def __init__(self):
		self.mnc_filters["2"] = self.telia_telenor
		self.mnc_filters["6"] = self.hi3g
		self.mnc_filters["20"] = self.telia_telenor

	def validate(self, mnc, enb, sid):
		if mnc not in self.mnc_filters:
			raise Exception('Cell filter not found for mnc %s' % mnc)

		return self.mnc_filters[mnc](enb, sid)

	def telia_telenor(self, enb, sid):
		valid_sectors = (
			10, 20, 30,     # L18
			11, 21, 31,     # L26C1
			12, 22, 32,     # L08
			13, 23, 33,     # L21
			14, 24, 34,     # L09
			15, 25, 35,     # L07
			111, 121, 131   # L26C2
		)

		if sid not in valid_sectors:
			return False

		if 190000 > enb < 160000:
			return False

		return True

	def hi3g(self, enb, sid):
		valid_sectors = (
			0, 1, 2,        # L26
			10, 11, 12,     # L26T
			50, 51, 52,     # L18
			60, 61, 62      # L18C2
		)

		if sid not in valid_sectors:
			return False

		if enb > 100000:
			return False

		return True
