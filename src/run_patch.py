from classes.PyCellDB import PyCellDB
from classes.CellIDStore import CellIDStore
from classes.Downloader import Downloader
import config as c
from time import time

start_time = time()

# Load previous data if it exists
cs = CellIDStore(c.ALLOWED_RATS, c.ALLOWED_MCCS, c.ALLOWED_MNCS)

# Download latest differential data
dl = Downloader()
file_to_patch = dl.download_to_exports_dir()

# Update data
cs.read_csv(file_to_patch)

# TODO: Write function to find changes to cellidstore since read from save file

# TODO: Write function to only update meta for nodes that changed
cs.update_node_meta()

# Save data
cs.save_store()

# Update database
db = PyCellDB(driver='mysql+pymysql', user=c.db_user, password=c.db_password, host=c.db_addr, port=c.db_port, db='pycellsort')

# TODO: Write function to update database records rather than just inserting data from objects

# Commit database changes
db.commit()

print('Done patch after %ss' % (round(time() - start_time, 3)))
