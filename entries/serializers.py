from rest_framework import serializers
from .models import LogEntries

class MyResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntries
        fields = '__all__' # Or specify a list of fields