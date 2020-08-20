from django.db import models
import constants

class TweetSchema(models.Model):
    class Meta:
        ordering = ('tweet_create_time',)
        db_table = 'tweets'
        indexes = [
            models.Index(fields=['tweet_external_id', 'tweet_create_time'])
        ]

    status_values = {constants.status_active: 'A', constants.status_deleted: 'D'}
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    modified_on = models.DateTimeField(null=False, auto_now=True)
    status = models.CharField(null=False, max_length=3, default='A')

    def get_status(self):
        if  self.status == 'A':
            return constants.status_active
        elif  self.status == 'D':
            return constants.status_deleted

    #fields
    tweet_create_time = models.DateTimeField(null=False)
    screen_name = models.CharField(null=False, max_length=255, blank=False)
    tweet_external_id = models.CharField(null=True, max_length=255, blank=False, unique=True)
    full_text = models.TextField(null=False, blank=False)