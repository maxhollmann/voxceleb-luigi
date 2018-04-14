import luigi

from .util import data_out_path, Config, check_output
from .soft_failure import softly_failing

from .download_audio import DownloadAudio
from .ffmpeg import FFmpeg
from .atomized_local_target import AtomizedLocalTarget


@softly_failing(propagate=True)
class ExtractSegment(luigi.Task):
    task_namespace = 'voxceleb'

    priority = 3

    person = luigi.Parameter()
    video = luigi.Parameter()
    segment = luigi.IntParameter()
    start = luigi.FloatParameter()
    stop = luigi.FloatParameter()

    def requires(self):
        return DownloadAudio(video=self.video)

    def output(self):
        return luigi.LocalTarget(
            data_out_path('segments', 'original', self.person,
                          '{}_{:07d}.wav'.format(self.video, int(self.segment))))

    def run(self):
        ffmpeg = FFmpeg(ffmpeg_bin=Config().ffmpeg_bin)
        with AtomizedLocalTarget(self.output()) as target:
            ffmpeg.extract_segment(
                self.input().path, str(target.path),
                start=self.start, stop=self.stop,
                timeout=300)
        check_output(self.output().path)
