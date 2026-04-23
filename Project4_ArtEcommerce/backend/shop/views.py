from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from decimal import Decimal


def evaluate_cart(cart):
    products = []
    items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        if quantity <= 0:
            continue

        item_total = product.price * quantity
        total += item_total

        # UI data
        product.quantity = quantity
        product.total_price = item_total
        products.append(product)

        # DB data
        items.append((product, quantity))

    return products, total, items


def product_list(request):
    products = Product.objects.all()

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

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


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

                if qty == 0:
                    cart.pop(pid, None)
                else:
                    cart[pid] = qty

        request.session['cart'] = cart

    products, total, _ = evaluate_cart(cart)

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

        products, total, items_to_create = evaluate_cart(cart)

        # Prevent empty orders
        if not items_to_create:
            return redirect('cart')

        # Create order AFTER validation
        order = Order.objects.create(
            name=name,
            email=email,
            address=address,
            total=Decimal(total)
        )

        # Create order items
        for product, quantity in items_to_create:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # clear cart
        request.session['cart'] = {}

        return redirect('order_success')

    products, total, _ = evaluate_cart(cart)

    return render(request, 'shop/checkout.html',{
        'products': products,
        'total': total
    })


def order_success(request):
    return render(request, 'shop/success.html')

