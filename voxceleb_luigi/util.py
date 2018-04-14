import luigi
import os
import shutil


class Config(luigi.Config):
    task_namespace = 'voxceleb'

    ffmpeg_bin = luigi.Parameter(default='ffmpeg')
    ffmpeg_directory = luigi.Parameter(default='')
    youtube_dl_bin = luigi.Parameter(default='youtube-dl')

    data_out_dir = luigi.Parameter()

    dataset = luigi.IntParameter(default=2)


def data_out_path(*path):
    path = os.path.join(Config().data_out_dir, *path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def check_output(path, check_exists=True, check_file=True, check_size=True):
    errors = []
    if check_exists and not os.path.exists(path):
        errors.append("doesn't exist")
    if check_file and not os.path.isfile(path):
        errors.append("is not a file")
    if check_size and os.path.getsize(path) == 0:
        errors.append("is empty")

    if errors:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

        raise RuntimeError("{} {}".format(path, ", ".join(errors)))
