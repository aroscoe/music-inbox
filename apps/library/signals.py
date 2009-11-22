from django.dispatch import Signal

upload_done = Signal(providing_args=["file", "name"])