from datetime import date
from config import OCID_API_KEY, DL_CHUNK_SIZE, EXPORTS_DIR
import gzip
import wget

today = date.today()
date_str = today.strftime("%Y-%m-%d")
lastpc = 0

urls = [
	'https://d2koia3g127518.cloudfront.net/export/MLS-full-cell-export-%sT000000.csv.gz' % date_str,
	#'https://opencellid.org/ocid/downloads?token=%s&type=full&file=cell_towers.csv.gz' % OCID_API_KEY
]


# Download files
def download_file(url):
	print('Started download: ', url)
	local_filename = url.split('?')[0].split('/')[-1]

	def bar_custom(current, total, width=80):
		global lastpc
		newpc = round(current / total * 100)
		if newpc > lastpc:
			print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))
			lastpc = newpc

	wget.download(url, bar=bar_custom)

	return local_filename


files = []
for url in urls:
	files.append(download_file(url))


# Unzip files
for file in files:
	with gzip.open(EXPORTS_DIR + file, 'rb') as f:
		file_content = f.read()

# Sort data


# Save variables if we can


# Run converter to save to db
