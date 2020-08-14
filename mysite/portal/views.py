# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from . models import *  
from . utils import *

# Create your views here.
import json
import itertools




def portal(request):

    signUpStatus="notLoggedIn"
    #details of all the farmers..
    if request.user.is_authenticated:
        
        try:
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            print("wholesalerLoggedIn")

        except:
            print("Not a wholesaler, check for farmer here")
            signUpStatus="farmerCompleted"
            #check for farmer
            farmerLoggedIn = farmer.objects.get(user=request.user)
            queryCrops = farmerLoggedIn.getAllCrops
            farmerCrops = []

            for c in queryCrops:
                farmerCrops.append({'cropId':c.id, 'Crop_name':c.name,'Crop_type':c.cropType,'Quantity':c.quantity,'Crop_price':c.cropPricePerUnit})



            context = {'crops': farmerCrops}
            print("farmerLoggedIn")
            return render(request, 'home-farmer.html', context)
        


                
    allFarmers = farmer.objects.all()
    allFarmerList = []


    for f in allFarmers:
        allFarmerList.append({'userId': f.id,'Name':f.name,'Email':f.email,'Contact':f.phoneNo,'Address_line1':f.address,'Address_city':f.city,'Address_state':f.state,'Address_zipcode':f.zipcode,'MajorSeller': f.majorCropType,'Ratings': f.getRating})

    #print(allFarmerList)
    context = {'allFarmers': allFarmerList, "signUpStatus": signUpStatus}

    print("home-user")
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










################################################### USER PAGES #####################################################


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
            if c.quantity > cropSelected.quantity:
                c.quantity = cropSelected.quantity
                
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



def makeDeal(request):
 
    cartData = json.loads(request.body)
    print(cartData['cart'])

    if request.user.is_authenticated:
    
        for c in cartData['cart']:
            print(c)
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            cropSelected = crop.objects.get(id=c['crop_id'])
            cropSelected.quantity=cropSelected.quantity-c['Quantity']
            cropSelected.save()
            dealMade = dealsMade.objects.create(buyer=wholesalerLoggedIn, crop=cropSelected)
            dealMade.quantity = c['Quantity']
            dealMade.save()

        print("deals table updated")

        cartTuples = cartItem.objects.all()
        for cartTuple in cartTuples:
            cartTuple.delete()

        print("cart deleted completely")        

        cartData['buyerId']=wholesalerLoggedIn.id

        status = saveInBlockchain(json.dumps(cartData))
        print(status)

        return JsonResponse("deal completed", safe=False)

    else:

        return JsonResponse("error", safe=False)

################################################### FARMER PAGES #####################################################

def addCropPage(request):


    return render(request,'addcrop-farmer.html')

def addCrop(request):

    cropDetails = json.loads(request.body)

    print(cropDetails)
    signUpStatus="notLoggedIn"
        
    if request.user.is_authenticated:
        
        try:
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            print("wholesalerLoggedIn")

        except:
            print("Not a wholesaler, check for farmer here")
            signUpStatus="farmerCompleted"
            #check for farmer
            farmerLoggedIn = farmer.objects.get(user=request.user)

            print("farmerLoggedIn")

            context = {'farmerId': farmerLoggedIn.id}
            
            farmerCrop, created = crop.objects.get_or_create(farmer=farmerLoggedIn, name=cropDetails['Crop_Name'])

            if created:
                print("new crop...")
            
            else:
                print("existing crop...")
            
            farmerCrop.cropType = cropDetails['Crop_Type']
            farmerCrop.quantity = cropDetails['Quantity']
            farmerCrop.cropPricePerUnit = cropDetails['Price_per_unit']
            farmerCrop.description = cropDetails['Crop_Description']

            print("....")
            farmerCrop.save()

            return JsonResponse("crop uploaded successfully...", safe=False)

                                                                                                                                                                                                   

    return JsonResponse("not logged in properly...", safe=False)



def editCropPage(request):

    cropId = request.GET['cropId']
    print("crop ID editing: ", cropId)

    cropSelected = crop.objects.get(id=cropId)

    cropDetails = {'crop_id': cropId, 'Crop_Name': cropSelected.name, 'Crop_Type': cropSelected.cropType, 'Quantity': cropSelected.quantity, 'Price_per_unit': cropSelected.cropPricePerUnit, 'Crop_Description': cropSelected.description }

    context = {'cropDetails': cropDetails}

    return render(request, 'editcrop.html', context)


