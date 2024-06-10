from django.db import models
from accounts.models import UserProfile, CoachProfile


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
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id) +' | '+ str(self.user) +' | '+ str(self.coach) +' | '+ str(self.created_at)




class Program_payment(models.Model):
    approved = models.BooleanField(default=False)
    description = models.TextField(max_length=4000, null=True, blank=True)
    image = models.ImageField(upload_to="payment", null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id) +' | ' + str(self.program.user) + ' | ' + str(self.program.coach)