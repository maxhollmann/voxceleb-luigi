import luigi
import luigi.util

from .util import data_out_path, Config

from .extract_data import ExtractData
from .process_video_for_person import ProcessVideoForPerson

from pathlib import Path


@luigi.util.requires(ExtractData)
class ProcessPerson(luigi.Task):
    task_namespace = 'voxceleb'

    priority = 1

    person = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(
            data_out_path('processed', 'ProcessPerson',
                          'person_{}.dummy'.format(self.person)))

    def run(self):
        person_path = Path(self.input().path, self.person)
        videos = [p.stem for p in person_path.iterdir()]

        video_tasks = [ProcessVideoForPerson(person=self.person, video=v) for v in videos]
        yield video_tasks

        with self.output().open("w") as f:
            f.write("done")
