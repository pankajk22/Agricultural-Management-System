# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from . models import *  
from . utils import *
import logging
import os
# Create your views here.
import json
import itertools

from datetime import date, datetime
import time
from pytz import timezone


format = "%Y-%m-%d %H:%M:%S %Z%z"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))

LOG_FORMAT="%(asctime)s %(levelname)s %(pathname)s.%(funcName)s(%(filename)s:%(lineno)d) -  %(message)s"
logging.basicConfig(filename="logfile.txt",level=logging.DEBUG,format=LOG_FORMAT)
logger = logging.getLogger()



def portal(request):#homepage for everyone depending upon the type of user it is
    
    logger.info("HOMEPAGE")
    logger.info("******************************************************************************")

    logger.info("homePage")
    
    print("homePage")
    signUpStatus="notLoggedIn"
    #details of all the farmers..
    if request.user.is_authenticated:
        
        try:
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            print("wholesalerLoggedIn")

        except:
            try:
                print("Not a wholesaler, check for farmer here")
                signUpStatus="farmerCompleted"
                #check for farmer
                farmerLoggedIn = farmer.objects.get(user=request.user)
                queryCrops = farmerLoggedIn.getAllCrops
                farmerCrops = []

                for c in queryCrops:
                    farmerCrops.append({'cropId':c.id, 'Crop_name':c.name,'Crop_type':c.cropType,'Quantity':c.quantity,'Crop_price':c.cropPricePerUnit, 'Crop_Desc': c.description})



                context = {'crops': farmerCrops}
                print("farmerLoggedIn")
                return render(request, 'home-farmer.html', context)
    
            except:
                signUpStatus="loggedInNotSignedUp"


                
    allFarmers = farmer.objects.all()
    allFarmerList = []


    if signUpStatus=="wholesalerCompleted":
        for f in allFarmers:
            allFarmerList.append({'userId': f.id,'Name':f.name,'Email':f.email,'Contact':f.phoneNo,'Address_line1':f.address,'Address_city':f.city,'Address_state':f.state,'Address_zipcode':f.zipcode,'MajorSeller': f.majorCropType,'Ratings': f.getRating})

    #print(allFarmerList)
    context = {'allFarmers': allFarmerList, "signUpStatus": signUpStatus}

    print(signUpStatus)
    return render(request, 'home-user.html', context)

def userSignUpPage(request):#rturns the user signup page
    logger.info("*****************************************INSIDE USER SIGNUP PAGE***************************************")
    return render(request, 'signup-user.html')


def farmerSignUpPage(request):#returns the farmer signup page
    logger.info("*****************************************INSIDE FARMER SIGNUP PAGE***************************************")
    return render(request, 'signup-farmer.html')
    
def signUp(request):#creates the user as requested, either farmer or wholesaler

    SignUpDetails = json.loads(request.body)
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
        
    return JsonResponse("signup completed:", safe=False)










################################################### USER PAGES #####################################################


def farmerPage(request):#displays the details of a particular farmer to the buyer

    logger.info("*****************************************FARMERS VISIBLE TO THE BUYERS***************************************")
    
    farmerId = request.GET['farmerId']
    signUpStatus="notLoggedIn"
    #details of all the farmers..
    if request.user.is_authenticated:
        
        try:
            signUpStatus="wholesalerCompleted"
            wholesalerLoggedIn = wholesaler.objects.get(user=request.user)
            print(signUpStatus)

        except:
            try:
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
    
            except:
                signUpStatus="loggedInNotSignedUp"

    if signUpStatus=="wholesalerCompleted":        
        logger.info('..........................................................................')
        
        logger.info("farmer ID to fetch: ", farmerId)

        
        print("farmer ID to fetch: ", farmerId)

        farmerSelected = farmer.objects.get(id=farmerId)

        queryCrops = farmerSelected.getAllCrops
        farmerCrops = []

        for c in queryCrops:
            farmerCrops.append({'cropId':c.id, 'Crop_name':c.name,'Crop_type':c.cropType,'Quantity':c.quantity,'Crop_price':c.cropPricePerUnit})

        print(farmerCrops)

        context = {'farmer':farmerSelected, 'crops': farmerCrops}
        return render(request,'farmerpage.html',context)

    elif signUpStatus=="notLoggedIn":
        logger.info('...........................................................................')
        messages.info(request, 'Not Logged In')
    
    elif signUpStatus=="farmerCompleted":
        logger.info('...........................................................................')
        messages.info(request, 'This is buyer accounts feature, please signup as a buyer to use this feature')

    elif signUpStatus=="loggedInNotSignedUp":
        logger.info('...........................................................................')
        messages.info(request, 'Complete your signup')
        

