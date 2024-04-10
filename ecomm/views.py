from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView
from .forms import CheckoutForm
from django.urls import reverse_lazy
from .models import *



# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = 'group10'
        context['product_list'] = Product.objects.all().order_by("-id")
        return context
# all product  show in home page 
class AllProductView(TemplateView):
    template_name = 'allproducts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context
# About us 
class AboutView(TemplateView):
    template_name = 'about.html'
# contact us 
class ContactView(TemplateView):
    template_name = 'contactus.html'

# product details 
class ProductDetailView(TemplateView):
    template_name='productdetails.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        url_slug =self.kwargs['slug']
        product=Product.objects.get(slug=url_slug)
        product.view_count +=1
        product.save()
        context['product']=product
        return context


# Add to cart 

class AddToCartView(TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pro_id']  # Get the product ID from the URL
        product_obj = Product.objects.get(id=product_id)  # Retrieve the product object

        # Check if a cart exists in the session
        cart_id = self.request.session.get("cart_id")

        if cart_id:
            # If a cart exists, retrieve the cart object
            cart_obj = Cart.objects.get(id=cart_id)

            # Check if the product is already in the cart
            cart_product = cart_obj.cartproduct_set.filter(product=product_obj)

            if cart_product.exists():
                # If the product is already in the cart, increment its quantity and subtotal
                cart_product = cart_product.first()
                cart_product.quantity += 1
                cart_product.subtotal += product_obj.selling_price
                cart_product.save()
            else:
                # If the product is not in the cart, create a new CartProduct object
                cart_product = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product_obj,
                    rate=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
        else:
            # If no cart exists, create a new cart
            cart_obj = Cart.objects.create(total=0)
            # Store the cart ID in the session
            self.request.session['cart_id'] = cart_obj.id

            # Create a new CartProduct object for the product
            cart_product = CartProduct.objects.create(
                cart=cart_obj,
                product=product_obj,
                rate=product_obj.selling_price,
                quantity=1,
                subtotal=product_obj.selling_price
            )

        # Update the total price of the cart
        cart_obj.total += product_obj.selling_price
        cart_obj.save()

        return context

    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pro_id']  # Get the product ID from the URL
        product_obj = Product.objects.get(id=product_id)  # Retrieve the product object

        # Check if a cart exists in the session
        cart_id = self.request.session.get("cart_id")

        if cart_id:
            # If a cart exists, retrieve the cart object
            cart_obj = Cart.objects.get(id=cart_id)

            # Check if the product is already in the cart
            cart_product = cart_obj.cartproduct_set.filter(product=product_obj)

            if cart_product.exists():
                # If the product is already in the cart, increment its quantity and subtotal
                cart_product = cart_product.first()
                cart_product.quantity += 1
                cart_product.subtotal += product_obj.selling_price
                cart_product.save()
            else:
                # If the product is not in the cart, create a new CartProduct object
                cart_product = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product_obj,
                    rate=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
        else:
            # If no cart exists, create a new cart
            cart_obj = Cart.objects.create(total=0)
            # Store the cart ID in the session
            self.request.session['cart_id'] = cart_obj.id


            # Create a new CartProduct object for the product
            cart_product = CartProduct.objects.create(
                cart=cart_obj,
                product=product_obj,
                rate=product_obj.selling_price,
                quantity=1,
                subtotal=product_obj.selling_price
            )

        # Update the total price of the cart
        cart_obj.total += product_obj.selling_price
        cart_obj.save()

        return context
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pro_id']
        product_obj = Product.objects.get(id=product_id)
        cart_id = self.request.session.get("cart_id")

        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_product = cart_obj.cartproduct_set.filter(product=product_obj)

            if cart_product.exists():
                cart_product = cart_product.first()
                cart_product.quantity += 1
                cart_product.subtotal += product_obj.selling_price
                cart_product.save()
            else:
                cart_product = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product_obj,
                    rate=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cart_product = CartProduct.objects.create(
                cart=cart_obj,
                product=product_obj,
                rate=product_obj.selling_price,
                quantity=1,
                subtotal=product_obj.selling_price
            )

        cart_obj.total += product_obj.selling_price
        cart_obj.save()

        return context
    
#my cart 

class MyCartView(TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

# ManageCartView 

class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        # print(cp_id, action)  # Debugging purposes
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart_obj=cp_obj.cart
       
        if action == 'inc':
            cp_obj.quantity+=1
            cp_obj.subtotal+=cp_obj.rate
            cp_obj.save()
            cart_obj.total+=cp_obj.rate
            cart_obj.save()
        
        elif action=='dcr':
            cp_obj.quantity -=1
            cp_obj.subtotal-=cp_obj.rate
            cp_obj.save()
            cart_obj.total-=cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity==0:
                cp_obj.delete()



        elif action=='rmv':
            cart_obj.total-=cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
            
        else:
            pass
        

        return redirect('ecomm:mycart')
    
# empty cart  view

class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id=request.session.get("cart_id", None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect("ecomm:mycart")
    
# CheckOutView 

class CheckOutView(CreateView):
    template_name='checkout.html'
    form_class=CheckoutForm
    success_url=reverse_lazy('ecomm:home')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None
        context['cart']=cart_obj
        return context
    def form_valid(self, form):
        cart_id=self.request.session.get("cart_id")
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status='Order Received'
            del self.request.session['cart_id']
        else:
            return redirect("ecomm:home")
        return super().form_valid(form)

   

