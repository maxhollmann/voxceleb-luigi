import luigi
import luigi.util

from .util import data_out_path, check_output, Config

from .download_data import DownloadData

from pathlib import Path
import shutil
import subprocess


@luigi.util.requires(DownloadData)
class ExtractData(luigi.Task):
    task_namespace = 'voxceleb'

    def output(self):
        if Config().dataset == 1:
            return luigi.LocalTarget(data_out_path('data', 'voxceleb1_txt'))
        else:
            return luigi.LocalTarget(data_out_path('data', 'all'))

    def run(self):
        out_dir = Path(self.output().path).parent

        run = subprocess.run(
            ["unzip", "-o",
             self.input().path,
             "-d", str(out_dir)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if run.returncode != 0:
            raise RuntimeError("unzip failed:\n\n{}\n\n{}".format(
                run.stderr.decode("utf-8")
            ))


        if Config().dataset == 2:
            (out_dir / 'all').mkdir(parents=True)

            for set in ('test', 'dev'):
                for person_dir in (out_dir / set / 'txt').iterdir():
                    print(f"Moving {set}/{person_dir.name}")
                    person_dir.rename(out_dir / 'all' / person_dir.name)

                print(f"Deleting {set}")
                shutil.rmtree(out_dir / set, ignore_errors=True)

        check_output(self.output().path, check_file=False, check_size=False)
