from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator , RegexValidator
from django.utils import timezone
from datetime import datetime, timedelta

hex_color_validator = RegexValidator(
    regex=r'^[0-9A-Fa-f]{6}$',
    message='Color code must be exactly 6 hexadecimal characters (example: FF5733)'
)

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100 , unique=True , verbose_name='name')
    slug = models.SlugField(max_length=100, unique=True , verbose_name='slug')
    description = models.TextField(blank=True,verbose_name='description')
    icon = models.CharField(max_length=100,blank=True,verbose_name='icon')
    # image = models.ImageField(upload_to='service_categories/',null=True,blank=True,verbose_name='image')
    color_code = models.CharField(max_length=6,validators=[hex_color_validator],blank=True,verbose_name='Hex Color Code (without #)',)
    order = models.PositiveIntegerField(default=0,verbose_name='order')
    is_featured = models.BooleanField(default=False,verbose_name='is featured')
    is_active = models.BooleanField(default=True,verbose_name='active')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='updated at')

    class Meta:
        ordering = ['order']
        verbose_name = 'service category'
        verbose_name_plural = 'service categories'

    def __str__(self):
        return self.name

class Service(models.Model):

    category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,related_name='services',verbose_name='category')
    name = models.CharField(max_length=100,verbose_name='name')
    slug = models.SlugField(max_length=100,unique=True , verbose_name='slug')
    description = models.TextField(blank=True,verbose_name='description')

    #price
    price = models.DecimalField(max_digits=10,decimal_places=0,validators=[MinValueValidator(0)],verbose_name='price')
    discount_price = models.DecimalField(decimal_places=0,max_digits=10,blank=True,null=True,validators=[MinValueValidator(0)],verbose_name='discount price')
    duration = models.PositiveIntegerField(validators=[MinValueValidator(15)],verbose_name='duration')


    # image = models.ImageField(upload_to='services/%Y/%m/',null=True,blank=True,verbose_name='image')

    #count
    view_count = models.PositiveIntegerField(default=0,verbose_name='view count')
    booking_count = models.PositiveIntegerField(default=0,verbose_name='booking count')
    rating = models.DecimalField(decimal_places=0,max_digits=10,blank=True,null=True,verbose_name='rating')


    #status
    is_active = models.BooleanField(default=True,verbose_name='active')
    is_featured = models.BooleanField(default=False,verbose_name='is featured')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='updated at')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    def get_final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_discount_percentage(self):
        if self.discount_price and self.price > 0:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('in_progress','in_progress'),
        ('complete','complete'),
        ('cancelled','cancelled'),
        ('rejected','rejected'),
        ('no_show','no show'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('cash','cash'),
        ('cart','cart'),
        ('online','online'),
        ('wallet','wallet'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='customer',related_name='appointments_as_customer')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='staff',related_name='appointments_as_staff')
    service = models.ForeignKey(Service,on_delete=models.CASCADE,verbose_name='service')

    appointment_date = models.DateTimeField(default=timezone.now,verbose_name='appointment date')
    appointment_time = models.TimeField(blank=True,null=True,verbose_name='appointment time')
    end_time = models.TimeField(blank=True,null=True,verbose_name='end time')

    notes = models.TextField(blank=True,verbose_name='notes')
    staff_notes = models.TextField(blank=True,verbose_name='staff notes')

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending',verbose_name='status')
    total_price = models.DecimalField(decimal_places=0,max_digits=10,verbose_name='total price')
    is_paid = models.BooleanField(default=False,verbose_name='is paid')
    payment_date = models.DateTimeField(blank=True,null=True,verbose_name='payment date')
    payment_method = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,verbose_name='payment method')


    reminder_sent = models.BooleanField(default=False,verbose_name='reminder sent')
    reminder_sent_at = models.DateTimeField(blank=True,null=True,verbose_name='reminder sent at')

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='updated at')
    cancelled_at = models.DateTimeField(blank=True,null=True,verbose_name='cancelled at')

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        ordering = ['-appointment_date' , 'appointment_time']

        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['staff', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.customer.get_full_name()} - {self.service.name} - {self.appointment_date}"

    def save(self, *args, **kwargs):
        if not self.end_time and self.appointment_time:

            start = datetime.combine(self.appointment_date, self.appointment_time)
            end = start + timedelta(minutes=self.service.duration)
            self.end_time = end.time()

        if not self.total_price:
            self.total_price = self.service.get_final_price()
        super().save(*args, **kwargs)

    def can_cancel(self):
        if self.status in ['cancelled', 'completed', 'no_show']:
            return False

        appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time)
        if appointment_datetime < timezone.now():
            return False

        return True

    def get_status_badge_class(self):
        status_classes = {
            'pending': 'warning',
            'confirmed': 'info',
            'in_progress': 'primary',
            'completed': 'success',
            'cancelled': 'danger',
            'no_show': 'secondary',
        }
        return status_classes.get(self.status, 'secondary')

class TimeSlot(models.Model):
    WEEKDAYS_CHOICES = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    )

    staff = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='time_slots', limit_choices_to={'role': 'staff'}, verbose_name='staff')
    weekday  = models.IntegerField(choices=WEEKDAYS_CHOICES,verbose_name='weekday')
    start_time = models.TimeField(blank=True,null=True,verbose_name='start time')
    end_time = models.TimeField(blank=True,null=True,verbose_name='end time')
    is_available = models.BooleanField(default=False,verbose_name='is available')

    class Meta:
        verbose_name = 'time slot'
        verbose_name_plural = 'time slots'
        ordering = ['start_time' , 'weekday']
        unique_together = ('staff', 'weekday' , 'start_time')

    def __str__(self):
        return f"{self.staff.get_full_name()} - {self.get_weekday_display()} ({self.start_time} - {self.end_time})"


class Holiday(models.Model):
    name = models.CharField(max_length=100,verbose_name='holiday')
    date = models.DateField(unique=True,verbose_name='date')
    description = models.TextField(blank=True,verbose_name='description')
    is_active = models.BooleanField(default=True,verbose_name='is active')

    class Meta:
        verbose_name = 'holiday'
        verbose_name_plural = 'holidays'
        ordering = ['date']

    def __str__(self):
        return self.name