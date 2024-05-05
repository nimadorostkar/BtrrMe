from django.db import models
from accounts.models import User


class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)

    ''' 
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'],name='unique_1' ),
            models.UniqueConstraint(fields=['user2', 'user1'],name='unique_2')
        ]
    '''

    class Meta:
        unique_together = [('user1', 'user2')]

    def __str__(self):
        return str(self.user1) + " | " + str(self.user2)




class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.time)

