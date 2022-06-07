import unittest
from copy import deepcopy

from case import Case


class TestCase(unittest.TestCase):

    def test_get_main_case(self):
        case = Case()
        case.casing_dict = {
            'album': {
                'lower_album': {
                    'lower_album': ['file_0.mp3', 'file_1.mp3', 'file_2.mp3'],
                    'Lower_album': ['file_3.mp3'],
                    'LOWER_Album': ['file_4.mp3', 'file_5.mp3']
                },
                'other_album': {
                    'Other_Album': ['file_6.mp3']
                }
            },
            'artist': {
                'solid': {
                    'solid': ['file_0.mp3']
                }
            }
        }
        self. assertEqual(case.get_tag_main_case('album', 'lower_album'), 'lower_album')
        self. assertEqual(case.get_tag_main_case('album', 'other_album'), 'Other_Album')
        self. assertEqual(case.get_tag_main_case('artist', 'solid'), 'solid')
        with self.assertRaises(KeyError):
            case.get_tag_main_case('artist', 'missing')


if __name__ == '__main__':
    unittest.main()
