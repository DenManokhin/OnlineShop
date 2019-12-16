from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from django.db.models.functions import Cast

from shop.models import Item, OrderItem, Order, Review


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


@login_required
def add_to_cart_view(request, slug):
    item_to_be_added = get_object_or_404(Item, slug=slug)
    # Check if current user have unpaid order
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    if order:
        # Check if item to be added is already in the cart
        order_item = order.orderitem_set.filter(order=order, item=item_to_be_added).first()
        if order_item:
            order_item.amount += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(order=order, item=item_to_be_added, amount=1)
    # If current user doesn't have an unpaid order create one
    else:
        order = Order.objects.create(user=request.user, is_paid=False)
        order_item = OrderItem.objects.create(order=order, item=item_to_be_added, amount=1)

    order_item.save()
    messages.info(request, 'This item was added to your cart.')
    return redirect('product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    OrderItem.objects.filter(
        item__slug=slug,
        order__is_paid=False,
        order__user=request.user
    ).delete()
    return redirect('cart')


@login_required
def cart_view(request):
    context = {
        'cart_items': []
    }

    order = request.user.order_set.filter(is_paid=False).first()
    if order:
        cart_items = order.orderitem_set.all()
    else:
        cart_items = OrderItem.objects.none()

    for order_item in cart_items:
        cart_items_with_subtotal = {
            'order_item': order_item,
            'subtotal': order_item.amount * order_item.item.discount_price
        }
        context['cart_items'].append(cart_items_with_subtotal)

    total = 0
    for cart_item in context['cart_items']:
        total += cart_item['subtotal']
    context['total'] = total

    return render(request, 'cart.html', context)
