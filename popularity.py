import logging
import re

from base import Base
from mutagen.id3 import ID3

log = logging.getLogger(__name__)


class Popularity(Base):

    tag_re = 'POPM:.*'

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def valid_popularities(self, whitelist):
        result = []
        for email in whitelist:
            result.append(f"POPM:{email}")
        return result

    def process(self, files, whitelist):
        """
        remove popularities not matching the given emails
        """
        good_frames = self.valid_popularities(whitelist)
        for file in files:
            file = ID3(file)
            for frame in list(file.keys()):
                if re.match(self.tag_re, frame):
                    if frame not in good_frames:
                        del file[frame]
                        if self.write_to_file:
                            file.save()


    def list(self, files):
        for file in files:
            file = ID3(file)
            for frame in file.keys():
                if re.match(self.tag_re, frame):
                    print(frame)
