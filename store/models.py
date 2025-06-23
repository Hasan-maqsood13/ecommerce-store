from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class Registration(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'), 
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username}     - {self.email} - {self.role}"    
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    
    # Parent category field — allows admin to choose category/subcategory
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text="Select a parent category if this is a subcategory"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

class Product(models.Model):
    PRODUCT_TAG_CHOICES = [
        ('featured', 'Featured'),
        ('on_sale', 'On Sale'),
        ('top_rated', 'Top Rated'),
        ('normal', 'Normal'),
        ('clearance', 'Clearance'),
        ('new_arrival', 'New Arrivals'),
        ('limited', 'Limited Quantities'),
        ('best_choice', 'The Best Choices'),
    ]

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        help_text="Select category or subcategory"
    )
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    tag = models.CharField(
        max_length=30,
        choices=PRODUCT_TAG_CHOICES,
        default='normal',
        help_text='Product label for homepage filtering'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carted_by')
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')  # prevent duplicate cart entries

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"