from time import time

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


def getEnbSecId(cid):
	pass


with open('../exports/MLS-full-cell-export-2021-01-17T000000.csv') as f:
	line = f.readline()
	print(line)

	while line:
		line_counter += 1

		if line_counter % 100000 == 0:
			print(allowed_counter, line_counter, str(time() - st))

		line = f.readline()
		if ',' not in line:
			print('Error at line:', line_counter)
			continue

		row = line.split(',')

		if row[0] not in allowed_rats:
			continue
		if row[1] not in allowed_mccs:
			continue
		if row[2] not in allowed_mncs[row[1]]:
			continue

		allowed_counter += 1

		if row[4] in cell_ids[row[1]][row[2]]:
			cell_ids[row[1]][row[2]][row[4]] += 1
			print('Found', row[4], cell_ids[row[1]][row[2]][row[4]])
		else:
			cell_ids[row[1]][row[2]][row[4]] = 1
