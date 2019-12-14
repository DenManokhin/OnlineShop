from django.shortcuts import render

from shop.models import Item


def items_view(request):
    context = {}
    context["items"] = Item.objects.all()
    return render(request, 'shop.html', context)

