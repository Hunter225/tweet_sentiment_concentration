from django.db import models
import constants

class SuggestionSchema(models.Model):
    class Meta:
        ordering = ('created_on',)
        db_table = 'suggestions'

    status_values = {constants.status_active: 'A', constants.status_deleted: 'D'}
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    modified_on = models.DateTimeField(null=False, auto_now=True)
    status = models.CharField(null=False, max_length=3, default='A')

    def get_status(self):
        if  self.status == 'A':
            return constants.status_active
        elif  self.status == 'D':
            return constants.status_deleted

    suggestion_date = models.DateField(null=False, blank=False)
    previous_concentraion = models.FloatField(null=False, blank=False)
    current_concentraion = models.FloatField(null=False, blank=False)
    suggestion = models.IntegerField(null=False, blank=False)