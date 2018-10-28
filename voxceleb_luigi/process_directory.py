import luigi
import luigi.util
from pathlib import Path
import re

from .util import pipeline_path, Config, sanitize_filename
from .extract_segment import ExtractSegment


class ProcessDirectory(luigi.Task):
    task_namespace = 'voxceleb'

    resources = {'process_directory': 1}

    path = luigi.Parameter()
    base_path = luigi.Parameter(default=None)
    depth = luigi.IntParameter(default=0)

    @property
    def priority(self):
        return self.depth

    def output(self):
        return luigi.LocalTarget(
            pipeline_path(
                'ProcessDirectory',
                f'{sanitize_filename(self.path)}.done'))

    def run(self):
        path = Path(self.path)

        subdirs = [p for p in path.iterdir() if p.is_dir()]
        subdir_tasks = [
            ProcessDirectory(
                path=str(subdir),
                base_path=self.base_path or self.path,
                depth=self.depth + 1)
            for subdir in subdirs]
        yield subdir_tasks

        seg_files = [p for p in _segment_files(path.iterdir())]
        segment_tasks = [
            ExtractSegment(
                segment_file=str(file),
                base_path=self.base_path or self.path)
            for file in seg_files]
        yield segment_tasks

        with self.output().open("w") as f:
            f.write("done")


def _segment_files(paths):
    pattern = re.compile(r'\d+\.txt')

    for path in paths:
        if not path.is_file(): continue
        if not pattern.match(path.name): continue
        yield path
