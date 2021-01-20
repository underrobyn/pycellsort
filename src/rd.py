from time import time
from moz import MozSector, MozNode
import pickle

# Allowed data
allowed_rats = ['LTE']
allowed_mccs = ['234']
allowed_mncs = {
	'234': ['10', '15', '20', '30']
}

# Generate empty data structure
cell_ids = {}
for mcc in allowed_mncs:
	cell_ids[mcc] = {}
	for mnc in allowed_mncs[mcc]:
		cell_ids[mcc][mnc] = {}

# Counters
line_counter = 0
allowed_counter = 0
st = time()


def decomposeCellId(cid):
	binstr = bin(cid)
	sid = str(int(binstr[-8:], 2))
	nid = str(int(binstr[:-8], 2))

	return nid, sid


with open('../exports/MLS-full-cell-export-2021-01-17T000000.csv') as f:
	line = f.readline()
	print(line)

	while line:
		line_counter += 1

		if line_counter % 500000 == 0:
			print(allowed_counter, line_counter, str(time() - st))

		line = f.readline()
		if ',' not in line:
			print('Error at line:', line_counter)
			continue

		# https://ichnaea.readthedocs.io/en/latest/import_export.html
		row = line.split(',')

		if row[0] not in allowed_rats:
			continue
		if row[1] not in allowed_mccs:
			continue
		if row[2] not in allowed_mncs[row[1]]:
			continue

		allowed_counter += 1

		# Check cell ID won't break the decomposition function
		cid = int(row[4])
		if cid < 256:
			print(cid, 'invalid')
			continue

		# Decompose cell id into
		enb, sid = decomposeCellId(cid)

		# Create MozNode if not exists
		if enb not in cell_ids[row[1]][row[2]]:
			cell_ids[row[1]][row[2]][enb] = MozNode(row[1], row[2], enb)

		cell_ids[row[1]][row[2]][enb].update_sector(
			MozSector(sid, row[5], row[3], row[7], row[6], row[8], row[9], row[11], row[12])
		)

print('Dumping data')
with open('../exports/dump-enblocs.pickle', 'wb') as fp:
	fp.write(pickle.dumps(cell_ids))
