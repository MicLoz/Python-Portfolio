from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title_display', 'price', 'created_at')
    search_fields = ('title',)
    inlines = [ProductImageInline]

    def title_display(self, obj):
        return f"Product: {obj.title}"

    def save_related(self, request, form, formsets, change):
        """
        Ensures only one main image per product after admin save.
        This keeps UI consistent and avoids confusion during bulk edits.
        """
        super().save_related(request, form, formsets, change)

        product = form.instance

        main_images = product.images.filter(is_main=True)

        if main_images.count() > 1:
            # keep the last selected one as main
            keep = main_images.last()
            main_images.exclude(id=keep.id).update(is_main=False)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_display', 'is_main')

    def product_display(self, obj):
        suffix = " (MAIN) " if obj.is_main else ""
        return f"{obj.product.title} - Image {obj.id}{suffix}"

    product_display.short_description = 'Image'
