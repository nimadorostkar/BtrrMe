from django.contrib import admin
from program.models import Program,Program_payment,Nutrition_program_table,Nutrition_program,Workout_program,Supplement_program_table,Supplement_program


class Workout_programAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
admin.site.register(Workout_program, Workout_programAdmin)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'coach', 'status', 'type', 'created_at')
admin.site.register(Program, ProgramAdmin)


class Program_paymentAdmin(admin.ModelAdmin):
    list_display = ('id','approved', 'created_at')
admin.site.register(Program_payment, Program_paymentAdmin)

class Nutrition_program_tableInline(admin.TabularInline):
    model = Nutrition_program_table
    extra = 1
class Nutrition_programAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    inlines = [Nutrition_program_tableInline]
admin.site.register(Nutrition_program, Nutrition_programAdmin)



class Supplement_program_tableInline(admin.TabularInline):
    model = Supplement_program_table
    extra = 1
class Supplement_programAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    inlines = [Supplement_program_tableInline]
admin.site.register(Supplement_program, Supplement_programAdmin)




