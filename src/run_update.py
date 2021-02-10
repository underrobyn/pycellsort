from classes.PyCellDB import PyCellDB
from classes.CellIDStore import CellIDStore
import config as c
from time import time

start_time = time()

# Load previous data if it exists
cs = CellIDStore(c.ALLOWED_RATS, c.ALLOWED_MCCS, c.ALLOWED_MNCS)

# Download latest data


# Update data
export_file = c.EXPORTS_DIR + 'MLS-full-cell-export-2021-02-10T000000.csv'
cs.read_csv(export_file)
cs.update_locations()

# Save data
cs.save_store()

# Update database
db = PyCellDB()
db.insert_cells(cs.cell_ids)
db.commit()

print('Done after %ss' % (round(time() - start_time, 3)))
