from .odels import Cart, CartDetail

# we use context processor to return data of cart in all pages



def get_or_create_cart(request):
    if request.user.is_autenticated:
        cart , created = Cart.objects.get_or_create(user=request.user,status='inprogress')
        if not created:
            cart_detail = CartDetail.objects.filter(cart=cart)
            return {'cart_data' : cart , 'cart_detail_data' : cart_detail}
        return {'cart_data' : cart}
    else:
        return{}