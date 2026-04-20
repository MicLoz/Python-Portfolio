from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem

def product_list(request):
    products = Product.objects.all()

    print(products.query)
    print(products.count())

    categories = Category.objects.all()

    category_id = request.GET.get('category')
    search_query = request.GET.get('search')

    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)

    # Search by title
    if search_query:
        products = products.filter(title__icontains=search_query)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }

    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('product_list')

def cart_view(request):
    cart = request.session.get('cart', {})

    # HANDLE UPDATES (POST)
    if request.method == 'POST':
        for product_id, quantity in request.POST.items():
            if product_id.startswith('qty_'):
                pid = product_id.replace('qty_', '')

                try:
                    qty = max(0, int(quantity))
                except ValueError:
                    continue

                if qty == '0':
                    cart.pop(pid, None)
                else:
                    cart[pid] = qty

        request.session['cart'] = cart

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        product.quantity = quantity
        product.total_price = product.price * quantity

        total += product.total_price
        products.append(product)

    context = {
        'products': products,
        'total': total
    }

    return render(request, 'shop/cart.html', context)

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if not name or not email or not address:
            return render(request, 'shop/checkout.html', {
                'error': 'All fields are required'
            })

        total = 0

        order = Order.objects.create(
            name=name,
            email=email,
            address=address,
            total=0
        )

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)

            item_total = product.price * quantity
            total += item_total

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # update total AFTER calculation
        order.total = total
        order.save()

        # clear cart
        request.session['cart'] = {}

        return redirect('order_success')

    return render(request, 'shop/checkout.html',{
        'cart': cart
    })

def order_success(request):
    return render(request, 'shop/success.html')

