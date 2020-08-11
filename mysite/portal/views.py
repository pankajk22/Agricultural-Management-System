# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from . models import *  

# Create your views here.
import json
import itertools

'''
#from web3.auto.infura import w3
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
#print(w3.eth.blockNumber)
#print(w3.isConnected())

infura_url = "https://ropsten.infura.io/v3/105a8a2d75f5428789ffd84c8c9b2ba9"

web3_ropsten = Web3(HTTPProvider(infura_url))

print(web3_ropsten.isConnected())

account="0xbAE6e58D470195BeE55b22872d76B342d0e6BF25"
balance = web3_ropsten.eth.getBalance("0xbAE6e58D470195BeE55b22872d76B342d0e6BF25")
print(f"Balance of account {account} : {balance}")
'''


def portal(request):

    signUpStatus="notLoggedIn"
    #details of all the farmers..
    if request.user.is_authenticated:
        
        try:
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            

        except:
            print("Not a wholesaler, check for farmer here")
            try:
                signUpStatus="farmerCompleted"
                #check for farmer
                farmerLoggedIn = farmer.objects.get(user=request.user)
            except:
                signUpStatus="notCompleted"
                #new account... redirect to signup page
                
    allFarmers = farmer.objects.all()
    allFarmerList = []


    for f in allFarmers:
        allFarmerList.append({'userId': f.id,'Name':f.name,'Email':f.email,'Contact':f.phoneNo,'Address_line1':f.address,'Address_city':f.city,'Address_state':f.state,'Address_zipcode':f.zipcode,'MajorSeller': f.majorCropType,'Ratings': f.getRating})

    print(allFarmerList)
    context = {'allFarmers': allFarmerList, "signUpStatus": signUpStatus}

    return render(request, 'home-user.html', context)

def userSignUpPage(request):

    return render(request, 'signup-user.html')


def farmerSignUpPage(request):

    return render(request, 'signup-farmer.html')
    
def signUp(request):

    SignUpDetails = json.loads(request.GET['signUpUser'])
    print(SignUpDetails)


    if request.user.is_authenticated:
    
        if SignUpDetails["Type"] == "buyer":
            wholesalerCreated, created = wholesaler.objects.get_or_create(user=request.user)
            wholesalerCreated.name = SignUpDetails["Name"]
            wholesalerCreated.email = SignUpDetails["Email"]
            wholesalerCreated.phoneNo = SignUpDetails["Contact"]
            wholesalerCreated.save()
            print("Wholesaler Created")

        elif SignUpDetails["Type"] == "farmer":
            farmerCreated, created = farmer.objects.get_or_create(user=request.user)
            farmerCreated.name = SignUpDetails["Name"]
            farmerCreated.email = SignUpDetails["Email"]
            farmerCreated.phoneNo = SignUpDetails["Contact"]
            farmerCreated.address = SignUpDetails["Address_line1"]
            farmerCreated.city = SignUpDetails["Address_city"]
            farmerCreated.state = SignUpDetails["Address_state"]
            farmerCreated.zipcode = SignUpDetails["Address_zipcode"]
            farmerCreated.idType = SignUpDetails["id_type"]
            farmerCreated.idNumber = SignUpDetails["id_number"]
            farmerCreated.save()
            print("Farmer Created")

    
    else:
        print("not logged in via google")
        
    return redirect("/")

def farmerPage(request):

    farmerId = request.GET['farmerId']
    print("farmer ID to fetch: ", farmerId)

    farmerSelected = farmer.objects.get(id=farmerId)

    queryCrops = farmerSelected.getAllCrops
    farmerCrops = []

    for c in queryCrops:
        farmerCrops.append({'cropId':c.id, 'Crop_name':c.name,'Crop_type':c.cropType,'Quantity':c.quantity,'Crop_price':c.cropPricePerUnit})

    print(farmerCrops)

    context = {'farmer':farmerSelected, 'crops': farmerCrops}
    return render(request,'farmerpage.html',context)

def userCartPage(request):

    signUpStatus="notLoggedIn"
    #details of all the farmers..
    if request.user.is_authenticated:
        

        signUpStatus="wholesalerCompleted"
        wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
        cart = wholesalerLoggedIn.getCart

        cartList = []

        for c in cart:
            cropSelected = crop.objects.get(id=c.crop_id)
            farmerOfCrop = cropSelected.farmer
            cartList.append({'crop_id': c.crop_id, 'crop_name' :cropSelected.name,'crop_type': cropSelected.cropType, 'farmerId': farmerOfCrop.id, 'farmer_name': farmerOfCrop.name,'Quantity':c.quantity, 'max_quantity_available':cropSelected.quantity, 'Crop_price':cropSelected.cropPricePerUnit})
        
        context = {'cartList': cartList}

        return render(request,'user-cart.html', context)

        '''except:
            print("Not a wholesaler, check for farmer here")
            try:
                signUpStatus="farmerCompleted"
                #check for farmer
                farmerLoggedIn = farmer.objects.get(user=request.user)
            except:
                signUpStatus="notCompleted"
                #new account... redirect to signup page'''
        
    return redirect("/")


def addToCart(request):

    data = json.loads(request.body)
    cropId = data["cropId"]
    qty = data["qty"]

    if request.user.is_authenticated:
    
        try:
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            cropSelected = crop.objects.get(id=cropId)
            print("Checking wholesaler's cart")
            cartItemSelected, created = cartItem.objects.get_or_create(wholesaler=wholesalerLoggedIn, crop=cropSelected)
            cartItemSelected.quantity = qty
        
            cartItemSelected.save()
            print("Item saved...")
            print(wholesalerLoggedIn.getCart)            

            return JsonResponse("cart Updated", safe=False)
            
        except:
            print("Not a wholesaler, check for farmer here")
            try:
                signUpStatus="farmerCompleted"
                #check for farmer
                farmerLoggedIn = farmer.objects.get(user=request.user)
                return JsonResponse("not feasible", safe=False)

            except:
                signUpStatus="notCompleted"
                return JsonResponse("not feasible", safe=False)
                #new account... redirect to signup page'''


    else:
        return JsonResponse("not feasible", safe=False)

def updateCart(request):

    cartData = json.loads(request.body)
    print(cartData['cart'])

    if request.user.is_authenticated:
    
        for c in cartData['cart']:
            print(c)
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            cropSelected = crop.objects.get(id=c['crop_id'])
            cartItemSelected, created = cartItem.objects.get_or_create(wholesaler=wholesalerLoggedIn, crop=cropSelected)
            
            cartItemSelected.quantity = c['Quantity']
            
            if cartItemSelected.quantity <= 0:
                cartItemSelected.delete()
            
            else:
                cartItemSelected.save()
        

        return JsonResponse("cart updated", safe=False)

    else:

        return JsonResponse("not updated", safe=False)