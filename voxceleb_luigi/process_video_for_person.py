import luigi
import luigi.util

from .util import data_out_path, Config

from .extract_data import ExtractData
from .extract_segment import ExtractSegment
from .download_audio import DownloadAudio

from pathlib import Path
import re


@luigi.util.requires(ExtractData)
class ProcessVideoForPerson(luigi.Task):
    task_namespace = 'voxceleb'

    priority = 2

    person = luigi.Parameter()
    video = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(
            data_out_path('processed', 'ProcessVideoForPerson',
                          'video_{}_for_{}.dummy'.format(self.video, self.person)))

    def run(self):
        segments = self._get_segments()
        segment_tasks = [ExtractSegment(person=self.person, video=self.video,
                                        segment=int(seg), start=float(start), stop=float(stop))
                         for seg, start, stop in segments]

        yield segment_tasks

        # No need for the original video anymore
        audio = DownloadAudio(video=self.video)
        try:
            Path(audio.output().path).unlink()
        except OSError:
            pass

        with self.output().open("w") as f:
            f.write("done")


    def _get_segments(self):
        if Config().dataset == 1:
            video_file = Path(self.input().path, self.person, self.video).with_suffix('.txt')
            with video_file.open('r') as f:
                video_desc = f.read()

            matches = re.findall("_(\d+)\s+([\d.]+)\s+([\d.]+)", video_desc)
            return matches

        else:
            video_dir = Path(self.input().path, self.person, self.video)
            segment_files = video_dir.glob("*.txt")

            segments = []
            for segment_file in segment_files:
                segment = int(segment_file.stem)
                with segment_file.open('r') as f:
                    segment_desc = f.read().strip()

                lines = segment_desc.split("\n")
                lines = [lines[5], lines[-1]]
                frames = [int(l.split(' ', maxsplit=1)[0]) for l in lines]
                start, stop = tuple(frame / 25 for frame in frames) # frame no (25fps) to sec
                segments.append((segment, start, stop))

            return segments
