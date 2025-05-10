from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Ward, BedType, Bed

# Register Days model so that days can be added in the admin panel
admin.site.register(Day)

class UserModel(UserAdmin):
    list_display = ['username', 'email', 'user_type']
admin.site.register(CustomUser, UserModel)

admin.site.register(Specialization)

# ✅ Customizing DoctorReg in admin panel
class DoctorRegAdmin(admin.ModelAdmin):
    list_display = ['admin', 'mobilenumber', 'specialization_id', 'fee']
    filter_horizontal = ('available_days',)  # ✅ Allows multiple selections in a better UI

admin.site.register(DoctorReg, DoctorRegAdmin)

admin.site.register(Appointment)
admin.site.register(Page)

# Register the bed management models
@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(BedType)
class BedTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'ward', 'bed_type', 'is_occupied')
    list_filter = ('ward', 'bed_type', 'is_occupied')
    search_fields = ('bed_number',)



# Register the bed management models
