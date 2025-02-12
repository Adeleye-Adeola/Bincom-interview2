from django.db import models

# Create your models here.

class AnnouncedPUResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    polling_unit_uniqueid = models.IntegerField()
    party_abbreviation = models.CharField(max_length=10)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '_announced_pu_results'  # I used this to tell Django to use the existing table I imported

class LGAS(models.Model):
    lga_id = models.AutoField(primary_key=True)
    lga_name = models.CharField(max_length=100)

    class Meta:
        db_table = "_lga"

class PollingUnits(models.Model):
    polling_unit_id = models.AutoField(primary_key=True)
    lga = models.ForeignKey(LGAS, on_delete=models.CASCADE)
    polling_unit_name = models.CharField(max_length=100)

    class Meta:
        db_table = "_polling_unit"





class Party(models.Model):
    partyid = models.AutoField(primary_key=True)
    partyname = models.CharField(max_length=10)

    class Meta:
        db_table = "_party"
