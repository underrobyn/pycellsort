from CellFilters import CellFilter

cf = CellFilter()

tests = [
	# Check out of bounds
	'cf.validate("234", "10", 0, 0) == False',
	'cf.validate("234", "15", 0, 0) == False',
	'cf.validate("234", "20", 0, 0) == False',
	'cf.validate("234", "30", 0, 0) == False',

	'cf.validate("234", "10", 0, 256) == False',
	'cf.validate("234", "15", 0, 256) == False',
	'cf.validate("234", "20", 0, 256) == False',
	'cf.validate("234", "30", 0, 256) == False',

	# O2
	'cf.validate("234", "10", 91, 110) == True',
	'cf.validate("234", "10", 510005, 110) == True',
	'cf.validate("234", "10", 112758, 116) == True',
	'cf.validate("234", "10", 112758, 117) == True',
	'cf.validate("234", "10", 112958, 115) == True',
	'cf.validate("234", "10", 531346, 127) == True',
	'cf.validate("234", "10", 531346, 156) == True',
	'cf.validate("234", "10", 531346, 165) == True',
	'cf.validate("234", "10", 91, 10) == False',
	'cf.validate("234", "10", 510000, 10) == False',

	# VF
	'cf.validate("234", "15", 91, 10) == True',
	'cf.validate("234", "15", 510005, 10) == True',
	'cf.validate("234", "15", 12958, 10) == True',
	'cf.validate("234", "15", 12958, 14) == True',
	'cf.validate("234", "15", 13153, 18) == True',
	'cf.validate("234", "15", 91, 110) == False',
	'cf.validate("234", "15", 510005, 110) == False',

	# 3
	'cf.validate("234", "20", 256, 0) == True',
	'cf.validate("234", "20", 321, 0) == True',
	'cf.validate("234", "20", 17000, 2) == False',
	'cf.validate("234", "20", 40000, 2) == False',
	'cf.validate("234", "20", 49501, 2) == True',
	'cf.validate("234", "20", 49565, 8) == True',
	'cf.validate("234", "20", 49522, 71) == True',

	# Check Three's small cells
	'cf.validate("234", "20", 50001, 16) == True',
	'cf.validate("234", "20", 50022, 16) == True',
	'cf.validate("234", "20", 50001, 0) == False',

	# EE
	'cf.validate("234", "30", 11000, 30) == False',
	'cf.validate("234", "30", 27980, 22) == False',
	'cf.validate("234", "30", 40000, 20) == False',
	'cf.validate("234", "30", 15350, 2) == True',
	'cf.validate("234", "30", 15350, 5) == True',
	'cf.validate("234", "30", 14160, 16) == True'
]

failures = 0
for test in tests:
	print("\n>> " + test)
	result = eval(test)

	if not result:
		failures += 1

	print(result)

print("\n%s tests completed, %s failed." % (len(tests), failures))