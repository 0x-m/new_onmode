from .models import Category


def CategoryContextProcessor(request):
    return {
        "categories": Category.objects.filter(parent=None),
    }
