class Filter:

	mnc_filters = {}

	def __repr__(self):
		return "<CellFilter(UK)>"

	def __init__(self):
		self.mnc_filters["10"] = self.o2
		self.mnc_filters["15"] = self.vodafone
		self.mnc_filters["20"] = self.three
		self.mnc_filters["30"] = self.ee

	def validate(self, mnc, enb, sid):
		if mnc not in self.mnc_filters:
			raise Exception('Cell filter not found for mnc %s' % mnc)

		return self.mnc_filters[mnc](enb, sid)

	def o2(self, enb, sid):
		return True

	def vodafone(self, enb, sid):
		return True

	def three(self, enb, sid):
		return True

	def ee(self, enb, sid):
		return True
