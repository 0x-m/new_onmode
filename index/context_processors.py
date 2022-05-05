
from .models import SiteInfo, Certificate

def info(request):
    return {
        'siteinfo': SiteInfo.objects.first(),
        'certs' : Certificate.objects.filter(show_on_index=True).all()

    }

