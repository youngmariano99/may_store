from django.shortcuts import render

from django.views.generic.list import ListView
# Create your views here.
from .models import Product

class ProductListView(ListView):
    template_name = "index.html"
    queryset = Product.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] ='Listado de productos'
        context['products'] = context ['product_list']
        
        return context