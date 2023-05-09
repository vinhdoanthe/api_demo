from rest_framework import serializers
from .models import Task


class WorkRequestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['number_of_items']
