from . import author
class GoodreadsBook:
    def __init__(self, book_dict, client):
        self._book_dict = book_dict
        self._client = client

    def __repr__(self):
        return self.title

    @property
    def gid(self):
        return self._book_dict['id']

    @property
    def title(self):
        return self._book_dict['title']

    @property
    def authors(self):
        if type(self._book_dict['authors']['author']) == list:
            return [author.GoodreadsAuthor(author_dict, self._client)
                    for author_dict in self._book_dict['authors']['author']]
        else:
            return [author.GoodreadsAuthor(self._book_dict['authors']['author'],
                                           self._client)]

    @property
    def description(self):
        return self._book_dict['description']

    @property
    def average_rating(self):
        return self._book_dict['average_rating']

    @property
    def num_pages(self):
        return self._book_dict['num_pages']

    @property
    def publication_date(self):
        return (self._book_dict['publication_month'],
                self._book_dict['publication_day'],
                self._book_dict['publication_year'])

