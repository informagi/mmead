import bz2
import gzip
import hashlib
import os
import re
import tarfile
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

from tqdm import tqdm

from .download_info import EMBEDDING_INFO, LINK_INFO, MAPPING_INFO


def get_cache_home():
    custom_dir = os.environ.get("MMEAD_CACHE")
    if custom_dir is not None and custom_dir != '':
        return custom_dir
    return os.path.expanduser(os.path.join(f'~{os.path.sep}.cache', "mmead"))


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
def _compute_md5(file, block_size=2**20):
    m = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def download_and_unpack(name, force=False, verbose=True):
    if name not in EMBEDDING_INFO and name not in LINK_INFO and name not in MAPPING_INFO:
        raise ValueError(f'Unrecognized data file: {name}')
    if name in EMBEDDING_INFO:
        info = EMBEDDING_INFO
    elif name in LINK_INFO:
        info = LINK_INFO
    else:
        info = MAPPING_INFO
    target = info[name]
    subdirectory = info['_folder']
    try:
        to_file = os.path.join(get_cache_home(), subdirectory, target['to_file'])
    except KeyError:
        to_file = os.path.join(get_cache_home(), subdirectory, f"{target['filename'][:-len(target['extension'])]}")

    # If file already exists, and if not force we can skip
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
    except (HTTPError, URLError):
        raise ValueError(f'Unable to download file at {target["url"]}.')
    try:
        return _unpack(
            to_unpack=downloaded,
            target_file=to_file,
            verbose=verbose,
            extension=target['extension'],
            subdirectory=subdirectory,
            to_file=target['to_file'],  # slightly confusing with other parameter, fix later
            version=target['version']
        )
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


def download_url(url, save_dir, local_filename=None, md5=None, verbose=True):
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

    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        urlretrieve(url, filename=destination_path, reporthook=t.update_to)

    if md5:
        md5_computed = _compute_md5(destination_path)
        assert md5_computed == md5, f'{destination_path} does not match checksum! Expecting {md5} got {md5_computed}.'

    return destination_path


def _is_within_directory(directory, target):
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    prefix = os.path.commonprefix([abs_directory, abs_target])
    return prefix == abs_directory


def _safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not _is_within_directory(path, member_path):
            raise Exception("Attempted Path Traversal in Tar File")
    tar.extractall(path, members, numeric_owner=numeric_owner)


def _unpack(to_unpack, target_file, verbose, extension, subdirectory, to_file, version):
    if verbose:
        print(f'Unpacking {to_unpack} to {target_file}...')
    if extension == '.tar.bz2':
        tmp_file = to_unpack[:-4]
        try:
            if verbose:
                print("Unpacking data, this can take a while...")
            with bz2.open(to_unpack, 'rb') as infile, open(tmp_file, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)
            with tarfile.open(tmp_file, 'r') as infile:
                _safe_extract(infile, os.path.join(get_cache_home(), subdirectory))
            os.rename(os.path.join(get_cache_home(), subdirectory, version, to_file), target_file)
            os.rmdir(os.path.join(get_cache_home(), subdirectory, version))
        finally:
            os.remove(tmp_file)
    elif extension == '.gz':
        if verbose:
            print("Unpacking data, this can take a while...")
        with gzip.open(to_unpack, 'rb') as infile, open(target_file, 'wb') as out:
            for line in infile:
                out.write(line)
    elif extension == '.tar':
        with tarfile.open(to_unpack, 'r') as read:
            _safe_extract(read, os.path.join(get_cache_home(), subdirectory))
    else:
        raise ValueError("Extension not recognized.")
    if verbose:
        print(f'Unpacking completed...')
    return target_file
