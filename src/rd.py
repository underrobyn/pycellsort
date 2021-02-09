from classes.MozNode import MozNode
from classes.MozSector import MozSector
from time import time
from os.path import isfile
import pickle


class CellIDStore:

	cell_ids = {}
	rat_list = ['LTE']
	mcc_list = []
	mnc_list = {}

	pickle_loc = 'cellidstore.pickle'
	pickle_inc_loc = 'cellidstore_ver%s.pickle'

	def __init__(self, allowed_rats, allowed_mccs, allowed_mncs):
		self.rat_list = allowed_rats
		self.mcc_list = allowed_mccs
		self.mnc_list = allowed_mncs

		self.load_store()
		self.create_store()

	def load_store(self):
		if not isfile(self.pickle_loc):
			print('No current database exists. We will create one later')
			return

		with open(self.pickle_loc, 'rb') as fp:
			self.cell_ids = pickle.loads(fp.read())

		print('Loaded Pickle file, found keys:')
		print(self.cell_ids.keys())

	def save_store(self):
		print('Saving data')

		with open(self.pickle_loc, 'wb') as fp:
			fp.write(pickle.dumps(self.cell_ids))
			print('Saved main-file')

		with open(self.pickle_inc_loc % self.get_time(), 'wb') as fp:
			fp.write(pickle.dumps(self.cell_ids))
			print('Saved backup-file')

	def create_store(self):
		changes = False

		for mcc in self.mcc_list:
			if mcc not in self.cell_ids:
				print('MCC created!', mcc)
				self.cell_ids[mcc] = {}
				changes = True

			for mnc in self.mnc_list[mcc]:
				if mnc not in self.cell_ids[mcc]:
					print('MNC created!', mcc, mnc)
					self.cell_ids[mcc][mnc] = {}
					changes = True

		if changes:
			print('There have been changes to the MCC / MNC codes in the CellIDStore')

	def check_allowed(self, rat, mcc, mnc):
		if rat not in self.rat_list: return False
		if mcc not in self.mcc_list: return False
		if mnc not in self.mnc_list[mcc]: return False
		return True

	def get_time(self):
		return round(time(), 3)

	def read_csv(self, file_loc):
		line_counter = 0
		allowed_counter = 0
		st = self.get_time()

		with open(file_loc) as f:
			line = f.readline()

			while line:
				line_counter += 1

				if line_counter % 500000 == 0:
					print('\t%s\t%s\t%s' % (allowed_counter, line_counter, round(self.get_time() - st,3)))

				line = f.readline()
				if ',' not in line:
					print('> No CSV data at line:', line_counter)
					continue

				# https://ichnaea.readthedocs.io/en/latest/import_export.html
				row = line.split(',')
				if not self.check_allowed(row[0], row[1], row[2]): continue
				allowed_counter += 1

				# Check cell ID won't break the decomposition function
				cid = int(row[4])
				if cid < 256:continue

				# Decompose cell id into
				enb, sid = self.decompose_cellid(cid)

				# Create MozNode if not exists
				if enb not in self.cell_ids[row[1]][row[2]]:
					self.cell_ids[row[1]][row[2]][enb] = MozNode(row[1], row[2], enb)

				self.cell_ids[row[1]][row[2]][enb].update_sector(
					MozSector(sid, row[5], row[3], row[7], row[6], row[8], row[9], row[11], row[12])
				)

	def decompose_cellid(self, cid):
		binstr = bin(cid)
		sid = str(int(binstr[-8:], 2))
		nid = str(int(binstr[:-8], 2))

		return nid, sid
