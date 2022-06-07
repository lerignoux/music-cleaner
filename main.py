import argparse
import logging
import os
from pathlib import Path
import sys

from base import Base
from case import Case
from popularity import Popularity

log = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


parser = argparse.ArgumentParser(description='Scripts to clean my music files.')
parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode')
parser.add_argument('--write-to-file', '-w', action='store_true', default=False,
                    help='Write changes to file.')
parser.add_argument('--folder', '-f', default='./',
                    help='folder containing the music files.')
parser.add_argument('--case', '-c', action='store_true',
                    help='Clean tags casing using the most common one.')
parser.add_argument('--list-popularities', action='store_true',
                    help='list popularities emails')
parser.add_argument('--tag-values', '-t',
                    help='list values of this tag')
parser.add_argument('--popularity', '-p',
                    help='Remove popularities not matching this email')
parser.add_argument('--url', '-u',
                    help='Remove urls from tags')




class AudioFiles:
    def __init__(self, folder="./", extension="mp3"):
        self.filenames = []
        for path in Path(folder).rglob(f'*.{extension}'):
            self.filenames.append(path.absolute())
        log.debug(f"{len(self.filenames)} files found.")
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.filenames):
            raise StopIteration
        return self.filenames[self.index]

if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    files = AudioFiles(args.folder)

    if args.tag_values:
        Base(args.write_to_file).list_tag_values(files, args.tag_values)

    if args.case:
        Case(args.write_to_file).process(files)

    if args.list_popularities:
        Popularity(args.write_to_file).list(files)

    if args.popularity:
        Popularity(args.write_to_file).process(files, [args.popularity])
