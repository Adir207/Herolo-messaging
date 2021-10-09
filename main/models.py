from django.db import models

# Create your models here.
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.PositiveIntegerField()
    reciver_id = models.PositiveIntegerField()
    subject = models.CharField(max_length=300)
    message_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return 'message_id: ' + str(self.message_id) + ' sender_id: ' + str(self.sender_id) + ' reciver_id: ' + str(self.reciver_id) + ' subject: ' + self.subject + ' message_text: ' + self.message_text + ' creation_date: ' + str(self.creation_date) + ' is_read: ' + str(self.is_read)
