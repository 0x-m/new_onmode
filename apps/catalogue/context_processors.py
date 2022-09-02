from .models import Category, Option

def CategoryContextProcessor(request):
    return {
        'categories': Category.objects.filter(parent=None),
    }
