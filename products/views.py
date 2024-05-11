from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q # NECESSARY for search functionality
from .models import Product, Category

# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries """
    
    products = Product.objects.all()
    query = None # used for search bar logic, below
    categories = None # used for category filtering logic in nav bar
    sort = None # used for sorting logic in nav bar
    direction = None # used for sorting logic in nav bar

    if request.GET:

        # Sort logic

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        
        # Sort logic part 1 end.

        # Category filtering logic
        
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Category filtering logic end.

        # SEARCH BAR LOGIC!!!!
        
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
            
        # Search bar logic end.

    current_sorting = f'{sort}_{direction}' # extra bit for sort logic

    context = {
        'products': products,
        'search_term': query, # needed for search bar logic
        'current_categories': categories, # needed for category filtering logic
        'current_sorting': current_sorting, # needed for sort logic
    }
    
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)