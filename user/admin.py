from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User , CustomerProfile , StaffProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'gender',
                    'created_at', 'updated_at', 'is_verified')
    list_filter = ('role', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    list_editable = ('role', 'is_verified')


    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Information', {
            'fields': ('phone', 'role', 'gender', 'birthday')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postcode')
        }),
        ('Settings', {
            'fields': ('is_verified', 'receive_notification_code')
        }),
    )



    @admin.register(CustomerProfile)
    class CustomerProfileAdmin(admin.ModelAdmin):
        list_display = ['user','skin_type','hair_type','hair_length','hair_color',
                        'total_reservations','last_reservation_date','created_at',]
        list_filter = ['skin_type','hair_type','hair_length','hair_color','is_vip',]
        search_fields = ['user__username','user__email','user__first_name','user__last_name',]
        readonly_fields = ['total_reservations', 'last_reservation_date',
                           'created_at', 'updated_at']

        fieldsets = (
            ('User Info', {
                'fields': ('user',)
            }),
            ('Appearance', {
                'fields': ('skin_type', 'hair_type', 'hair_length',
                           'hair_color', 'face_image', 'face_analysis_data')
            }),
            ('Reservation Info', {
                'fields': ('total_reservations', 'last_reservation_date', 'is_vip', 'notes')
            }),
            ('Notifications', {
                'fields': ('wants_sms_notifications', 'wants_email_notifications')
            }),
            ('Address', {
                'fields': ('address', 'city', 'state', 'postcode')
            }),
            ('Timestamps', {
                'fields': ('created_at', 'updated_at')
            }),
        )


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user','experience_years','rating','total_reviews',
                    'is_active','created_at' , 'updated_at']

    list_filter = ['is_active','experience_years','specialties']

    search_fields = ['user__username','user__email','user__first_name',
                    'user__last_name','specialties__name']


    list_editable = ['is_active']

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'is_active')
        }),
        ('Skills & Expertise', {
            'fields': ('specialties', 'certifications', 'experience_years', 'bio')
        }),
        ('Rating & Reviews', {
            'fields': ('rating', 'total_reviews')
        }),
        ('Working Hours', {
            'fields': ('working_hours',)
        }),
        ('Profile Image', {
            'fields': ('profile_image',)
        }),
    )