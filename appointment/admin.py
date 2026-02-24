from django.contrib import admin
from .models import (
    ServiceCategory , Service , Appointment , TimeSlot,
Holiday
)



@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'order', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active' , 'is_featured' , 'created_at']
    search_fields = ['id','name' , 'id' , 'description']
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active' , 'is_featured']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id','name', 'category', 'price', 'discount_price',
        'is_active', 'is_featured', 'view_count', 'booking_count' , 'rating'
    ]
    search_fields = ['id','name', 'category__name']
    list_editable = ['price', 'discount_price', 'is_active', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    readonly_fields = ['view_count', 'booking_count', 'rating']

    def get_final_price(self, obj):
        return obj.get_final_price()
    get_final_price.short_description = 'Final Price'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','customer', 'service', 'staff', 'status',
                    'is_paid', 'created_at' , 'updated_at' ]
    list_filter = ['id','status', 'is_paid', 'appointment_date', 'created_at' , 'updated_at']
    search_fields = ['id','customer__username', 'customer__phone', 'service__name']
    raw_id_fields = ['customer', 'staff']
    list_editable = ['status', 'is_paid']
    date_hierarchy = 'appointment_date'

    fieldsets = (
        ('reserve', {
            'fields': ('customer', 'service', 'staff')
        }),
        ('time', {
            'fields': ('appointment_date', 'appointment_time', 'end_time')
        }),
        ('notes', {
            'fields': ('notes', 'staff_notes')
        }),
        ('status', {
            'fields': ('status', 'total_price', 'is_paid','payment_date','payment_method')
        }),
        ('reminder', {
            'fields': ('reminder_sent', 'reminder_sent_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['staff', 'weekday', 'start_time', 'end_time', 'is_available']
    list_filter = ['weekday', 'is_available']
    search_fields = ['staff__username']
    list_editable = ['is_available']



@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'is_active']
    list_filter = ['is_active', 'date']
    search_fields = ['name']
    list_editable = ['is_active']
    date_hierarchy = 'date'
