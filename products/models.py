import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    stripe_product_price_id = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency="byn"
        )
        return stripe_product_price


class CartQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(cart.cart_sum() for cart in self)

    def total_quantity(self):
        return sum(cart.quantity for cart in self)

    def stripe_products(self):
        line_items = []
        for cart in self:
            item = {
                'price': cart.product.stripe_product_price_id,
                'quantity': cart.quantity,
            }
            line_items.append(item)
        return line_items


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def cart_sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        cart_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'product_price': float(self.product.price),
            'sum': float(self.cart_sum()),
        }
        return cart_item

    @classmethod
    def create_or_update(cls, product_id, user):
        carts = Cart.objects.filter(user=user, product_id=product_id)

        if not carts.exists():
            obj = Cart.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            cart = carts.first()
            cart.quantity += 1
            cart.save()
            is_created = False
            return cart, is_created
