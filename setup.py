from setuptools import setup
from pathlib import Path


# Get the long description from the README file
with (Path(__file__).resolve().parent / 'README.md').open(encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='voxceleb_luigi',
    version='0.1.2',
    description='Luigi pipeline to download VoxCeleb audio from YouTube and extract speaker segments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/maxhollmann/voxceleb-luigi',
    author='Max Hollmann',
    license='MIT',
    packages=['voxceleb_luigi'],
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['luigi'],
)
