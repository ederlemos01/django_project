from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id","title", "description", "banner", "location", "start_datetime", "end_datetime", "owner"]
        read_only_fields = ['owner']