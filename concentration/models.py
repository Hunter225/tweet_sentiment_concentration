from django.db import models
import constants

class ConcentrationSchema(models.Model):
    class Meta:
        ordering = ('created_on',)
        db_table = 'concentrations'

    status_values = {constants.status_active: 'A', constants.status_deleted: 'D'}
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    modified_on = models.DateTimeField(null=False, auto_now=True)
    status = models.CharField(null=False, max_length=3, default='A')

    def get_status(self):
        if  self.status == 'A':
            return constants.status_active
        elif  self.status == 'D':
            return constants.status_deleted

    calculation_date = models.DateField(null=False, blank=False)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    concentration = models.FloatField(null=False, blank=False)
    word_frequency = models.TextField(null=False, blank=False)
    day_of_week = models.IntegerField(null=False, blank=False)
