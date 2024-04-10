from django.urls import path
from .views import *
app_name="ecomm"
urlpatterns=[
    path("", HomeView.as_view(), name='home'),
    path("about/", AboutView.as_view(), name='aboutus'),
    path("contact/", ContactView.as_view(), name='contact'),
    path("all-products/", AllProductView.as_view(), name='allproducts'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='productdetails'),
    path('add-to-add-<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name='managecart'),
    path("empty-cart/", EmptyCartView.as_view(), name='emptycart'),
    path("checkout/", CheckOutView.as_view(), name='checkout'),
]