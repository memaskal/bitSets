from typing import Dict, List
from pyroaring import BitMap
from array import array


class TagsManager:
    TAG_KEYS = {'tag' + str(i) for i in range(1, 11)}

    def __init__(self, tags: Dict[str, BitMap]):
        self.tags = tags

    def add_tags(self, user_id: int, tags: List[str]):
        for tag_id in tags:
            self.tags[tag_id].add(user_id)

    def count_users_with_tags(self, tag_id1: str, tag_id2: str) -> int:
        return self.tags[tag_id1].intersection_cardinality(self.tags[tag_id2])

    def get_users_with_tag(self, tag_id: str) -> array:
        return self.tags[tag_id].to_array()
