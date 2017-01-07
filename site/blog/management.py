"""
Creates the default database.
"""

def create_default_db(**kwargs):
    from django.contrib.sites.models import Site
    from . import models
    # for site in Site.objects.all():
    #     if not hasattr(site, 'blog'):
    #         Blog.objects.create(site=site)