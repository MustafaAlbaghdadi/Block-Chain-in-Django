from datetime import timezone, datetime
from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Product(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    count = models.IntegerField(default=1)
    ownerID  = models.IntegerField(default=0)
    farmerID  = models.IntegerField(default=0)
    farm_temp = models.CharField(max_length=200)
    farm_humidity = models.CharField(max_length=200)
    compost_type = models.CharField(max_length=200)
    seed_type = models.CharField(max_length=200)
    unite_type = models.CharField(max_length=200)
    date_of_harvest = models.DateTimeField('date_of_harvest')
    farm_location = models.CharField(max_length=200)

    #Factory
    factoryID  = models.IntegerField(default=0, blank=True, null=True)
    canning_date = models.DateTimeField('date', blank=True, null=True)
    processing_date = models.DateTimeField('date', blank=True, null=True)
    expire_date = models.DateTimeField('date', blank=True, null=True)
    factory_temp = models.CharField(max_length=200, blank=True, null=True)
    factory_humidity = models.CharField(max_length=200, blank=True, null=True)
    #destrbutor
    distrabuterID  = models.IntegerField(default=0, blank=True, null=True)
    entry_store_date = models.DateTimeField('date', blank=True, null=True)
    destrbutor_temp = models.CharField(max_length=200, blank=True, null=True)
    destrbutor_humidity = models.CharField(max_length=200, blank=True, null=True)
    #markting
    marktingID  = models.IntegerField(default=0, blank=True, null=True)
    entry_market_date = models.DateTimeField('date', blank=True, null=True)
    market_temp = models.CharField(max_length=200, blank=True, null=True)
    market_humidity = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.Name

class Contract(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sellerID = models.IntegerField()
    buyerID = models.IntegerField()
    date = models.DateField('date published')
    info = models.CharField(max_length=10000)
    strHash = models.CharField(max_length=200 ,default='')
    prevHash = models.CharField(max_length=200,default='')

