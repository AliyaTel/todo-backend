import json
import os

grocery_list = {
    "title": "Продукты",
    "entries": [
        {
            "title": "Молочные",
            "entries": [
                {
                    "title": "Йогурт",
                    "entries": []
                },
                {
                    "title": "Сыр",
                    "entries": []
                }
            ]
        }
    ]
}


def print_with_indent(value, indent=0):
    indention = ''
    for i in range(indent):
        indention += '\t'
    print(indention + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            self.entries = []
        self.title = title
        self.parent = parent

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def json(self):
        res = {
            'title': self.title,
            'entries': [x.json() for x in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, grocery_list1: dict):
        new_entry = cls(grocery_list1['title'])
        for item in grocery_list1.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        new_file = os.path.join(path, f'{self.title}.json')
        with open(new_file, 'w') as file:
            json.dump(self.json(), file)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            content = json.load(file)
            return cls.from_json(content)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for i in self.entries:
            i.save(self.data_path)

    def load(self):
        if not os.listdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self



