# voxceleb-luigi
[![pypi version](http://img.shields.io/pypi/v/voxceleb_luigi.svg?style=flat)](https://pypi.python.org/pypi/voxceleb_luigi)

Luigi pipeline to download VoxCeleb audio from YouTube and extract speaker segments.

This pipeline can download both [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html) and [VoxCeleb2](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html).

## Installation

    pip install voxceleb_luigi

You need to have `ffmpeg` and `youtube-dl` installed. On systems with `apt`, you can simply run:

    sudo apt install ffmpeg youtube-dl


## Usage

Download and unpack at least one of the metadata directories with the YouTube URLs and timestamps (VC1 [dev](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/data/vox1_dev_txt.zip)/[test](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/data/vox1_test_txt.zip), VC2 [dev](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/data/vox2_dev_txt.zip)/[test](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/data/vox2_test_txt.zip)).

Start luigid, the central scheduler:

    luigid --background

Then start the worker process:

    luigi --module voxceleb_luigi \
        --workers 4 \
        voxceleb.ProcessDirectory \
        --path /path/to/metadata

The pipeline will recursively search `/path/to/metadata` for the segment files (by looking for files called like `00001.txt` etc.), download the audio of their source videos, and extract the speaker segments.

By default, the segment audio files are stored in parallel to the metadata in directories called `wav` that get created next to the `txt` directories. Suppose you have the metadata of the dev and test sets of VoxCeleb1 in `~/vc1` with paths looking like `~/vc1/dev/txt/idX/videoX/XXXXX.txt`. If you pass `--path ~/vc1` to the pipeline, segments will end up in `~/vc1/dev/wav/idX/videoX/XXXXX.wav`. Other output of the pipeline (full audio of videos, soft failures, dummy outputs for completed directories) are stored in `./voxceleb-luigi-files` by default.


## Configuration

Both the location where the dataset gets created and the storage directory for the pipeline can be changed through parameters in the `luigi.cfg` (default location is the current working directory; you can override this via the `LUIGI_CONFIG_PATH` environment variable):

    [voxceleb.Config]
    # Required
    output_dir=/where/to/store/wav/segments
    pipeline_dir=/where/to/put/pipeline/stuff

    ## Only necessary if youtube-dl, ffmpeg, and ffprobe are not in your PATH:
    #ffmpeg_bin=/ffmpeg-dir/ffmpeg
    #ffmpeg_directory=/ffmpeg-dir # passed on to youtube-dl via --ffmpeg-location
    #youtube_dl_bin=/path/to/youtube-dl

    [voxceleb.ProcessDirectory]
    ## alternative to the --path command line option
    #path=/path/to/metadata

When `output_dir` is set, the directory structure of the metadata is mirrored in this directory. In this case, the `txt` directories are not replaced by `wav`, but removed from the path.
