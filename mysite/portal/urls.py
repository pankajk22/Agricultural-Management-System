from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal, name="portal"),
    path('paperTrail', views.blockchainPaperTrail, name="paperTrail"),
    path('userSignUpPage/', views.userSignUpPage, name="userSignUpPage"),
    path('farmerSignUpPage/', views.farmerSignUpPage, name="farmerSignUpPage"),
    path('signUp/', views.signUp, name="signUp"),
    path('logout/', views.logout, name="logout"),
    
    ### User Pages
    path('farmerPage/', views.farmerPage, name="farmerPage"),
    path('addToCart/', views.addToCart, name="addToCart"),
    path('userCartPage/', views.userCartPage, name="userCartPage"),
    path('updateCart/', views.updateCart, name="updateCart"),
    path('makeDeal/', views.makeDeal, name="makeDeal"),

    ### Farmer Pages
    path('addCropPage/', views.addCropPage, name="addCropPage"),    
    path('addCrop/', views.addCrop, name="addCrop"),
    path('editCropPage/', views.editCropPage, name="editCropPage")
]