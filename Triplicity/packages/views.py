from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Category, Package

def package_list(request, category_slug=None):
    categories = Category.objects.all().order_by('name')
    packages = Package.objects.select_related('category').all().order_by('-created_at')
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        packages = packages.filter(category=selected_category)

    context = {
        'categories': categories,
        'packages': packages,
        'selected_category': selected_category,
    }
    return render(request, 'packages/package_list.html', context)

def package_detail(request, package_slug):
    package = get_object_or_404(Package, slug=package_slug)
    return render(request, 'packages/package_detail.html', {'package': package})
