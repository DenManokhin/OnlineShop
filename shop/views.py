from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from shop.models import Item, Review


def items_view(request):
    context = {"items": Item.objects.all()}
    return render(request, 'shop.html', context)


class ShopView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'shop.html'

    def get_queryset(self):
        category = self.request.GET.get('category', 'All')
        sort_order = self.request.GET.get('orderby', 'title')

        if category == 'All':
            return Item.objects.all().order_by(sort_order)
        else:
            return Item.objects.filter(category=category).order_by(sort_order)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [("All", "All")]
        context['categories'].extend(Item.CATEGORY_CHOICES)
        context['current_category'] = self.request.GET.get('category', 'All')

        context['sort_orders'] = [
            ('title', 'Title'),
            ('category', 'Category'),
            ('discount_price', 'Price'),
            ('rating', 'Rating')
        ]
        context['current_sort_order'] = self.request.GET.get('orderby', 'title')
        return context


class ProductView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(item=self.object)
        return context
