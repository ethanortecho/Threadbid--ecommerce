from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Listing(models.Model):

    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('LIKE_NEW', 'Like New'),
        ('USED', 'Used'),
        ('REFURBISHED', 'Refurbished')
    ]

    CATEGORY_CHOICES = [
        ('SHIRT', 'Shirt'),
        ('T_SHIRT', 'T-Shirt'),
        ('HOODIE', 'Hoodie'),
        ('FOOTWEAR', 'Footwear'),
        ('PANTS', 'Pants'),
    ]
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL')
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "listings", default=1)
    
    title = models.CharField(max_length=200)

    description = models.CharField(max_length = 1000)

    starting_price = models.DecimalField(max_digits=5, decimal_places=2)

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True,null=True)

    condition = models.CharField(max_length=100,choices=CONDITION_CHOICES)

    size = models.CharField(max_length=100)
    
    status  = models.BooleanField(default=True)



    #OTHER POTENTIAL FIELDS
        #brand?

    def minimum_bid(self):
        highest = self.bids.order_by('-bid').first()
        return highest.bid +1 if highest else self.starting_price
    
    def size_type(self):
        def size_type(self):
            if self.category in ['SHIRT', 'T_SHIRT', 'HOODIE']:
                return ['S', 'M', 'L', 'XL']
            elif self.category == 'FOOTWEAR':
                return [str(size) for size in range(1, 13)]  # 1-12 US sizes
            elif self.category == 'PANTS':
                return [str(size) for size in range(28, 41, 2)]  # Waist sizes
            return None  # Default for categories without a defined size type





class ListingImage(models.Model):

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(upload_to = 'listing_images/')
    

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing,on_delete =  models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        highest_bid = self.listing.bids.order_by('-bid_amount').first()

        if highest_bid:
            minimum_bid = highest_bid + 1
        else:
            minimum_bid = self.listing.starting_price +1

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = 'watchlist')



       
class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name= 'comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)