class Filter:
	mnc_filters = {}

	def __repr__(self):
		return "<CellFilter(NG)>"

	def __init__(self):
		self.mnc_filters["20"] = self.airtel
		self.mnc_filters["30"] = self.mtn
		self.mnc_filters["50"] = self.glo

	def validate(self, mnc, enb, sid):
		if mnc not in self.mnc_filters:
			raise Exception('Cell filter not found for mnc %s' % mnc)

		return self.mnc_filters[mnc](enb, sid)

	def mtn(self, enb, sid):
		valid_sectors = (
			1, 2, 3,			# L08
			4, 5, 6,			# L26
			10, 11, 12,			# L07
			81, 82, 83			# L21
		)

		if sid not in valid_sectors:
			return False

		if 200000 > enb > 1000000:
			return False

		return True

	def airtel(self, enb, sid):
		valid_sectors = (
			1, 2, 3,			# L18
			11, 12, 13,			# L26
			21, 22, 23			# L09
		)

		if sid not in valid_sectors:
			return False

		if 1000 > enb > 300000:
			return False

		return True

	def glo(self, enb, sid):
		valid_sectors = (
			1, 2, 3,			# L07
			4, 5, 6				# L18
		)

		if sid not in valid_sectors:
			return False

		if 1 > enb > 10000:
			return False

		return True
