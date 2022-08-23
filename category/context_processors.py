from .models import Category
from store.models import Product


def menu_links(request):

    links = Category.objects.all()
    return dict(links=links)
