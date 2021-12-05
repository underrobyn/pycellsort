class Filter:
	mnc_filters = {}

	def __repr__(self):
		return "<CellFilter(UK)>"

	def __init__(self):
		self.mnc_filters["4"] = self.other
		self.mnc_filters["10"] = self.o2
		self.mnc_filters["15"] = self.vodafone
		self.mnc_filters["20"] = self.three
		self.mnc_filters["30"] = self.ee
		self.mnc_filters["31"] = self.ee
		self.mnc_filters["32"] = self.ee
		self.mnc_filters["55"] = self.sure
		self.mnc_filters["58"] = self.manx

	def validate(self, mnc, enb, sid):
		if mnc not in self.mnc_filters:
			raise Exception('Cell filter not found for mnc %s' % mnc)

		return self.mnc_filters[mnc](enb, sid)

	def o2(self, enb, sid):
		valid_vf_host = (
			110, 120, 130, 140, 150, 160,  	# L08
			112, 122, 132, 142, 152, 162,  	# L09
			114, 124, 134, 144, 154, 164,  	# L21
			115, 125, 135, 145, 155, 165,  	# L23-C1
			116, 126, 136, 146, 156, 166,  	# L18
			117, 127, 137, 147, 157, 167   	# L23-C2
		)
		valid_o2_host = (
			23, 68, 						# Spidercloud cells
			110, 120, 130, 140, 150, 160,  	# L08
			112, 122, 132, 142, 152, 162,  	# L09
			114, 124, 134, 144, 154, 164,  	# L18
			115, 125, 135, 145, 155, 165,  	# L21
			116, 126, 136, 146, 156, 166,  	# L23-C1
			117, 127, 137, 147, 157, 167,  	# L23-C2
			118, 128, 138,					# L26 TDD
			119, 129, 139					# L07
		)

		if (3 < enb < 15000 or 100000 < enb < 115000) and sid in valid_vf_host:
			return True

		if 500000 < enb < 550000 and sid in valid_o2_host:
			return True

		return False

	def vodafone(self, enb, sid):
		valid_vf_host = (
			1, 2, 3, 4, 5, 6, 7, 8, 9,	# DAS Exceptions
			10, 20, 30, 40, 50, 60,		# L08
			21, 22,						# DAS Exceptions
			12, 22, 32, 42, 52, 62,		# L09
			14, 24, 34, 44, 54, 64,		# L21
			16, 26, 36, 46, 56, 66,		# L18
			18, 28, 38, 48, 58, 68,		# L26
			19, 29, 39					# L26 TDD
		)
		valid_o2_host = (
			10, 20, 30, 40, 50, 60,		# L08
			12, 22, 32, 42, 52, 62,		# L09
			14, 24, 34, 44, 54, 64,		# L18
			15, 25, 35, 45, 55, 65,		# L21
			18, 28, 38, 48, 58, 68,		# L26
		)

		if 3 < enb < 14500 and sid in valid_vf_host:
			return True

		if 500000 < enb < 545000 and sid in valid_o2_host:
			return True

		return False

	def three(self, enb, sid):
		if enb < 256:
			return False

		if 49999 < enb < 50025:
			if sid == 16:
				return True
			return False

		# Three's 8xxxx eNB DASes
		if 80000 < enb < 80100:
			return False

		if enb > 15000 and not (49000 < enb < 49999 or 50025 < enb < 51500):
			return False

		if sid not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 71, 72, 73, 74, 75, 76, 91, 92, 93):
			return False

		return True

	def ee(self, enb, sid):
		if 10000 < enb < 40000:
			if sid > 24 and sid not in (30, 31, 32):
				return False

			return True

		return False

	def sure(self, enb, sid):
		if enb > 300:
			return False
		return True

	def manx(self, enb, sid):
		if enb > 99:
			return False
		return True

	def other(self, enb, sid):
		return True
