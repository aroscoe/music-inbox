from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=60, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'libraries'
    
    class Admin:
        pass

class Artist(models.Model):
    name    = models.CharField(max_length=150)
    library = models.ForeignKey(Library)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % (self.name)
    
    class Admin:
        pass

class Album(models.Model):
    name   = models.CharField(max_length=150)
    artist = models.ForeignKey(Artist)
    
    def __str__(self):
        return '%s - %s' % (self.artist.name, self.name)

    #def __unicode__(self):
    #    return u'%s - %s' % (self.artist.name, self.name)
    
    class Admin:
        pass
