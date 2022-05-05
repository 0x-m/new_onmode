from .models import SiteInfo

def info(requet):
    return {
        'siteinfo': SiteInfo.objects.first()
    }

