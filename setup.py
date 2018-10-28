from setuptools import setup
from pathlib import Path


# Get the long description from the README file
with (Path(__file__).resolve().parent / 'README.md').open(encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='voxceleb_luigi',
    version='0.2.0',
    description='Luigi pipeline to download VoxCeleb audio from YouTube and extract speaker segments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/maxhollmann/voxceleb-luigi',
    author='Max Hollmann',
    license='MIT',
    packages=['voxceleb_luigi'],
    zip_safe=False,
    classifiers=[ # https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
    ],
    install_requires=['luigi'],
)
