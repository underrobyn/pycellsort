class Filter:
	mnc_filters = {}

	def __repr__(self):
		return "<CellFilter(DE)>"

	def __init__(self):
		self.mnc_filters["1"] = self.telekom
		self.mnc_filters["2"] = self.vodafone
		self.mnc_filters["3"] = self.o2de

	def validate(self, mnc, enb, sid):
		if mnc not in self.mnc_filters:
			raise Exception('Cell filter not found for mnc %s' % mnc)

		return self.mnc_filters[mnc](enb, sid)

	def vodafone(self, enb, sid):
		valid_sectors = (
			1, 2, 3,			# L08
			5, 6, 7,			# L26
			8, 9, 10,			# L18
			19, 20, 21,			# L21
			25, 26, 27,			# L09
			31, 32, 33,			# L07
			43, 44, 45,			# B38
			151, 152, 153		# B38
		)

		if sid not in valid_sectors:
			return False

		if enb < 200000 and 60000 >= enb > 70000:
			return False

		return True

	def telekom(self, enb, sid):
		valid_sectors = (
			0, 1, 2,
			3, 4, 5,
			6, 7, 8,
			9, 10, 11,
			15, 16, 17
		)

		if sid not in valid_sectors:
			return False

		if enb < 100000:
			return False

		return True

	def o2de(self, enb, sid):
		valid_sectors = (
			1, 2, 3, 4,			# L08 Normal
			13, 14, 15, 16,		# L26 Normal
			25, 26, 27, 28,		# L18 Normal
			37, 38, 39, 40,		# L21 Normal
			49, 50, 51,			# L07 Normal
			61, 62, 63			# L09 Normal
		)
		valid_or_sectors = (
			11, 12, 13,			# L07 OpenRAN
			21, 22, 23,			# L08 OpenRAN
			# 31, 32, 33,		# L09? OpenRAN
			41, 42, 43,			# L18 OpenRAN
			51, 52, 53,			# L21 OpenRAN
			61, 62, 63			# L26 OpenRAN
		)

		if sid not in valid_sectors and sid not in valid_or_sectors:
			return False

		if 10000 >= enb >= 200000:
			return False

		return True
