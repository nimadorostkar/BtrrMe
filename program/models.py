from django.db import models
from accounts.models import UserProfile, CoachProfile
from nutrition.models import Nutrition
from supplement.models import Supplement
import datetime
from datetime import datetime as date_time


class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    ref_id = models.CharField(max_length=256, null=True, blank=True)
    authority = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=4000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



class Workout_program(models.Model):
    saturday = models.JSONField(max_length=10000,null=True,blank=True)
    sunday = models.JSONField(max_length=10000, null=True, blank=True)
    monday = models.JSONField(max_length=10000, null=True, blank=True)
    tuesday = models.JSONField(max_length=10000, null=True, blank=True)
    wednesday = models.JSONField(max_length=10000, null=True, blank=True)
    thursday = models.JSONField(max_length=10000, null=True, blank=True)
    friday = models.JSONField(max_length=10000, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)




class Supplement_program(models.Model):
    description = models.TextField(max_length=4000, null=True, blank=True)
class Supplement_program_table(models.Model):
    supplement_program = models.ForeignKey(Supplement_program, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    time = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

class Nutrition_program(models.Model):
    description = models.TextField(max_length=4000, null=True, blank=True)
class Nutrition_program_table(models.Model):
    nutrition_program = models.ForeignKey(Nutrition_program, on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    time = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)






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

    status = models.CharField(max_length=60, default="new-and-payment-pending", choices=status_choices)
    type = models.CharField(max_length=60, default="workout", choices=type_choices)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    target = models.CharField(max_length=1000,null=True,blank=True)
    experience = models.CharField(max_length=1000,null=True,blank=True)
    description = models.TextField(max_length=4000,null=True,blank=True)
    duration_day = models.IntegerField()
    payment = models.ForeignKey(Transaction,on_delete=models.CASCADE,null=True,blank=True)
    nutrition_program = models.ForeignKey(Nutrition_program,on_delete=models.CASCADE,null=True,blank=True)
    workout_program = models.ForeignKey(Workout_program,on_delete=models.CASCADE,null=True,blank=True)
    supplement_program = models.ForeignKey(Supplement_program,on_delete=models.CASCADE,null=True,blank=True)
    program_receive_at = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) +' | '+ str(self.user) +' | '+ str(self.coach) +' | '+ str(self.created_at)

    def expired(self):
        delta = datetime.date.today() - self.program_receive_at
        if delta.days > self.duration_day:
            return True
        else:
            return False

    def remaining_days(self):
        today = date_time.now().date()
        elapsed_days = (today - self.program_receive_at).days
        remaining_days = self.duration_day - elapsed_days
        if remaining_days <= 0:
            self.status = "expired"
            self.save()
        return remaining_days