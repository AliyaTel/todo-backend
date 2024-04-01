from typing import List
from resources import Entry
import os


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for i in self.entries:
            new_path = os.path.join(self.data_path, i['title'])
            Entry.save(path=new_path)

