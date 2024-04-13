from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import *


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

# Create your views here.


class HomeView(EcomMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = 'group10'
        all_products= Product.objects.all().order_by("-id")
        paginator = Paginator(all_products, 9)
        page_number = self.request.GET.get("page")
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context
# all product  show in home page


class AllProductView(EcomMixin, TemplateView):
    template_name = 'allproducts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context
# About us


class AboutView(EcomMixin, TemplateView):
    template_name = 'about.html'
# contact us


class ContactView(EcomMixin, TemplateView):
    template_name = 'contactus.html'

# product details


class ProductDetailView(EcomMixin, TemplateView):
    template_name = 'productdetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


# Add to cart

class AddToCartView(EcomMixin, TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pro_id']  # Get the product ID from the URL
        product_obj = Product.objects.get(
            id=product_id)  # Retrieve the product object

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
        product_obj = Product.objects.get(
            id=product_id)  # Retrieve the product object

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

# my cart


class MyCartView(EcomMixin, TemplateView):
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
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()

        else:
            pass

        return redirect('ecomm:mycart')

# empty cart  view


class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomm:mycart")

# CheckOutView


class CheckOutView(EcomMixin, CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('ecomm:home')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.customer:
    #         pass
    #     else:
    #         return redirect("/login/?next=/checkout/")

    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order Received'
            del self.request.session['cart_id']
        else:
            return redirect("ecomm:home")
        return super().form_valid(form)


class CustomerRegistrationView(CreateView):
    template_name = 'customerregistration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomm:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email,  password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

    # CustomerLogoutView


class CustomerLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('ecomm:home')

# CustomerLoginView


class CustomerLoginView(FormView):
    template_name = 'customerlogin.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm:home")

    def form_invalid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            print("next_ulr", next_url)
            return next_url
        else:
            return super().get_success_url()


# CustomerProfileView

class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context

    # CustomerOrderDetails


class CustomerOrderDetails(DetailView):
    template_name = 'customerorderdetail.html'
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.Cart.customer:
                return redirect("ecomm:customerprofile")

        else:
            return redirect("/login/?next=/profile/")

        return super().dispatch(request, *args, **kwargs)
    

class SearchView(TemplateView):
    template_name="search.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
       
        kw=self.request.GET.get("keyword")
        results=Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw) | Q(return_policy__icontains=kw))
        context["results"]=results
  
        return context


# admin pages start here
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm:adminhome")

    def form_valid(self, form):

        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context


class AdminOrderDetailsView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"]=ORDER_STATUS
        return context



class AdminorderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset=Order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id=self.kwargs["pk"]
        order_obj=Order.objects.get(id=order_id)
        new_status=request.POST.get("status")
        order_obj.order_status=new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomm:adminorderdetails", kwargs={"pk":order_id}))

