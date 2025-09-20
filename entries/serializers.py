from rest_framework import serializers
from .models import LogEntries
class logSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntries
        # fields = ['user']
        fields = '__all__'