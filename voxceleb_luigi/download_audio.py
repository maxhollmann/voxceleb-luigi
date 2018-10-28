import luigi

from .util import pipeline_path, Config, check_output
from .soft_failure import softly_failing
from .atomized_local_target import AtomizedLocalTarget

import subprocess
import re


@softly_failing()
class DownloadAudio(luigi.Task):
    task_namespace = 'voxceleb'

    priority = 1000

    video = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(
            pipeline_path('DownloadAudio', '{}.wav'.format(self.video)))

    def run(self):
        with AtomizedLocalTarget(self.output()) as target:
            cmd = [Config().youtube_dl_bin,
                   "--extract-audio",
                   "--audio-format", "wav",
                   "--audio-quality", "1",
                   "--output", str(target.path)]

            if Config().ffmpeg_directory:
                cmd += ["--ffmpeg-location", Config().ffmpeg_directory]

            cmd += [self.video]

            run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if run.returncode != 0:
                target.fail()
                error = run.stderr.decode("utf-8")
                if re.search("YouTube said:", error):
                    self.fail_softly(error)
                    return
                else:
                    raise RuntimeError("youtube-dl failed:\n\n{}\n\n{}".format(
                        run.stdout.decode("utf-8"),
                        run.stderr.decode("utf-8")
                    ))

        check_output(self.output().path)
