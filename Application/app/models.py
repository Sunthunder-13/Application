from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Sale(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.product_name

class BadOrder(models.Model):
    transaction_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.transaction_id} - {self.product_name}"

class Inventory(models.Model):
    product_name = models.CharField(max_length=255)
    stock = models.IntegerField()
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    arrival_date = models.DateField(default=timezone.now)
    shelf_life = models.PositiveIntegerField(default=7)  # in days
    estimated_expiration_date = models.DateField(blank=True, null=True)
    estimated_expiration_week = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='Fresh')
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Ensure arrival_date is a date object
        arrival_date = self.arrival_date
        if isinstance(arrival_date, str):
            try:
                arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d").date()
            except Exception:
                arrival_date = timezone.localdate()
        # Calculate estimated_expiration_date
        if arrival_date and self.shelf_life:
            self.arrival_date = arrival_date
            self.estimated_expiration_date = arrival_date + timedelta(days=self.shelf_life)
            # --- Set estimated_expiration_week as "1st week of January" etc ---
            exp_date = self.estimated_expiration_date
            week_num = ((exp_date.day - 1) // 7) + 1
            week_suffix = {1: "1st", 2: "2nd", 3: "3rd"}.get(week_num, f"{week_num}th")
            month_name = exp_date.strftime("%B")
            self.estimated_expiration_week = f"{week_suffix} week of {month_name}"
            # --- Status logic ---
            today = timezone.localdate()
            if self.estimated_expiration_date < today:
                self.status = 'Expired'
            elif (self.estimated_expiration_date - today).days <= 7:
                self.status = 'Near Expiry'
            else:
                self.status = 'Fresh'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.product_name}"

class Expense(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.description}"


