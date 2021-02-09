from classes.PyCellDB import PyCellDB
from classes.CellIDStore import CellIDStore
import config as c

# Load previous data if it exists
cs = CellIDStore(c.ALLOWED_RATS, c.ALLOWED_MCCS, c.ALLOWED_MNCS)

# Download latest data


# Update data
export_file = c.EXPORTS_DIR + 'MLS-full-cell-export-2021-02-03T000000.csv'
cs.read_csv(export_file)

# Save data
cs.save_store()

# Update database
db = PyCellDB()
db.insert_cells(cs.cell_ids)
db.commit()
