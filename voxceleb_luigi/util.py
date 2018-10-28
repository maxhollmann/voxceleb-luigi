import luigi
from pathlib import Path
import shutil
from hashlib import blake2s
import re


class Config(luigi.Config):
    task_namespace = 'voxceleb'

    ffmpeg_bin = luigi.Parameter(default='ffmpeg')
    ffmpeg_directory = luigi.Parameter(default='')
    youtube_dl_bin = luigi.Parameter(default='youtube-dl')

    output_dir = luigi.Parameter(default=None)
    pipeline_dir = luigi.Parameter(default='voxceleb-luigi-files')


def ensure_path(path):
    path = Path(path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def output_path(*path):
    return str(ensure_path(Path(Config().output_dir, *path)))

def pipeline_path(*path):
    return str(ensure_path(Path(Config().pipeline_dir, *path)))



def sanitize_filename(s):
    return re.sub(r'(?u)[^-\w.]', '_', s)

def stable_hash(x):
    b = x.encode()
    h = blake2s()
    h.update(b)
    return h.hexdigest()


def check_output(path, check_exists=True, check_file=True, check_size=True):
    path = Path(path)
    errors = []
    if check_exists and not path.exists():
        errors.append("doesn't exist")
    if check_file and not path.is_file():
        errors.append("is not a file")
    if check_size and path.lstat().st_size == 0:
        errors.append("is empty")

    if errors:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

        raise RuntimeError("{} {}".format(path, ", ".join(errors)))
