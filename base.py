import logging
import os

from mutagen.easyid3 import EasyID3

log = logging.getLogger(__name__)


class Base:

    tags = set(('title', 'artist', 'album', 'tracknumber' 'composer', 'comment', 'comment_other'))

    def __init__(self, write_to_file=False):
        self.write_to_file = write_to_file

    def list_tag_values(self, files, tag):
        values = set()
        for file in files:
            file = EasyID3(file)
            if tag in file:
                for tag_value in file[tag]:
                    values.add(tag_value)
        log.info(f"`{tag}` values : ")
        for value in sorted(values):
            log.info(f"    {value}")

    def update_file_tag(self, filename, tag, old_value, new_value):
        file = EasyID3(filename)
        tags = file[tag]
        for i, tag_values in enumerate(tags):
            if tag_values == old_value:
                log.info(f"Updating {os.path.basename(filename)} tag {tag} `{old_value}`->`{new_value}`")
                tags[i] = new_value
        file[tag] = tags
        if self.write_to_file:
            file.save()

    def process(*args, **kwargs):
        raise NotImplementedError(f"{self.__name__} need to override process method")
