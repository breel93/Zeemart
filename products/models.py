from django.db.models import Q
import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from zeemart.utils import unique_slug_generator
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
    price       = models.DecimalField(decimal_places = 2, max_digits=20,default=0.00)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    category    = models.ForeignKey(Category, default="", related_name='Category', blank=True, null=True, on_delete=models.CASCADE)
    subcategory    = models.ForeignKey(SubCategory,default="", related_name='SubCategory', blank=True, null=True, on_delete=models.CASCADE)
    

  

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

class ProductImage(models.Model):
    # user = models.ForeignKey(User)
    property = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)


