from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Brand, Category, Product, ProductImage,
    ProductVariant, Tag, Wishlist, ProductView
)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name','country','is_active', 'created_at']
    list_filter = ['id','country','is_active','created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at',)
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Details', {
            'fields': ('country', 'website')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','parent','order','is_active', 'created_at','updated_at']
    list_filter = ['id','is_active','created_at','updated_at','parent']
    search_fields = ['name','slug','id']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at',)
    list_editable = ['is_active' , 'order' , 'parent']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['name', 'sku', 'color_code', 'price_adjustment', 'stock', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'brand', 'price_display',
        'stock_status', 'sales_count', 'rating',
        'is_active', 'is_featured'
    ]
    list_filter = [
        'is_active', 'is_featured', 'category',
        'brand','created_at'
    ]
    search_fields = ['name','category','brand','is_active' ]
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured']

    inlines = [ProductImageInline, ProductVariantInline]

    fieldsets = (
        ('Information', {
            'fields': ('name', 'slug', 'category', 'brand', 'description')
        }),
        ('Price', {
            'fields': (
                'price', 'discount_price', 'cost_price',
                'stock', 'low_stock_threshold'
            )
        }),
        ('Code', {
            'fields': ('sku', 'barcode')
        }),
        ('Specifications', {
            'fields': ('weight', 'volume'),
            'classes': ('collapse',)
        }),
        ('Ability', {
            'fields': (
                'ingredients', 'how_to_use', 'features',
            ),
            'classes': ('collapse',)
        }),

        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_available')
        }),
        ('Statistics', {
            'fields': ('view_count', 'sales_count', 'rating', 'rating_count'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        if obj.discount_price:
            return format_html(
                '<span style="text-decoration: line-through;">{}</span> '
                '<span style="color: red; font-weight: bold;">{}</span>',
                f"{obj.price:,}",
                f"{obj.discount_price:,}"
            )
        return f"{obj.price:,}"

    price_display.short_description = 'Price'

    def stock_status(self, obj):
        if obj.stock == 0:
            color = 'red'
            text = 'Unavailable'
        elif obj.is_low_stock():
            color = 'orange'
            text = f'less ({obj.stock})'
        else:
            color = 'green'
            text = f'price ({obj.stock})'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )

    stock_status.short_description = 'available'



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    raw_id_fields = ['user', 'product']


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'ip_address']
    raw_id_fields = ['product', 'user']
    date_hierarchy = 'created_at'