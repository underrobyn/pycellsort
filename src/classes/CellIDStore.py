from classes.MozNode import MozNode
from classes.MozSector import MozSector
from CellFilters import CellFilter
from time import time
from functools import lru_cache
from os.path import isfile
import pickle


def get_time():
	return round(time(), 3)


def decompose_cellid(cid):
	binstr = bin(cid)
	sid = str(int(binstr[-8:], 2))
	nid = str(int(binstr[:-8], 2))

	return nid, sid


class CellIDStore:
	cell_ids = {}

	rat_list = ['LTE']
	mcc_list = []
	mnc_list = {}

	_file_list = set()
	_changes = False

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
		self._changes = False

		for mcc in self.mcc_list:
			if mcc not in self.cell_ids:
				print('MCC created!', mcc)
				self.cell_ids[mcc] = {}
				self._changes = True

			for mnc in self.mnc_list[mcc]:
				if mnc not in self.cell_ids[mcc]:
					print('MNC created!', mcc, mnc)
					self.cell_ids[mcc][mnc] = {}
					self._changes = True

		if self._changes:
			print('There have been changes to the MCC / MNC codes in the CellIDStore\n')

	# TODO: Enable when lists are larger, currently makes performance worse by a few ms
	# @lru_cache(maxsize=256)
	def check_allowed(self, rat, mcc, mnc):
		if rat not in self.rat_list: return False
		if mcc not in self.mcc_list: return False
		if mnc not in self.mnc_list[mcc]: return False
		return True

	def check_file_processed(self, file_name):
		# If file name in list, don't re-process it unless new MCC / MNC added
		if file_name in self._file_list:
			if self._changes:
				return True

			# There were no changes so return False
			return False

		# If file not previously processed, add name to list
		self._file_list.add(file_name)

		return True

	def read_csv(self, dir_name, file_name):
		line_counter = 0
		allowed_counter = 0
		st = get_time()

		# TODO: Could change this to use a hash of file instead of file name?
		if not self.check_file_processed(file_name):
			print('Skipping parsing of file %s' % file_name)
			return

		# https://codereview.stackexchange.com/questions/79449/need-fast-csv-parser-for-python-to-parse-80gb-csv-file
		print('Started parsing file: %s\nProgress printed every %s rows' % (file_name, self.update_every))
		with open(dir_name + file_name) as f:
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
				enb, sid = decompose_cellid(cid)

				if not self.cell_filter.validate(row[1], row[2], int(enb), int(sid)):
					# print('Bad sector at:', row[1], row[2], enb, sid)
					continue

				# Create MozNode if not exists
				if enb not in self.cell_ids[row[1]][row[2]]:
					self.cell_ids[row[1]][row[2]][enb] = MozNode(row[1], row[2], enb)

				self.cell_ids[row[1]][row[2]][enb].update_sector(
					MozSector(sid, row[5], row[3], row[7], row[6], row[8], row[9], row[11], row[12])
				)

		print('Parsing Complete for: %s\n\t- Total rows: %s\n\t- Total stored: %s\n\t- Time taken: %ss\n' %
			  (file_name, line_counter, allowed_counter, round(get_time() - st, 4)))

	def update_node_meta(self):
		for mcc in self.cell_ids:
			for mnc in self.cell_ids[mcc]:
				print('Running eNB calculations for %s eNBs for %s-%s' % (len(self.cell_ids[mcc][mnc]), mcc, mnc))
				for enb in self.cell_ids[mcc][mnc]:
					self.cell_ids[mcc][mnc][enb].update_node_meta()
					self.cell_ids[mcc][mnc][enb].calc_loc()
