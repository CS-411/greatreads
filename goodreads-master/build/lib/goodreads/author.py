class GoodreadsAuthor:
    def __init__(self, author_dict, client):
        self._author_dict = author_dict
        self._client = client

    def __repr__(self):
        return self.name

    @property
    def name(self):
        return self._author_dict['name']

    @property
    def works_count(self):
        return self._author_dict['works_count']
