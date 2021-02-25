class Filter:
	mnc_filters = {}

	def __repr__(self):
		return "<CellFilter(Cuba)>"

	def __init__(self):
		self.mnc_filters["1"] = self.cubacel

	def validate(self, mnc, enb, sid):
		if mnc not in self.mnc_filters:
			raise Exception('Cell filter not found for mnc %s' % mnc)

		return self.mnc_filters[mnc](enb, sid)

	def cubacel(self, enb, sid):
		if 420000 > enb < 400000:
			return False

		if sid not in (1, 2, 3, 4, 5, 6):
			return False

		return True
