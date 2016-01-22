

import json

from rest_framework import serializers

from patients.models import Patient, Bed, Admission, Schedule


class BedSerializer(serializers.ModelSerializer):
    #displayName = serializers.ReadOnlyField()

    class Meta:
        model = Bed
        
        


        
class ScheduleSerializer(serializers.ModelSerializer):
    displayName = serializers.ReadOnlyField()
    #bed = serializers.PrimaryKeyRelatedField( read_only=True, many=True)
   
    class Meta:
        model = Schedule 

class PatientSerializer(serializers.ModelSerializer):
    displayName = serializers.ReadOnlyField()
    bed = serializers.PrimaryKeyRelatedField( read_only=True)
   
    class Meta:
        model = Patient 
        
        
class AdmissionSerializer(serializers.ModelSerializer):
    #displayName = serializers.ReadOnlyField()

    class Meta:
        model = Admission