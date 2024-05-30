from django.shortcuts import render, get_object_or_404
from . models import Pet, Product   
from . forms import SearchForm

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