from .models import Cart, CartDetail

# we use context processor to return data of cart in all pages



def get_or_create_cart(request):    # get or create a cart for a user 
    if request.user.is_authenticated:  # if user is authenticated 
        cart , created = Cart.objects.get_or_create(user=request.user,status='inprogress') # get a cart of exiting user, if not, create one
        if not created:             # if cart is not created
            cart_detail = CartDetail.objects.filter(cart=cart)   # get all products of exiting cart 
            return {'cart_data' : cart , 'cart_detail_data' : cart_detail}   # return data of cart and cart detail 
        return {'cart_data' : cart}       # return data of cart 
    else:                                 # if user is not authenticated
        return{}                         # return empty dictionary