from django.contrib import admin
from program.models import Program, Program_payment


class Program_paymentInline(admin.TabularInline):
    model = Program_payment
    extra = 1

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'coach', 'status', 'type', 'created_at')
    inlines = [Program_paymentInline]
admin.site.register(Program, ProgramAdmin)