def userCartPage(request):#returns the cart details of the user

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


def addToCart(request):#add to cart functionality... triggered when a user clicks on add to cart button... it returns a JSON response of the status

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

def updateCart(request):#update cart functionality... triggered when a user clicks on save car button on their cart page.. it returns a JSON response of the status

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



def makeDeal(request):#make deal functionality... triggered when a user clicks on make deal button, i.e. buys the crops from the farmer(s)... it returns a JSON response of the status
#includes the functionality of saving the paper trail into the blockchain 
    cartData = json.loads(request.body)
    print(cartData['cart'])
    paperTrail = []

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

            paperTrail.append({"date": str(date.today()),"time": str(datetime.now().time()), "dealId": dealMade.id, "cropId":cropSelected.id, "cropName": c['crop_name'], "cropType": c['crop_type'], "farmerName": c['farmer_name'], "buyerName":wholesalerLoggedIn.name,"quantity": c['Quantity'], "price": c['Crop_price']})

        print("deals table updated")

        cartTuples = cartItem.objects.all()
        for cartTuple in cartTuples:
            cartTuple.delete()

        print("cart deleted completely")        

        cartData['buyerId']=wholesalerLoggedIn.id

        status = saveInBlockchain(json.dumps(paperTrail))#function in utils.py file...
        print(status)

        return JsonResponse("deal completed", safe=False)

    else:

        return JsonResponse("error", safe=False)



################################################### FARMER PAGES #####################################################

def addCropPage(request):#returns the page to fill the add crop details

    return render(request,'addcrop-farmer.html')

def addCrop(request):#add crop functionality

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
            
            if cropDetails['action']=="add":
                print("adding the crop")
                farmerCrop, created = crop.objects.get_or_create(farmer=farmerLoggedIn, name=cropDetails['Crop_Name'], description=cropDetails['Crop_Description'], cropPricePerUnit=cropDetails['Price_per_unit'], cropType=cropDetails['Crop_Type'])
                
                if created:
                    farmerCrop.quantity=cropDetails['Quantity']

                else:
                    farmerCrop.quantity = farmerCrop.quantity+int(cropDetails['Quantity'])
                
                farmerCrop.save()

            elif cropDetails['action']=="edit":
                print("editing the crop")
                farmerCrop = crop.objects.get(farmer=farmerLoggedIn, id=cropDetails['cropId'])
                
                farmerCrop.cropType = cropDetails['Crop_Type']
                farmerCrop.quantity = cropDetails['Quantity']
                farmerCrop.cropPricePerUnit = cropDetails['Price_per_unit']
                farmerCrop.description = cropDetails['Crop_Description']

            print("....")
            farmerCrop.save()

            return JsonResponse("crop uploaded successfully...", safe=False)

                                                                                                                                                                                                   

    return JsonResponse("not logged in properly...", safe=False)



def editCropPage(request):#returns edit crop page for the crop requested for the edit

    cropId = request.GET['cropId']
    print("crop ID editing: ", cropId)

    cropSelected = crop.objects.get(id=cropId)

    cropDetails = {'crop_id': cropId, 'Crop_Name': cropSelected.name, 'Crop_Type': cropSelected.cropType, 'Quantity': cropSelected.quantity, 'Price_per_unit': cropSelected.cropPricePerUnit, 'Crop_Description': cropSelected.description }

    context = {'cropDetails': cropDetails}

    return render(request, 'editcrop.html', context)


def logout(request):#just logout funcionality

    auth.logout(request)
    signUpStatus="notLoggedIn"
    allFarmers = farmer.objects.all()
    allFarmerList = []

    for f in allFarmers:
        allFarmerList.append({'userId': f.id,'Name':f.name,'Email':f.email,'Contact':f.phoneNo,'Address_line1':f.address,'Address_city':f.city,'Address_state':f.state,'Address_zipcode':f.zipcode,'MajorSeller': f.majorCropType,'Ratings': f.getRating})

    #print(allFarmerList)
    context = {'allFarmers': [], "signUpStatus": signUpStatus}

    print("home-user")
    return render(request, 'home-user.html', context)

def blockchainPaperTrail(request):

    context = {"paperTrail":getPaperTrail()}
    return render(request, 'paperTrail.html', context)