import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.functional import cached_property

from shop.utils import get_item_image_upload_location


class Item(models.Model):
    CATEGORY_CHOICES = (
        ('RAM', 'RAM'),
        ('GPU', 'GPU'),
        ('CPU', 'CPU'),
        ('HDD', 'HDD'),
        ('MB', 'Motherboard'),
        ('FAN', 'Fan'),
        ('PS', 'Power supply'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_item_image_upload_location, null=True, blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    discount_price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], editable=False)
    rating = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        self.discount_price = self.price - self.price * self.discount / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    ship_to = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.order} - {self.item} - {self.amount}'
