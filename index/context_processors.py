
from .models import SiteInfo, Certificate

def info(request):
    siteinfo = SiteInfo.objects.first()
    return {
        'siteinfo': siteinfo,
        'GOOGLE_TAG_ID': siteinfo.GOOGLE_TAG_ID,
        'certs' : Certificate.objects.filter(show_on_index=True).all(),
    }

