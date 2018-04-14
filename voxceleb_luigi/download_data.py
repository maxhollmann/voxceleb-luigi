import luigi

from .util import data_out_path, check_output, Config
from .atomized_local_target import AtomizedLocalTarget

import subprocess


class DownloadData(luigi.Task):
    task_namespace = 'voxceleb'

    voxceleb1_url = luigi.Parameter(default="http://www.robots.ox.ac.uk/~vgg/data/voxceleb/voxceleb1.zip")
    voxceleb2_url = luigi.Parameter(default="http://www.robots.ox.ac.uk/~vgg/data/voxceleb2/vox2_txt.zip")

    def output(self):
        return luigi.LocalTarget(data_out_path('data', 'data.zip'))

    def run(self):
        if Config().dataset == 1:
            url = self.voxceleb1_url
        else:
            url = self.voxceleb2_url

        with AtomizedLocalTarget(self.output()) as target:
            run = subprocess.run(
                ["curl", "-L", "-o", str(target.path), url],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            if run.returncode != 0:
                target.fail()
                raise RuntimeError("curl failed:\n\n{}\n\n{}".format(
                    run.stdout.decode("utf-8"),
                    run.stderr.decode("utf-8")
                ))

        check_output(self.output().path)
