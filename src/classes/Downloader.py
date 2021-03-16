from datetime import datetime, timedelta
from urllib import request
from shutil import copyfileobj
from os.path import isfile
import gzip as gz
from config import EXPORTS_DIR


class Downloader:

    mls_base = 'https://d2koia3g127518.cloudfront.net/export/'

    def __init__(self):
        pass

    def download_file(self):
        url = self._get_mls_url()
        file_name = self._get_mls_file_name() + '.gz'

        print('Downloading:', url, file_name)
        downloaded_file, http_msg = request.urlretrieve(url=url, filename=file_name)

        print(http_msg)

        return downloaded_file

    def download_to_exports_dir(self):
        file_name = self.download_file()
        out_location = EXPORTS_DIR + self._get_mls_file_name()

        if not isfile(file_name):
            print('Could find a file at:', file_name)
            return

        print('File will be extracted to:', out_location)
        with gz.open(file_name, 'rb') as f_in:
            with open(out_location, 'wb') as f_out:
                copyfileobj(f_in, f_out)

        print('Done')
        return out_location

    def _get_mls_file_name(self):
        t_minus1h = datetime.now() - timedelta(hours=1)
        t_minus1h_str = t_minus1h.strftime("%Y-%m-%dT%H")
        return 'MLS-diff-cell-export-%s0000.csv' % t_minus1h_str

    def _get_mls_url(self):
        return self.mls_base + self._get_mls_file_name() + '.gz'


if __name__ == '__main__':
    dl = Downloader()
    dl._get_mls_url()