from .models import Certificate, SiteInfo


def info(request):
    siteinfo = SiteInfo.objects.first()
    return {
        "siteinfo": siteinfo,
        "GOOGLE_TAG_ID": siteinfo.GOOGLE_TAG_ID if siteinfo else "",
        "certs": Certificate.objects.filter(show_on_index=True).all(),
    }
