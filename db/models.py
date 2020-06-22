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
    expire_date = models.DateTimeField('date')
    count = models.IntegerField(default=1)
    ownerID  = models.IntegerField(default=0)

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

