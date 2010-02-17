import tea
from django.conf import settings

def decrypt_id(id, exception_to_raise):
    try:
        if not isinstance(id, long):
            id = long(id)
            return tea.decrypt(id , settings.KEY)
    except ValueError:
        raise exception_to_raise

def encrypt_id(id):
    return tea.encrypt(id, settings.KEY)
