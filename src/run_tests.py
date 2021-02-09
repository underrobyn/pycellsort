from CellFilters import CellFilter
from tests import cell_filter

tests = []

# CellFilter tests
cf = CellFilter()
tests = tests + cell_filter.tests

failures = 0
for test in tests:
	print("\n>> " + test)
	result = eval(test)

	if not result:
		failures += 1

	print(result)

print("\n%s tests completed, %s failed." % (len(tests), failures))