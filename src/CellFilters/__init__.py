class CellFilter:
	modules = {
		"234": "united_kingdom"
	}
	loaded = {}
	filters = {}

	def validate(self, mcc, mnc, enb, sid):
		mnc_filter = self.check_module_exists(mcc)
		return mnc_filter.validate(mnc, enb, sid)

	def check_module_exists(self, mcc):
		if mcc in self.filters:
			return self.filters[mcc]

		if mcc not in self.loaded:
			if mcc in self.modules:
				self.loaded[mcc] = __import__('CellFilters.countries.'+self.modules[mcc], globals(), locals(), ['Filter'])
			else:
				raise Exception('Cell filter not found for mcc %s' % mcc)

		self.filters[mcc] = self.loaded[mcc].Filter()
		return self.filters[mcc]
