from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=60, blank=True)
    
    class Meta:
        verbose_name_plural = 'libraries'
    
    class Admin:
        pass

class LibraryItem(models.Model):
    name = models.CharField(max_length=150)
    library = models.ForeignKey(Library)
    
    class Admin:
        pass