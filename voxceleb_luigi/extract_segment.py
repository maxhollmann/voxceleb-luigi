import luigi
from pathlib import Path
from collections import namedtuple

from .util import ensure_path, Config, check_output
from .soft_failure import softly_failing

from .download_audio import DownloadAudio
from .ffmpeg import FFmpeg
from .atomized_local_target import AtomizedLocalTarget


Segment = namedtuple(
    'Segment',
    ('person', 'video', 'id', 'start', 'stop'))


@softly_failing(propagate=True)
class ExtractSegment(luigi.Task):
    task_namespace = 'voxceleb'

    priority = 1000

    segment_file = luigi.Parameter()
    base_path = luigi.Parameter()

    def requires(self):
        return DownloadAudio(video=self._segment.video)

    def output(self):
        output_dir = Config().output_dir

        path = Path(self.segment_file).relative_to(self.base_path)
        parts = list(path.parts)
        try:
            txt_index = parts.index('txt')
        except ValueError:
            raise RuntimeError(
                "No output_dir specified and no parent "
                f"directory called 'txt' in '{path}'.")

        if output_dir:
            del parts[txt_index]
            path = Path(output_dir, *parts)
        else:
            parts[txt_index] = "wav"
            path = Path(self.base_path, *parts)

        path = path.with_suffix('.wav')
        return luigi.LocalTarget(str(ensure_path(path)))

    def run(self):
        ffmpeg = FFmpeg(ffmpeg_bin=Config().ffmpeg_bin)
        with AtomizedLocalTarget(self.output()) as target:
            ffmpeg.extract_segment(
                self.input().path, str(target.path),
                start=self._segment.start, stop=self._segment.stop,
                timeout=300)
        check_output(self.output().path)


    @property
    def _segment(self):
        if self.__cached_segment is None:
            self.__cached_segment = _parse_segment_file(self.segment_file)
        return self.__cached_segment
    __cached_segment = None



def _parse_segment_file(path):
    path = Path(path)

    with path.open('r') as f:
        segment_desc = f.read().strip()

    header, frames = segment_desc.split("\n\n")
    header = _parse_header(header)
    start, stop = _get_segment_boundaries(frames)

    return Segment(
        person=header['Identity'],
        video=header['Reference'],
        id=path.stem,
        start=start,
        stop=stop,
    )

def _parse_header(header):
    def _parse_line(line):
        k, v = line.split("\t")
        k = k[:-2].strip() # remove '\s*: ' from end
        v = v.strip()
        return k, v
    return dict(_parse_line(line) for line in header.split("\n"))

def _get_segment_boundaries(frames):
    def _get_frame_seconds(line):
        frame = int(line.split("\t")[0])
        return frame / 25 # frame index to sec (25fps)
    lines = frames.split("\n")
    return _get_frame_seconds(lines[1]), _get_frame_seconds(lines[-1])
