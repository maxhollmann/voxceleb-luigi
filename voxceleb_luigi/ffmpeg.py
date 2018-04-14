import subprocess
import os


class FFmpeg:
    def __init__(self, ffmpeg_bin='ffmpeg'):
        self.ffmpeg_bin = ffmpeg_bin

    def extract_segment(self, source, destination, start, stop, timeout=None):
        args = ["-i", source,
                "-ss", str(start),
                "-to", str(stop),
                "-f", "wav", destination]
        self._run_ffmpeg(args, destination=destination, timeout=timeout)


    def _run_ffmpeg(self, args, destination=None, timeout=None):
        cmd = [self.ffmpeg_bin, "-y"] + args

        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                if proc.returncode != 0:
                    raise RuntimeError("ffmpeg failed:\n\n{}".format(stderr.decode("utf-8")))
            except subprocess.TimeoutExpired as e:
                if destination:
                    try:
                        os.remove(destination)
                    except OSError:
                        pass
                raise

        return stdout, stderr
