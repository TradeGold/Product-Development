from django.db import models
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    product_category = models.CharField(max_length=100)
    product_category_image = models.ImageField(upload_to='category')
    def __str__(self):
        return self.product_category

class Product(models.Model):
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.CharField(max_length=200)
    product_short_description = models.TextField(max_length=150)
    product_long_description = models.TextField(max_length=300)
    image1 = models.ImageField(upload_to='product')
    image2 = models.FileField(upload_to='product', blank=True, null=True)
    def __str__(self):
        return self.product_name
class Today_Special(models.Model):
    product_1 = models.ForeignKey(Product, related_name='product1', on_delete=models.CASCADE)
    product_2 = models.ForeignKey(Product,related_name='product2',on_delete=models.CASCADE)
    product_3 = models.ForeignKey(Product,related_name='product3', on_delete=models.CASCADE)
class Youtube_Link(models.Model):
    Youtube_Link = models.CharField(max_length=9000)
class Featured_product_of_month(models.Model):
    product_of_month = models.ForeignKey(Product,on_delete=models.CASCADE)

class New(models.Model):
    recepie_name = models.CharField(max_length=200)
    recepie_description = models.TextField(max_length=500)
    recepie_ingredients = models.TextField(max_length=5000,help_text="Use ',' to seperate ingredients")
    recepie_direction = models.TextField(max_length=10000)
    final_image = models.ImageField(upload_to='recepie')

    def recepie_ingredient_list(self):
        return self.recepie_ingredients.split(',')

    def __str__(self):
        return self.recepie_name
class FAQ(models.Model):
    question = models.CharField(max_length=5000)
    answer = models.TextField(max_length=15000)
class login_register(models.Model):
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_no=models.CharField(max_length=10)
    email_address = models.EmailField()
    password = models.CharField(max_length=40)
    date_registered = models.DateField(default=timezone.now())

    def __str__(self):
        return self.fullname

class review(models.Model):
    user = models.ForeignKey(login_register,on_delete=models.CASCADE)
    review = models.TextField(max_length=110)
    reviewdate = models.DateField()

class add_to_cart(models.Model):
    cartproduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    cartuser = models.ForeignKey(login_register,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField(default="No description")
    cake_description = models.CharField(max_length=400, default="Not a cake!")
    create_date = models.DateField(default=timezone.now())

class guestcart(models.Model):
    cartproduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    guestuser = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    description = models.TextField(default="No description")
    cake_description = models.CharField(max_length=400,default="Not a cake!")
    create_date = models.DateField(default=timezone.now())
class email_verification(models.Model):
    user = models.OneToOneField(login_register, on_delete=models.CASCADE)
    token = models.CharField(max_length=250)
    verify = models.BooleanField(default=False)
class checkout_order(models.Model):
    order_choice=(
        ('Pending','Pending'),
        ('Accepted', 'Accepted'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancel Order', 'Cancel Order'),
    )
    userid = models.ForeignKey(login_register, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordername = models.CharField(max_length=200)
    deliveryaddress = models.CharField(max_length=200)
    deliverydate = models.DateField()
    phoneno = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    description = models.CharField(max_length=400)
    cake_description = models.CharField(max_length=400)
    payment_method = models.CharField(max_length=150, default="Home Delivery")
    order_status = models.CharField(max_length=30,choices=order_choice,default="Pending")

class temporary_order_store(models.Model):
    userid = models.ForeignKey(login_register,on_delete=models.CASCADE)
    username = models.CharField(max_length=400)
    deliveryaddress = models.CharField(max_length=400)
    deliverydate = models.DateField()
    phoneno = models.CharField(max_length=10)

class VideoComment(models.Model):
    productid = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment_date = models.CharField(max_length=400)
    comment_by = models.CharField(max_length=400)
    comment = models.CharField(max_length=900, default="This is great")


