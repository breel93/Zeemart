from django.db.models import Q
from random import randint
import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from zeemart.utils import unique_slug_generator
from django.db.models import Count
# Create your models here.



# category



                

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )


# category
class Category(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    slug         = models.SlugField(blank=True,unique=True)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)

    def get_category_url(self):
        return reverse("product:category-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.slug
    
    
    def get_products(self):
        return Product.objects.filter(category__title = self.title)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)



#  subcategory
class SubCategory(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    slug         = models.SlugField(blank=True,unique=True)
    category     = models.ForeignKey(Category,default="", blank=True, null=True, on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)

    def get_subcategory_url(self):
        return reverse("product:subcategory-detail", kwargs={"slug": self.category, "sub_slug": self.slug })
    
    def __str__(self):
        return self.slug
    
    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
    
def subcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(subcategory_pre_save_receiver, sender=SubCategory) 

#  sub-subcategory
class SubSubCategory(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    slug         = models.SlugField(blank=True,unique=True)
    category     = models.ForeignKey(Category,default="", blank=True, null=True, on_delete=models.CASCADE)
    subcategory  = models.ForeignKey(SubCategory,default="", blank=True, null=True, on_delete=models.CASCADE)
    image        = models.ImageField(upload_to='products/', null=True, blank=True)


    def get_subsubcategory_url(self):
        return reverse("product:subsubcategory-detail", kwargs={"slug": self.category, "sub_slug": self.subcategory ,"subsub_slug":self.slug })
    
    def __str__(self):
        return self.slug
    
    class Meta:
        verbose_name = 'SubSubCategory'
        verbose_name_plural = 'SubSubCategories'
    
def subsubcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(subsubcategory_pre_save_receiver, sender=SubSubCategory) 


class Brand(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    slug         = models.SlugField(blank=True,unique=True)
    image        = models.ImageField(upload_to='products/', null=True, blank=True)


    def get_brand_url(self):
        return reverse("product:brand-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.slug
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
    
def brand_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(brand_pre_save_receiver, sender=Brand) 





class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups =( Q(title__icontains=query) | 
                  Q(description__icontains=query)|
                  Q(tag__title__icontains=query)|
                  Q(category__title__icontains=query) )
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None


    def search(self,query):
        # lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().active().search(query)

class Product(models.Model): 
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places = 0, max_digits=10,default=0.00)
    old_price   = models.DecimalField(decimal_places = 0, max_digits=10, default=0.00, null=True, blank=True)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    category    = models.ForeignKey(Category, default="", related_name='Category', blank=True, null=True, on_delete=models.CASCADE)
    subcategory    = models.ForeignKey(SubCategory,default="", related_name='SubCategory', blank=True, null=True, on_delete=models.CASCADE)
    subsubcategory    = models.ForeignKey(SubSubCategory,default="", related_name='SubSubCategory', blank=True, null=True, on_delete=models.CASCADE)
    brand         = models.ForeignKey(Brand, default="",related_name='Brand', blank=True, null=True, on_delete=models.CASCADE)

  

    objects = ProductManager()

    def get_absolute_url(self):

        return reverse("product:product-details",kwargs={"slug":self.slug})
        
        # return "/products/{slug}".format(slug=self.slug)

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title
    
    



def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)

class MoreImages(models.Model):
    # user = models.ForeignKey(User)
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        verbose_name = 'MoreImage'
        verbose_name_plural = 'MoreImages'
