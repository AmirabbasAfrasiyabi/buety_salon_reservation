from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator ,RegexValidator
from django.utils.text import slugify



# Create your models here.

class Brand(models.Model):
    COUNTRY_CHOICES = (
        ('IR', 'Iran'),
        ('IT', 'Italy'),
        ('FR', 'France'),
        ('KR', 'South Korea'),
        ('TR', 'Turkey'),
        ('US', 'United States'),
        ('DE', 'Germany'),
        ('other' , 'Other'),
    )

    name = models.CharField(max_length=100 , unique=True , verbose_name="brand")
    slug = models.SlugField(max_length=100, unique=True , verbose_name="slug")
    # logo = models.ImageField(upload_to="brands/", null=True , blank=True , verbose_name="logo")
    description = models.TextField(blank=True , null=True , verbose_name="description")

    country = models.CharField(choices=COUNTRY_CHOICES,blank=True,null=True)
    website = models.URLField(blank=True)

    is_active = models.BooleanField(default=True , verbose_name="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100 , unique=True , verbose_name="category")
    slug = models.SlugField(max_length=100, unique=True , verbose_name="slug")
    parent = models.ForeignKey('self',on_delete=models.CASCADE,related_name='children',null=True,blank=True,verbose_name="Parent Category")
    description = models.TextField(blank=True , null=True , verbose_name="description")
    # image = models.ImageField(upload_to="categories/", null=True , blank=True , verbose_name="image")
    icon = models.CharField(max_length=100 , blank=True , null=True , verbose_name="icon")
    order = models.PositiveIntegerField(blank=True , null=True , verbose_name="order")
    is_active = models.BooleanField(default=True , verbose_name="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['name','order']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_all_children(self):
        children = list(self.children.all())
        for child in list(children):
            children.extend(child.get_all_children())
        return children

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):

    Sku_validator = RegexValidator(
        regex=r'^d{5} - d{5}',
    )

    Ingredient_Choices = (
        ('Paraben_free', 'Paraben_free'),
        ('Sulfate_free', 'Sulfate_free'),
        ('Organic', 'Organic'),
        ('Vitamin_C', 'Vitamin_C'),
        ('Aloe_Vera', 'Aloe_Vera'),
        ('Collagen', 'Collagen'),
        ('Other', 'Other'),
    )

    HowToUse_Choices = (
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('After_Bath', 'After_Bath'),
        ('Before_Sleep', 'Before_Sleep'),
        ('Other', 'Other'),
    )

    Feature_Choices = (
        ('Water_Proof', 'Water_Proof'),
        ('Long_Lasting', 'Long_Lasting'),
        ('Anti_Allergy', 'Anti_Allergy'),
        ('fast_absorb', 'fast_absorb'),
        ('matter', 'matter'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=100 , unique=True , verbose_name="product")
    slug = models.SlugField(max_length=100, unique=True , verbose_name="slug")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',null=True,blank=True,verbose_name="category")
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="brand")
    description = models.TextField(blank=True , null=True , verbose_name="description")

    price = models.DecimalField(max_digits=10, decimal_places=0 , validators=[MinValueValidator(0)], verbose_name="price")
    discount_price = models.DecimalField(max_digits=10 , decimal_places=0 , blank=True , null=True , validators=[MinValueValidator(0)] , verbose_name="discount price")
    cost_price = models.DecimalField(max_digits=10 , decimal_places=0 , blank=True , null=True , validators=[MinValueValidator(0)] , verbose_name="cost price")

    #موجودی
    stock = models.PositiveIntegerField(default=0,blank=True , null=True , verbose_name="stock")
    low_stock_threshold = models.PositiveIntegerField(default=10  , verbose_name="low stock threshold")

    #ability
    sku = models.CharField(unique=True,validators=[Sku_validator])
    barcode = models.CharField(max_length=100,blank=True,verbose_name='barcode')
    weight = models.DecimalField(max_digits=8 , decimal_places=2 , blank=True , null=True ,  verbose_name="weight")
    volume = models.DecimalField(max_digits=8 , decimal_places=2 , blank=True , null=True , verbose_name="volume")

    #image
    # main_image = models.ImageField(upload_to='products/%Y/%m/',verbose_name="main image")


    #ویژگی محصول

    ingredients = models.CharField(choices=Ingredient_Choices,blank=True,null=True , verbose_name="ingredients")
    how_to_use = models.CharField(choices=HowToUse_Choices,blank=True,null=True , verbose_name="how to use")
    features = models.CharField(choices=Feature_Choices,blank=True,null=True , verbose_name="features")

    SKIN_TYPE_CHOICES = (
        ('all', 'all'),
        ('normal', 'normal'),
        ('dry', 'dry'),
        ('oily', 'oily'),
        ('combination', 'combination'),
        ('sensitive', 'sensitive'),
    )

    suitable_for_skin = models.CharField(
        max_length=20,
        choices=SKIN_TYPE_CHOICES,
        default='all',
        verbose_name='suitable skin type',
    )

    view_count = models.PositiveIntegerField(default=0 , blank=True , null=True , verbose_name="views")
    sales_count = models.PositiveIntegerField(default=0 , blank=True , null=True , verbose_name="sales")
    rating = models.DecimalField(max_digits=3 , decimal_places=2 , blank=True , null=True ,
                                 default=0.00,validators=[MinValueValidator(0), MaxValueValidator(5)],verbose_name="rating")

    rating_count = models.PositiveIntegerField(default=0 , blank=True , null=True , verbose_name="rating")


    #status
    is_active = models.BooleanField(default=True , verbose_name="active")
    is_featured = models.BooleanField(default=True , verbose_name="featured")
    is_available = models.BooleanField(default=True , verbose_name="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ['-created_at' , '-is_featured']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['-sales_count']),
        ]

    def __str__(self):
        return self.name

    def get_final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_discount_percentage(self):
        if self.discount_price and self.price > 0:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0

    def is_in_stock(self):
        return self.stock > 0

    def is_low_stock(self):
        return 0 < self.stock <= self.low_stock_threshold

    def get_profit_margin(self):
        if self.cost_price and self.cost_price > 0:
            final_price = self.get_final_price()
            profit = ((final_price - self.cost_price) / self.cost_price) * 100
            return round(profit, 2)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images',verbose_name='product')
    # image = models.ImageField(upload_to='products/%Y/%m/',blank=True,verbose_name='image')
    alt_text = models.CharField(max_length=255,blank=True,verbose_name='alt text')
    order = models.PositiveIntegerField(default=0 , blank=True , null=True , verbose_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"
        ordering = ['order']

    def __str__(self):
        return self.product.name

class ProductVariant(models.Model):

    Sku_validator = RegexValidator(
        regex=r'^d{5} - d{5}',
    )
    ColorCode_validator = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='variations',verbose_name='product')
    name = models.CharField(max_length=255,blank=True,unique=True,verbose_name='name')
    sku = models.CharField(unique=True, validators=[Sku_validator])
    color_code = models.CharField(validators=[ColorCode_validator] , verbose_name='color code')
    price_adjustment = models.DecimalField(max_digits=10 , decimal_places=0 ,default=0,verbose_name='price adjustment')
    stock = models.PositiveIntegerField(default=0 , blank=True , null=True , verbose_name="stock")

    # image = models.ImageField(upload_to='products_variants/',blank=True,verbose_name='image')

    is_active = models.BooleanField(default=True , verbose_name="active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "variation"
        verbose_name_plural = "variations"
        ordering = ['-created_at' , 'is_active']

    def __str__(self):
        return self.product.name

    def get_final_price(self):
        base_price = self.product.get_final_price()
        return base_price + self.price_adjustment


class Tag(models.Model):

    name = models.CharField(max_length=255,blank=True,unique=True,verbose_name='name')
    slug = models.SlugField(max_length=255,blank=True,unique=True,verbose_name='slug')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='tags',verbose_name='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ['-created_at' , 'updated_at']

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='wishlists',verbose_name='User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='wishlists',verbose_name='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "wishlist"
        verbose_name_plural = "wishlists"
        ordering = ['-created_at' , 'updated_at']
        unique_together = ('user','product')

    def __str__(self):
        return self.product.name

class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='views',verbose_name='product')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='views',verbose_name='user')
    ip_address = models.GenericIPAddressField(verbose_name='IP address')
    session_key = models.CharField(max_length=255,blank=True,verbose_name='session key')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "view"
        verbose_name_plural = "views"
        ordering = ['-created_at' , 'updated_at']
        indexes = [
            models.Index(fields=['product' , '-created_at']),
        ]
    def __str__(self):
        return self.product.name