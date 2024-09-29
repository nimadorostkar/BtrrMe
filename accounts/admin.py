from django.contrib import admin
from accounts.models import User, CoachProfile, UserProfile, Gallery, Certificate,BodyVersion, WorkExperience

class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user_type', 'created_at', 'is_profile_fill')
admin.site.register(User, UserAdmin)



admin.site.register(UserProfile)
admin.site.register(CoachProfile)
admin.site.register(WorkExperience)
admin.site.register(Gallery)
admin.site.register(Certificate)
admin.site.register(BodyVersion)