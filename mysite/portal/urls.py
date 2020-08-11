from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal, name="portal"),
    path('userSignUpPage/', views.userSignUpPage, name="userSignUpPage"),
    path('signUp/', views.signUp, name="signUp"),
    path('farmerPage/', views.farmerPage, name="farmerPage"),
    path('addToCart/', views.addToCart, name="addToCart"),
    path('userCartPage/', views.userCartPage, name="userCartPage"),
    path('updateCart/', views.updateCart, name="updateCart")
]