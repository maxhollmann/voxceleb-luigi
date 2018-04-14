# voxceleb-luigi
[![pypi version](http://img.shields.io/pypi/v/voxceleb_luigi.svg?style=flat)](https://pypi.python.org/pypi/voxceleb_luigi)

Luigi pipeline to download VoxCeleb audio from YouTube and extract speaker segments.

This pipeline can download both the original [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/) and [VoxCeleb2](http://www.robots.ox.ac.uk/~vgg/data/voxceleb2/).

## Installation

    pip install voxceleb_luigi

You need to have `ffmpeg` and `youtube-dl` installed. On systems with `apt`, you can simply run:

    sudo apt install ffmpeg youtube-dl


## Usage

Some configuration is necessary, the easiest way is to put it in your `luigi.cfg` (default location is the current working directory; you can override this by setting the `LUIGI_CONFIG_PATH` environment variable).

    [voxceleb.Config]
    # Necessary, otherwise the pipeline will try to save data to /
    data_out_dir=/path/to/voxceleb

    # Only necessary if youtube-dl, ffmpeg, and ffprobe are not in your PATH:
    ffmpeg_bin=/ffmpeg-dir/ffmpeg
    ffmpeg_directory=/ffmpeg-dir
    youtube_dl_bin=/path/to/youtube-dl

    # 1 for VoxCeleb, 2 for VoxCeleb2 (default)
    dataset=2


To run the pipeline, first start luigid:

    luigid --background

and then start the workers:

    luigi --module voxceleb_luigi --workers 5 voxceleb.ProcessPeople
