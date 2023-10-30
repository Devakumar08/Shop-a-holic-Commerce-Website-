from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        banner =  Product.objects.filter(category='B')
        if request.user.is_authenticated:
            li = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles,'totalitem':li,'banner':banner})

class ProductDetailView(View):
    def get(self, request,pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart =False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required 
def add_to_cart(request):  
    totalitem = 0 
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request): 
    totalitem = 0 
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [ p for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity* p.product.discounted_price) 
                amount += temp_amount       
                total_amount= amount+ shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart,'total_amount':total_amount,'amount':amount,'totalitem':totalitem})
        else:
            
            return render(request, 'app/emptycart.html', {'carts':cart,'total_amount':total_amount,'amount':amount,'totalitem':totalitem})
        
   
def plus_cart(request) :
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.0
        cart_product = [ p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            temp_amount = (p.quantity* p.product.discounted_price) 
            amount += temp_amount       
          
        data = {
                'quantity': c.quantity,
                'amount':amount,
                'total_amount':amount+ shipping_amount
            }
        return JsonResponse(data)
        
        

def minus_cart(request) :
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.0
        cart_product = [ p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            temp_amount = (p.quantity* p.product.discounted_price) 
            amount += temp_amount       
           
        
        data = {
                'quantity': c.quantity,
                'amount':amount,
                'total_amount':amount+shipping_amount
            }
        return JsonResponse(data)
@login_required 
def remove_cart(request) :
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity-=1
        c.delete()
        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.0
        cart_product = [ p for p in Cart.objects.all() if p.user==request.user]
        # print(cart_product)
        for p in cart_product:
            temp_amount = (p.quantity* p.product.discounted_price) 
            amount += temp_amount       
          
        
        data = {
                
                'amount':amount,
                'total_amount':amount + shipping_amount
            }
        return JsonResponse(data)
        
@login_required    
def checkout1(request):
    totalitem = 0
    user = request.user
    add= Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [ p for p in Cart.objects.all() if p.user==request.user]   
    if cart_product: 
        for p in cart_product:
            temp_amount = (p.quantity* p.product.discounted_price) 
            amount += temp_amount   
        total_amount = amount + shipping_amount
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        
    return render(request, 'app/checkout.html',{'add':add, 'total_amount': total_amount, 'cart_items':cart_items,'totalitem':totalitem} )
   
@login_required   
def payment_done(request):
    print("Payment done view")
    user = request.user
    custid = request.GET.get('custid')      
    print(custid)     
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity= c.quantity).save()
        c.delete()
    return redirect("orders")
   
   
   
   
   
   
   
   
   
   
   
   
            
            
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required 
def address(request):
    add = Customer.objects.filter(user = request.user)
    
    return render(request, 'app/address.html', {'add':add,'active':'btn-primary'})


@login_required 
def orders(request):
    orders_placed = OrderPlaced.objects.filter(user=request.user)
    
    return render(request, 'app/orders.html', {'order_placed':orders_placed})


def banner(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data is None:
        banner = Product.objects.filter(category='B')
    elif data in ['Samsung', 'Moto', 'Suit','Fashion','Headphones']:
        banner = Product.objects.filter(category='B', brand=data)
    return render(request, 'app/banner.html', {'banner': banner,'totalitem':totalitem})
        
def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data in ['Samsung', 'Nokia', 'Apple']:
        mobiles = Product.objects.filter(category='M', brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M', discounted_price__lt=20000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M', discounted_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles,'totalitem':totalitem})


def topwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    if data is None:
        tops = Product.objects.filter(category='TW')
    elif data in ['Nike', 'Raymond', 'Beast', 'Adidas', 'Leo']:
        tops = Product.objects.filter(category='TW', brand=data)
    elif data == 'below':
        tops = Product.objects.filter(category='TW', discounted_price__lt=499)
    elif data == 'above':
        tops = Product.objects.filter(category='TW', discounted_price__gt=499)
    return render(request, 'app/topwear.html', {'tops': tops,'totalitem':totalitem})

def login(request):
 return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    totalitem = 0
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'You have been registered')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@method_decorator(login_required, name = 'dispatch')
class ProfileView(View):
    totalitem = 0
    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})

    def post(self,request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr, name=name, locality=locality, city=city, state =state, zipcode= zipcode )
            reg.save()
            
            messages.success(request,'Congratulations Profile has been updated Successfully')
            
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})