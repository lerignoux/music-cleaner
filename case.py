import logging
from copy import copy
from mutagen.easyid3 import EasyID3

from base import Base


log = logging.getLogger(__name__)

class Case(Base):

    def __init__(self, *args, **kwargs):
        """
        casing_dict: {
            album: {
                testalbum: {
                    TestAlbum: [File1.mp3, File3.mp3]
                    testalbum: [File2.mp3]
                }
            }
        }
        """
        super().__init__(self, *args, **kwargs)
        self.casing_dict = {tag: {} for tag in self.tags}

    def get_tag_main_case(self, tag, tag_id):
        max_count = 0
        main_tag = None
        for tag_case, files in self.casing_dict[tag][tag_id].items():
                if len(files) > max_count:
                    max_count = len(files)
                    main_tag = tag_case
        return main_tag

    def add_tag_case_record(self, filename, tag, value):
        tag_id = value.lower()
        if tag_id not in self.casing_dict[tag]:
            self.casing_dict[tag][tag_id] = {}
        if value not in self.casing_dict[tag][tag_id]:
            self.casing_dict[tag][tag_id][value] = []
        self.casing_dict[tag][tag_id][value].append(filename)

    def process(self, files):
        files = [EasyID3(file) for file in files]

        log.info("Building tag casing records")
        for file in files:
            for tag in self.tags:
                file_tags = file.get(tag, [])
                for file_tag in file_tags:
                    self.add_tag_case_record(file.filename, tag, file_tag)

        log.info("Cleaning wrong case records")
        for file in files:
            self.cleanup_tags(file)

    def cleanup_tags(self, file):
        for tag in self.tags:
            file_tags = file.get(tag, [])
            for file_tag in file_tags:
                self.cleanup_tag(file, tag)

    def cleanup_tag(self, file, tag):
        for index, value in enumerate(copy(file[tag])):
            main_tag = self.get_tag_main_case(tag, value.lower())
            if value != main_tag:
                self.update_file_tag(file.filename, tag, value, main_tag)
