import gzip
import bz2
import tarfile
import hashlib
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

from tqdm import tqdm

from mmead.download_info import EMBEDDING_INFO, LINK_INFO, MAPPING_INFO


# https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, t_size=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if t_size is not None:
            self.total = t_size
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


# For large files, we need to compute MD5 block by block. See:
# https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
def compute_md5(file, block_size=2**20):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def get_cache_home():
    custom_dir = os.environ.get("MMEAD_CACHE")
    if custom_dir is not None and custom_dir != '':
        return custom_dir
    return os.path.expanduser(os.path.join(f'~{os.path.sep}.cache', "mmead"))


def download_and_unpack(name, force=False, verbose=True):
    print("BEGIN OF DOWNLOAD AND UNPACK")
    if name not in EMBEDDING_INFO and name not in LINK_INFO and name not in MAPPING_INFO:
        raise ValueError(f'Unrecognized data file: {name}')
    if name in EMBEDDING_INFO:
        target = EMBEDDING_INFO[name]
        subdirectory = EMBEDDING_INFO['_folder']
    elif name in LINK_INFO:
        target = LINK_INFO[name]
        subdirectory = LINK_INFO['_folder']
    else:
        target = MAPPING_INFO[name]
        subdirectory = MAPPING_INFO['_folder']

    to_file = os.path.join(get_cache_home(), subdirectory, f"{target['filename'][:-len(target['extension'])]}")
    if os.path.exists(to_file):
        if not force:
            if verbose:
                print(f'{to_file} already exists, skipping download.')
            return to_file
        if verbose:
            print(f'{to_file} already exists, but force=True, removing {to_file} and fetching fresh copy...')
        os.remove(to_file)

    tmp_folder = f"{target['filename'][:-len(target['extension'])]}.{target['md5']}"
    try:
        downloaded = _download(
            url=target['url'],
            target_filename=target['filename'],
            subdirectory=subdirectory,
            tmp_folder=tmp_folder,
            md5=target['md5'],
            verbose=verbose
        )
        return _unpack(
            to_unpack=downloaded,
            target_file=to_file,
            verbose=verbose,
            extension=target['extension']
        )
    except (HTTPError, URLError):
        raise ValueError(f'Unable to download pre-built index at {target["url"]}.')
    finally:
        #  Remove temporary folder and temporary file
        tmp_folder = f"{target['filename'][:-len(target['extension'])]}.{target['md5']}"
        os.remove(
            os.path.join(
                get_cache_home(),
                subdirectory,
                tmp_folder,
                target['filename']
            )
        )
        os.rmdir(
            os.path.join(
                get_cache_home(),
                subdirectory,
                tmp_folder
            )
        )


def _download(url, target_filename, subdirectory, tmp_folder, md5, verbose):
    # Create directory where to copy data to
    to_folder = os.path.join(get_cache_home(), subdirectory, tmp_folder)

    if not os.path.exists(to_folder):
        os.makedirs(to_folder)

    to_file = os.path.join(to_folder, target_filename)

    # If there's a local file, it's likely corrupted, because we remove the local file on success.
    # So, we want to remove.
    if os.path.exists(to_file):
        os.remove(to_file)

    print(f'Downloading data at {url}...')
    return download_url(url, to_folder, local_filename=target_filename, verbose=verbose, md5=md5)


def download_url(url, save_dir, local_filename=None, md5=None, force=False, verbose=True):
    # If caller does not specify local filename, figure it out from the download URL:
    if not local_filename:
        filename = url.split('/')[-1]
        filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter
    else:
        # Otherwise, use the specified local_filename:
        filename = local_filename

    destination_path = os.path.join(save_dir, filename)

    if verbose:
        print(f'Downloading {url} to {destination_path}...')

    if os.path.exists(destination_path):
        if verbose:
            print(f'{destination_path} already exists!')
        if not force:
            if verbose:
                print(f'Skipping download.')
            return destination_path
        if verbose:
            print(f'force=True, removing {destination_path}; fetching fresh copy...')
        os.remove(destination_path)

    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        urlretrieve(url, filename=destination_path, reporthook=t.update_to)

    if md5:
        md5_computed = compute_md5(destination_path)
        assert md5_computed == md5, f'{destination_path} does not match checksum! Expecting {md5} got {md5_computed}.'

    return destination_path


def _unpack(to_unpack, target_file, verbose, extension):
    if verbose:
        print(f'Unpacking {to_unpack} to {target_file}...')
    if extension == '.tar.bz2':
        try:
            with bz2.open(to_unpack, 'rb') as read, open(target_file + '.tar', 'wb') as write:
                write.write(read.read())
            with tarfile.open(target_file + '.tar', 'rb') as read:
                read.extractall(target_file)
        finally:
            os.remove(target_file + '.tar')
    elif extension == '.gz':
        with gzip.open(to_unpack, 'rb') as read, open(target_file, 'wb') as write:
            write.write(read.read())
    elif extension == '.tar':
        try:
            with tarfile.open(to_unpack, 'rb') as read:
                read.extractall(target_file)
        finally:
            os.remove(to_unpack)
    else:
        raise ValueError("Extension not recognized.")
    return target_file
