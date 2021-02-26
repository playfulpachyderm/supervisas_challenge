import random
import string

from django.db import models

ALNUM_CHARS = string.digits + string.ascii_letters

def get_short_url(length=10):
    """Just a random string, since it can't mean anything (user can choose their own"""
    return "".join(random.choice(ALNUM_CHARS) for i in range(length))

class ShortUrl(models.Model):
    """A shortened URL"""
    long_url = models.CharField(max_length=500)
    short_id = models.CharField(max_length=20)

    @classmethod
    def get_short_for(cls, long_url):
        """Factory method for shortening a given URL"""
        existing = ShortUrl.objects.filter(long_url=long_url)
        if existing:
            return existing[0]
        return cls(long_url=long_url, short_id=get_short_url())

    @classmethod
    def lookup_long_version(cls, short_id):
        """Look up a stored url given its short id"""
        return ShortUrl.objects.get(short_id=short_id)

    def full_url(self):
        return f"http://localhost:3080/{self.short_id}"
