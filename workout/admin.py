from django.contrib import admin
from workout.models import MainMuscle, Muscle, Equipment, Workout
from ckeditor.widgets import CKEditorWidget
from django import forms
from import_export.admin import ImportExportModelAdmin



class MainMuscleAdmin(admin.ModelAdmin):
    list_display = ('name','english_name')
admin.site.register(MainMuscle, MainMuscleAdmin)


class MuscleAdmin(admin.ModelAdmin):
    list_display = ('name','english_name','main_muscle')
admin.site.register(Muscle, MuscleAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Equipment, EquipmentAdmin)


class WorkoutAdmin(ImportExportModelAdmin):
    list_display = ('img','name','english_name','motion_status','type','id')
    list_filter = ("type", "muscle", "equipment","place")
    search_fields = ['name', 'english_name', 'description']
admin.site.register(Workout, WorkoutAdmin)