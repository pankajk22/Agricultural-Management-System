# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class wholesaler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    phoneNo = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    @property
    def getCart(self):
        allItems = self.cartitem_set.all()
        return allItems

class farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    phoneNo = models.CharField(max_length=20, null=True, blank=True)
    #address attributes
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    #id attributes
    idType = models.CharField(max_length=200, null=True)
    idNumber = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.name)

    @property
    def getAllCrops(self):
        allCrops = self.crop_set.all()
        return allCrops

    @property
    def majorCropType(self):
        allCrops = self.crop_set.all()
        allCropType = []
        for crop in allCrops:
            if crop.cropType not in allCropType:
                allCropType.append(crop.cropType)
        print("#################",allCropType)
        return allCropType

    @property
    def getRating(self):
        allRatings = self.farmerrating_set.all()
        ratingSum = 0 
        for rating in allRatings:
            ratingSum = ratingSum + rating

        if len(allRatings) == 0:
            return "Not rated yet"
        else:
            return "Ratings:"+str(float(float(ratingSum)/float(len(allRatings))))



class crop(models.Model):
    farmer = models.ForeignKey(farmer, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    cropType = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(default=1, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    cropPricePerUnit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

class dealsMade(models.Model):
    crop = models.ForeignKey(crop, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.FloatField(default=1)
    buyer = models.ForeignKey(wholesaler, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class farmerRating(models.Model):
    farmer = models.ForeignKey(farmer, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()

class cartItem(models.Model):
    wholesaler = models.ForeignKey(wholesaler, on_delete=models.CASCADE, null=True, blank=True)
    crop = models.ForeignKey(crop, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(crop.name)