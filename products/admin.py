from django.contrib import admin
from products.models import Product, Category, SubCategory, ProductImage

# Register your models here.

class ProductCategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    inlines = [ ProductImageInline, ]
    list_display = ['__str__', 'slug','title', 'price', 'image', 'category' ]
    search_fields = ["title", "description"]
   
    class Meta:
        model = Product

class CategoryInline(admin.TabularInline):
    model = Product
    extra = 1

class CategorySubInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = [  CategorySubInline, CategoryInline,]
    list_display = ['__str__','title' ]

    class Meta:
        model = Category

class SubCategoryInline(admin.TabularInline):
    model = Product
    extra = 1
class ProductSubCategoryAdmin(admin.ModelAdmin):
    inlines = [ SubCategoryInline,]
    list_display = ['__str__','title' ]

    class Meta:
        model = SubCategory





admin.site.register(Product, ProductAdmin)
admin.site.register(Category, ProductCategoryAdmin)
admin.site.register(SubCategory, ProductSubCategoryAdmin)