import unittest
from pyroaring import BitMap
from array import array
from src.TagsManager import TagsManager


class TestTagsManager(unittest.TestCase):
    @staticmethod
    def create_empty_tag_list():
        """
        Creates an empty tag list, for tag1, tag2, ...tag10
        """
        tags = {}
        for tag in TagsManager.TAG_KEYS:
            tags[tag] = BitMap()
        return tags

    def setUp(self) -> None:
        self.tags = TestTagsManager.create_empty_tag_list()
        self.tagsm = TagsManager(self.tags)

    def test_countUsers_havingBothTags_returnsPositiveNumber(self):
        self.tagsm.add_tags(1, ['tag1', 'tag2'])
        self.tagsm.add_tags(2, ['tag1', 'tag2', 'tag3'])
        self.tagsm.add_tags(3, ['tag5'])
        self.tagsm.add_tags(4, ['tag1'])
        self.assertEqual(2, self.tagsm.count_users_with_tags('tag1', 'tag2'))

    def test_countUsers_notHavingBothTags_returnsZero(self):
        self.tagsm.add_tags(1, ['tag1', 'tag4'])
        self.tagsm.add_tags(2, ['tag2', 'tag3'])
        self.tagsm.add_tags(3, ['tag3', 'tag1'])
        self.tagsm.add_tags(4, ['tag1'])
        self.assertEqual(0, self.tagsm.count_users_with_tags('tag1', 'tag2'))

    def test_getUsers_havingSearchTag_returnsNonEmptyArrayOfUsers(self):
        self.tagsm.add_tags(1, ['tag1', 'tag2'])
        self.tagsm.add_tags(2, ['tag1', 'tag2', 'tag3'])
        self.tagsm.add_tags(3, ['tag5'])
        self.tagsm.add_tags(4, ['tag1'])
        self.assertEqual(array('I', [1, 2, 4]), self.tagsm.get_users_with_tag('tag1'))

    def test_getUsers_notHavingSearchTag_returnsEmptyArrayOfUsers(self):
        self.tagsm.add_tags(1, ['tag1', 'tag2'])
        self.tagsm.add_tags(2, ['tag1', 'tag2', 'tag3'])
        self.assertEqual(array('I', []), self.tagsm.get_users_with_tag('tag4'))
