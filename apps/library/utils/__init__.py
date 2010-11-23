from django.conf import settings
from django.contrib.sites.models import Site

import tea

def decrypt_id(id, exception_to_raise):
    try:
        if not isinstance(id, long):
            id = long(id)
        return tea.decrypt(id, settings.KEY)
    except ValueError:
        raise exception_to_raise
 
def encrypt_id(id):
    return tea.encrypt(id, settings.KEY)

def rss_url(library_id):
    '''Returns the full rss url for a library_id'''
    return 'http://%s/library/feeds/newalbums/%s/' % \
        (Site.objects.get_current().domain, encrypt_id(library_id))

