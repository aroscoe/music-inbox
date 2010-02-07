from django.test import TestCase

def test_views_missing(self):
    """
    >>> from library.models import *
    >>> Library.objects.create(pk=1, name='foo')
    <Library: foo>
    >>> from library.views import *
    >>> missing(None, 1).content
    '{"processing": 2, "data": {}}'
    """

