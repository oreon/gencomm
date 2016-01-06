

from rest_framework import serializers

from patients.models import Patient, Bed


class PatientSerializer(serializers.ModelSerializer):
    #displayName = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        
        
class BedSerializer(serializers.ModelSerializer):
    #displayName = serializers.ReadOnlyField()

    class Meta:
        model = Bed