from products.models import Cart


def carts(request):
    user = request.user
    if user.is_authenticated:
        return {'carts': Cart.objects.filter(user=user)}
    else:
        return {'carts': []}
