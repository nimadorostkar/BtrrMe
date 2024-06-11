from django.db import models
from accounts.models import UserProfile, CoachProfile
from nutrition.models import Nutrition



class Workout_program(models.Model):
    saturday = models.CharField(max_length=1000,null=True,blank=True)
    sunday = models.CharField(max_length=1000, null=True, blank=True)
    monday = models.CharField(max_length=1000, null=True, blank=True)
    tuesday = models.CharField(max_length=1000, null=True, blank=True)
    wednesday = models.CharField(max_length=1000, null=True, blank=True)
    thursday = models.CharField(max_length=1000, null=True, blank=True)
    friday = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.id)




class Program_payment(models.Model):
    approved = models.BooleanField(default=False)
    description = models.TextField(max_length=4000, null=True, blank=True)
    image = models.ImageField(upload_to="payment", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id) +' | ' + str(self.program.user) + ' | ' + str(self.program.coach)



class Nutrition_program(models.Model):
    description = models.TextField(max_length=4000, null=True, blank=True)
class Nutrition_program_table(models.Model):
    nutrition_program = models.ForeignKey(Nutrition_program, on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    time = models.CharField(max_length=100)



class Program(models.Model):
    status_choices = (("cancelled", "cancelled"),
                      ("expired","expired"),
                      ("paid-and-waiting-for-program","paid-and-waiting-for-program"),
                      ("new-and-payment-pending","new-and-payment-pending"),
                      ("completed","completed"))

    type_choices = (("nutrition", "nutrition"),
                    ("workout", "workout"),
                    ("supplement", "supplement"),
                    ("full", "full"))

    status = models.CharField(max_length=40, default="new-and-payment-pending", choices=status_choices)
    type = models.CharField(max_length=40, default="workout", choices=type_choices)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    target = models.CharField(max_length=1000,null=True,blank=True)
    experience = models.CharField(max_length=1000,null=True,blank=True)
    description = models.TextField(max_length=4000,null=True,blank=True)
    duration_day = models.IntegerField(default=45)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    payment = models.ForeignKey(Program_payment, on_delete=models.CASCADE)
    nutrition_program = models.ForeignKey(Nutrition_program, on_delete=models.CASCADE)
    workout_program = models.ForeignKey(Workout_program, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) +' | '+ str(self.user) +' | '+ str(self.coach) +' | '+ str(self.created_at)







