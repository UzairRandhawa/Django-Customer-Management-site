from . models import *
import json

def cookieCart(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False}
            
        cartitem = order['get_cart_items']

        for i in cart:
            try:
            
                cartitem += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] +=total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                        'product':{
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
        return{'cartitem': cartitem,'order':order,'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False )
        items = order.orderitem_set.all()
        cartitem = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartitem = cookieData['cartitem']
        order = cookieData['order']
        items = cookieData['items']

    return{'items':items,'order':order,'cartitem': cartitem}

def guestORder(request, data):

    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
            email= email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
            customer = customer,
            complete= False
    )
    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderitem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']

            )
    return customer,order
    