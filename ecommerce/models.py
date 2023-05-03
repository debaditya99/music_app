from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('G','Guitar'),
    ('V','Voilin'),
    ('P','Piano'),
    ('T','Tabla'),
    ('D','Drum')
)

LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField() 
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default='S', max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, default='P', max_length=1)
    slug = models.SlugField()
    description = models.TextField(default="this is a test description")
    image = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    image4 = models.ImageField()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ecommerce:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("ecommerce:add-to-cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("ecommerce:remove-from-cart", kwargs={
            'slug': self.slug
        })

# links Order and Item. 
# One order can have multiple items.
# so we need a table named OrderItem for that
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

# order always needs to be associated with a user
# ordered if true will be visible as a shopping cart, otherwise in order history
# an Order can have multiple items
# an item can have multiple users. //kinda dumb that I wrote this. What explains ManyToMany
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20,blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField() 
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('Address', related_name="billing_address", on_delete=models.SET_NULL,blank=True, null=True)
    shipping_address = models.ForeignKey('Address', related_name="shipping_address", on_delete=models.SET_NULL,blank=True, null=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True, null=True)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL, blank=True, null=True)
    
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

COUNTRY_CHOICES = (
    ('IN','India'),
    ('NP','Nepal')
)

STATE_CHOICES = (
    ('DL','Delhi'),
    ('HR','Haryana'),
    ('PB','Punjab'),
    ('UP','Uttar Pradesh'),
    ('LK','Lucknow'),
    ('BH','Bihar'),
    ('BN','Bangalore'),
    ('MH','Maharastra')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(choices=COUNTRY_CHOICES, default='IN', max_length=2)
    state = models.CharField(choices=STATE_CHOICES, default='DL', max_length=4)
    zip = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

# # Create your models here.
# class Instruments(models.Model):
#     instrument_id = models.CharField(max_length=4,primary_key=True)
#     instrument_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.instrument_name

# class Product(models.Model):
#     product_id = models.CharField(max_length=11,primary_key=True)
#     product_name = models.CharField(max_length=100)
#     product_description = models.charField(max_length=400)
#     category = models.ForeignKey(Instruments, on_delete=models.CASCADE)
#     sub_category = models.CharField(max_length=100)
#     price = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     def __str__(self):
#         return self.product_name

# class Order(models.Model):
#     # user Id foreign key
#     # Product Id foreign key (how to handle multiple products in an order?)
#     # total amount of all products
#     order_id = models.AutoField(primary_key=True)
#     email = models.CharField(max_length=255)
#     phone = models.CharField(max_length=14)
#     total_price = models.IntegerField()
#     date = models.DateTimeField()
#     status = models.CharField(max_length=255)

# class order_products(models.Model):
#     order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    

# class delivery_details(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     address = models.CharField(max_length=500)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     zip_code = models.CharField(max_length=10)


# # class OrderUpdate(models.Model):

# class Contantus(models.Model):
#     email = models.EmailField()
#     address = models.CharField(max_length=500)

