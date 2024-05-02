from django.contrib import admin
from workout.models import MainMuscle, Muscle, Equipment, Workout
from ckeditor.widgets import CKEditorWidget
from django import forms
from import_export.admin import ImportExportModelAdmin



class MainMuscleAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(MainMuscle, MainMuscleAdmin)


class MuscleAdmin(admin.ModelAdmin):
    list_display = ('name','main_muscle')
admin.site.register(Muscle, MuscleAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Equipment, EquipmentAdmin)


class WorkoutAdmin(ImportExportModelAdmin):
    list_display = ('name','muscle','motion_status','type')
admin.site.register(Workout, WorkoutAdmin)