from django_cron import cronScheduler, Job
from library.models import MBArtist

class CheckArtists(Job):
    """cron job that looks for new albums once a day, for ever artist in every library"""

    # once / day
    run_every = 60 * 60 * 24

    def job(self):
        for artist in MBArtist.objects.all():
            artist.fetch_albums()
        

cronScheduler.register(CheckArtists)
