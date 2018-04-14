import luigi
import luigi.util

from pathlib import Path

from hashlib import blake2s

from .util import data_out_path, Config

from .extract_data import ExtractData
from .process_person import ProcessPerson


@luigi.util.requires(ExtractData)
class ProcessPeople(luigi.Task):
    task_namespace = 'voxceleb'

    max_people = luigi.IntParameter(default=99999)

    def output(self):
        return luigi.LocalTarget(
            data_out_path('processed', 'ProcessPeople',
                          'max_people_{}.dummy'.format(self.max_people)))

    def run(self):
        people = self._get_people()
        people = people[:self.max_people]

        people_tasks = [ProcessPerson(person=p) for p in people]
        yield people_tasks

        with self.output().open("w") as f:
            f.write("done")


    def _get_people(self):
        people = [p.name for p in Path(self.input().path).iterdir()]
        people.sort(key=_stable_hash)
        return people



def _stable_hash(x):
    b = x.encode()
    h = blake2s()
    h.update(b)
    return h.hexdigest()
