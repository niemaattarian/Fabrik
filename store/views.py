from unittest import loader

from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from store.models import Product
from store.forms import ProductForm

# Create your views here.

class ProductList(ListView):
    model = Product

class ProductDetail(DetailView):
    model = Product

class ProductUpdate(UpdateView):
    model = Product
    # Field must be same as the model attribute
    fields = ['name', 'price', 'size']
    success_url = reverse_lazy('product_list')

class ProductCreate(CreateView):
    model = Product
    # Field must be same as the model attribute
    fields = ['name', 'price', 'size']
    success_url = reverse_lazy('product_list')

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


def index(request, context=None):
    if context is None:
        context = {}

    context['products'] = Product.objects.all()

    return render(request, 'store/product_list.html', context=context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return index(request, {'user': user})

        else:
            return redirect('login')

    elif request.method == 'GET':
        return render(request, 'registration/login.html', {})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #User.objects.create_user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return index(request, {'user': user})

        else:
            return redirect('login')

        print(user)
    elif request.method == 'GET':
        return render(request, 'registration/register.html', {})

def logout(request):
    if request.method == 'POST':
        logout(request)

    elif request.method == 'GET':
        return render(request, 'store/product_list.html', {})