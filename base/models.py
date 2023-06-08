from django.db import models
from jsonfield import JSONField
from django.shortcuts import redirect
from django.urls import reverse

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    description = models.TextField()
    platform = models.CharField(max_length=100)
    poster = models.CharField(max_length=1000) # ipfs addreess
    images = JSONField() # it's gonna store like a json, we will convert it to python list which contain ipfs addresses
    price = models.FloatField() # in ETH
    token_id = models.CharField(max_length=100) # NFT
    private_key = models.CharField(max_length=200) # from encrypted ipfs hash
    slug = models.SlugField(max_length=150, unique=True) # local url
    wallet_address = models.CharField(max_length=200) # game developer wallet address

    def get_absolute_url(self):
        return reverse('game_detail_url', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name