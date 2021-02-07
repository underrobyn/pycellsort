from CellFilters import CellFilter

cf = CellFilter()

tests = [
	# Check out of bounds
	'cf.validate("234", "10", "0", "0") == False',
	'cf.validate("234", "15", "0", "0") == False',
	'cf.validate("234", "20", "0", "0") == False',
	'cf.validate("234", "30", "0", "0") == False',

	'cf.validate("234", "10", "0", "256") == False',
	'cf.validate("234", "15", "0", "256") == False',
	'cf.validate("234", "20", "0", "256") == False',
	'cf.validate("234", "30", "0", "256") == False',

	# O2
	'cf.validate("234", "10", "91", "110") == True',
	'cf.validate("234", "10", "510005", "110") == True',
	'cf.validate("234", "10", "91", "10") == False',
	'cf.validate("234", "10", "510005", "10") == False',

	# VF
	'cf.validate("234", "15", "91", "10") == True',
	'cf.validate("234", "15", "510005", "10") == True',
	'cf.validate("234", "15", "91", "110") == False',
	'cf.validate("234", "15", "510005", "110") == False',

	# Check Three's small cells
	'cf.validate("234", "20", "50001", "16") == True',
	'cf.validate("234", "20", "50001", "0") == False',

	# EE
	'cf.validate("234", "30", "11000", "30") == False',
	'cf.validate("234", "30", "15350", "2") == True'
]

failures = 0
for test in tests:
	result = eval(test)

	if result == False:
		failures += 1

	print("\n>> " + test)
	print(result)

print("\n%s tests completed, %s failed." % (len(tests), failures))