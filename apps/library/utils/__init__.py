from library.utils import tea
from settings import KEY

def decrypt_id(id, exception_to_raise):
    try:
        if not isinstance(id, long):
            id = long(id)
            id = tea.decrypt(id , KEY)
    except ValueError:
        raise exception_to_raise

def encrypt_id(id):
    return tea.encrypt(id, KEY)
