from django.contrib import admin
from products.models import Product, Category, SubCategory,MoreImages, SubSubCategory, Brand

# Register your models here.

class ProductCategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = MoreImages
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
class SubCategorySubInline(admin.TabularInline):
    model = SubSubCategory
    extra = 1

class ProductSubCategoryAdmin(admin.ModelAdmin):
    inlines = [ SubCategorySubInline ,]
    list_display = ['__str__','title' ]

    class Meta:
        model = SubCategory





admin.site.register(Product, ProductAdmin)
admin.site.register(Category, ProductCategoryAdmin)
admin.site.register(SubCategory, ProductSubCategoryAdmin)
admin.site.register(SubSubCategory)
admin.site.register(Brand)