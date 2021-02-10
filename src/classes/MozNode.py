from math import ceil, log, log10
from statistics import mean, stdev


class MozNode:
	def __init__(self, mcc, mnc, node_id):
		self.mcc = mcc
		self.mnc = mnc
		self.node_id = node_id

		self.lat = 0
		self.lng = 0

		self.sectors_total_lat = 0
		self.sectors_total_lng = 0
		self.sectors_mean_lat = 0
		self.sectors_mean_lng = 0
		self.sectors_stdev_lat = 0
		self.sectors_stdev_lng = 0

		self.sectors = {}
		self.sector_count = 0

	def update_sector(self, sector):
		if sector.sector_id in self.sectors:
			# print('Duplicate sector, %s-%s-> %s:%s' % (self.mcc, self.mnc, self.node_id, sector.sector_id))
			pass
		else:
			self.sectors[sector.sector_id] = sector
			self.sector_count += 1

	def calc_sector_stats(self):
		lats = []
		lngs = []

		for sector in self.sectors:
			lats.append(self.sectors[sector].lat)
			lngs.append(self.sectors[sector].lng)

		self.sectors_total_lat = sum(lats)
		self.sectors_total_lng = sum(lngs)
		self.sectors_mean_lat = mean(lats)
		self.sectors_mean_lng = mean(lngs)

		if self.sector_count > 1:
			self.sectors_stdev_lat = stdev(lats)
			self.sectors_stdev_lng = stdev(lngs)

	def calc_loc(self):
		self.calc_sector_stats()

		# If deviation from mean is 0 we already have the best location
		if self.sectors_stdev_lat == 0 and self.sectors_stdev_lng == 0:
			self.lat = self.sectors_mean_lat
			self.lng = self.sectors_mean_lng
			return

		total_lat = total_lng = total_weight = 0

		for sector_id in self.sectors:
			sector = self.sectors[sector_id]

			deviation_lat = 0
			deviation_lng = 0
			if self.sectors_stdev_lat != 0:
				deviation_lat = abs((self.sectors_mean_lat - sector.lat) / self.sectors_stdev_lat)
			if self.sectors_stdev_lng != 0:
				deviation_lng = abs((self.sectors_mean_lng - sector.lng) / self.sectors_stdev_lng)

			deviation_total = deviation_lat + deviation_lng

			deviation_weight = (-1 * log10(deviation_total**2 + 1)) + 1
			if deviation_weight < 0:
				deviation_weight = 0

			cell_weight = 1 + ceil(log(sector.samples)) + deviation_weight

			total_lat += sector.lat * cell_weight
			total_lng += sector.lng * cell_weight
			total_weight += cell_weight

		self.lat = total_lat / total_weight
		self.lng = total_lng / total_weight
