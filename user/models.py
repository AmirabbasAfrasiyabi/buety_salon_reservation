from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    ROLE_CHOICES = (
        ('customer', 'customer'),
        ('admin', 'admin'),
        ('staff', 'staff'),
    )

    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    )

    phone_validator = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be in format: 09121234567"
    )

    email_validator = RegexValidator(
        regex=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        message='Enter a valid email address (example: example@gmail.com).'
    )

    PostalCode_validator = RegexValidator(
        regex=r'^d{5} - d{5}',
    )

    # اطلاعات پایه
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')


    email = models.CharField(
        max_length=254,
        unique=True,
        validators=[email_validator]
    )

    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_validator]
    )

    # آدرس
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(unique=True,
                                validators=[PostalCode_validator])

    # وضعیت‌ها
    is_verified = models.BooleanField(default=False)
    receive_notification_code = models.BooleanField(default=True)

    # تاریخ‌ها
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    @property
    def is_customer(self):
        return self.role == 'customer'

    @property
    def is_staff_member(self):
        return self.role == 'staff'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser



class CustomerProfile(models.Model):

    SKIN_TYPE_CHOICES = (
        ('normal', 'normal'),
        ('dry' , 'dry') ,
        ('oily' , 'oily') ,
        ('sensitive', 'sensitive'),
        ('combination' , 'combination'),
    )

    HAIR_TYPE_CHOICES = (
        ('normal', 'normal'),
        ('wavy', 'wavy'),
        ('curly', 'curly'),
        ('coily', 'coily'),
    )

    HAIR_LENGTH_CHOICES = (
        ('short', 'short'),
        ('medium', 'medium'),
        ('long', 'long'),
    )

    HAIR_COLOR_CHOICES = (
        ('black', 'black'),
        ('white', 'white'),
        ('red', 'red'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('purple', 'purple'),
        ('cyan', 'cyan'),
        ('magenta', 'magenta'),
        ('yellow', 'yellow'),
        ('cyan', 'cyan'),
        ('magenta', 'magenta'),
        ('yellow', 'yellow'),
        ('brown', 'brown'),
        ('blonde', 'blonde'),
        ('other', 'other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='customer_profile' , verbose_name='user')


    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES,blank=True,default='normal')
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPE_CHOICES,blank=True,default='normal')
    hair_color = models.CharField(max_length=20,choices=HAIR_COLOR_CHOICES, blank=True,default='black')
    hair_length = models.CharField(max_length=20, choices=HAIR_LENGTH_CHOICES, blank=True,default='short')


    face_image = models.ImageField(
        upload_to='faces/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='face_image'
    )

    face_analysis_data = models.JSONField(
        blank=True,
        null=True,
        verbose_name='face_analysis_data'
    )

    total_reservations = models.PositiveIntegerField(default=0 , verbose_name='total_reservations')
    last_reservation_date = models.DateTimeField(blank=True,null=True ,verbose_name='last_reservation_date')

    is_vip = models.BooleanField(default=False, verbose_name='is_vip')
    notes = models.TextField(blank=True,null=True,verbose_name='notes')

    wants_sms_notifications = models.BooleanField(default=False, verbose_name='wants_sms_notifications')
    wants_email_notifications = models.BooleanField(default=False, verbose_name='wants_email_notifications')

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'customer profile'
        verbose_name_plural = 'customer profiles'

    def __str__(self):
        return f"profile{self.user.get_full_name()}"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='staff_profile' , verbose_name='user')
    specialties = models.ManyToManyField( 'appointment.Service', blank=True,related_name='specialists',verbose_name='specialties')
    experience_years = models.PositiveIntegerField(default=0 , verbose_name='experience')
    bio = models.TextField(blank=True,null=True,verbose_name='bio')
    # profile_image = models.ImageField(upload_to='staff_profiles/%Y/%m/',blank=True,null=True,verbose_name='profile_image')
    working_hours = models.JSONField(default=dict,blank=True,null=True,verbose_name='working_hours')

    is_active = models.BooleanField(default=True, verbose_name='is_active')

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='rating')

    total_reviews = models.PositiveIntegerField(default=0 , verbose_name='total_reviews')
    certifications = models.JSONField(default=list,blank=True,verbose_name='certifications',)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff'

    def __str__(self):
        return self.user

    def update_rating(self, new_rating):

        total_score = self.rating * self.total_reviews
        self.total_reviews += 1
        self.rating = (total_score + new_rating) / self.total_reviews
        self.save()