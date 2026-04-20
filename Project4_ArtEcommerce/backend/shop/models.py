from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        #If this image is being set as the main Image
        if self.is_main:
            # unset all other images for this product
            ProductImage.objects.filter(
                product=self.product,
                is_main=True
            ).update(is_main=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        was_main = self.is_main
        product = self.product

        super().delete(*args, **kwargs)

        # If we deleted the main image → assign a new one
        if was_main:
            next_image = product.images.first()
            if next_image:
                next_image.is_main = True
                next_image.save()

    def __str__(self):
        suffix = " (MAIN)" if self.is_main else ""
        return f"{self.product.title} - Image {self.id}{suffix}"

class Order(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
