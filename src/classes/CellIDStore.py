from classes.MozNode import MozNode
from classes.MozSector import MozSector
from CellFilters import CellFilter
from time import time
from os.path import isfile
import pickle


def get_time():
	return round(time(), 3)


class CellIDStore:
	cell_ids = {}
	rat_list = ['LTE']
	mcc_list = []
	mnc_list = {}
	save_backup = False
	update_every = 1000000

	pickle_loc = 'cellidstore.pickle'
	pickle_inc_loc = 'cellidstore_ver%s.pickle'

	def __init__(self, allowed_rats, allowed_mccs, allowed_mncs):
		self.rat_list = allowed_rats
		self.mcc_list = allowed_mccs
		self.mnc_list = allowed_mncs

		self.load_store()
		self.create_store()

		self.cell_filter = CellFilter()

	def load_store(self):
		if not isfile(self.pickle_loc):
			print('No current database exists. We will create one later')
			return

		with open(self.pickle_loc, 'rb') as fp:
			self.cell_ids = pickle.loads(fp.read())

		print('Loaded Pickle file, found keys:')
		print(list(self.cell_ids.keys()))
		print()

	def save_store(self):
		print('Saving data')

		with open(self.pickle_loc, 'wb') as fp:
			fp.write(pickle.dumps(self.cell_ids))
			print('Saved main-file')

		if self.save_backup:
			with open(self.pickle_inc_loc % get_time(), 'wb') as fp:
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
			print('There have been changes to the MCC / MNC codes in the CellIDStore\n')

	def check_allowed(self, rat, mcc, mnc):
		if rat not in self.rat_list: return False
		if mcc not in self.mcc_list: return False
		if mnc not in self.mnc_list[mcc]: return False
		return True

	def read_csv(self, file_loc):
		line_counter = 0
		allowed_counter = 0
		st = get_time()

		print('Started parsing file: %s\nProgress printed every %s rows' % (file_loc, self.update_every))
		with open(file_loc) as f:
			line = f.readline()

			while line:
				line_counter += 1

				if line_counter % 1000000 == 0:
					print('\t%s\t%s\t%ss' % (allowed_counter, line_counter, round(get_time() - st, 3)))

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
				if cid < 256: continue

				# Decompose cell id into
				enb, sid = self.decompose_cellid(cid)

				if not self.cell_filter.validate(row[1], row[2], int(enb), int(sid)):
					# print('Bad sector at:', row[1], row[2], enb, sid)
					continue

				# Create MozNode if not exists
				if enb not in self.cell_ids[row[1]][row[2]]:
					self.cell_ids[row[1]][row[2]][enb] = MozNode(row[1], row[2], enb)

				self.cell_ids[row[1]][row[2]][enb].update_sector(
					MozSector(sid, row[5], row[3], row[7], row[6], row[8], row[9], row[11], row[12])
				)

		print('\t%s\t%s\t%ss\nParsing Complete for: %s\n' % (allowed_counter, line_counter, round(get_time() - st, 3), file_loc))

	def update_node_meta(self):
		for mcc in self.cell_ids:
			for mnc in self.cell_ids[mcc]:
				print('Running eNB calculations for %s eNBs for %s-%s' % (len(self.cell_ids[mcc][mnc]), mcc, mnc))
				for enb in self.cell_ids[mcc][mnc]:
					self.cell_ids[mcc][mnc][enb].update_node_meta()
					self.cell_ids[mcc][mnc][enb].calc_loc()

	def decompose_cellid(self, cid):
		binstr = bin(cid)
		sid = str(int(binstr[-8:], 2))
		nid = str(int(binstr[:-8], 2))

		return nid, sid
