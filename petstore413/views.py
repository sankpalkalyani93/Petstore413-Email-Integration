from django.http import HttpResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from . models import Pet, Product, Cart, CartItem, OrderItems 
from . forms import OrderCreateForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def pet_list(request):
    form = SearchForm(request.GET or None)
    pets = Pet.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        pets = pets.filter(name__icontains=query)

    return render(request, 'petstore413/pet_list.html', {'pets': pets, 'form': form})

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'petstore413/pet_detail.html', {'pet': pet})

def product_list(request):
    form = SearchForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        products = products.filter(name__icontains=query)

    return render(request, 'petstore413/product_list.html', {'products': products, 'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'petstore413/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, item_type, item_id):
    user_cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    if item_type == 'pet':
        item = get_object_or_404(Pet, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, pet=item)
    else:
        item = get_object_or_404(Product, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    cart_items = CartItem.objects.filter(cart=cart) 
    total = sum(item.total for item in cart_items)
    print("total : ", total )
    return render(request, 'petstore413/cart_detail.html', {'cart_items': cart_items, 'total': total})

def increase_qunatity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def order_create(request):
    cart = Cart.objects.get(id=1)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart.items.all():
                OrderItems.objects.create(
                    order = order,
                    product = item.product,
                    pet = item.pet,
                    price = item.product.price if item.product else item.pet.price,
                    quantity = item.quantity
                )
            cart.items.all().delete()

            # Send email with order details
            subject = f'Order Confirmation - {order.id}'
            html_message = render_to_string('petstore413/order_confirmation_email.html', {'order': order})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to = form.cleaned_data['email']
            send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=False)

            client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
            payment_data = {
                'amount': int(order.total_cost * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}', 
            }
            print(payment_data)
            payment = client.order.create(data=payment_data)
             
            return render(request, 'petstore413/order_created.html', {'order': order, 'payment': payment, 'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID})
    else : 
        form = OrderCreateForm()
    return render(request, 'petstore413/order_create.html', {'cart': cart, 'form': form})

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        return HttpResponse("Payment Successful")
    return HttpResponse(status=400)