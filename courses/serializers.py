from rest_framework import serializers
import utilities.serializers as utl_serializers
from . import models

class CourseCardSerializer(utl_serializers.ExtraFieldsModelSerializer):
    day_of_the_week = serializers.CharField(read_only=True,
                                            source='get_day_of_the_week')
    owner_name = serializers.CharField(read_only=True,
                                        source='get_owner_full_name')

    class Meta:
        model = models.Course
        exclude = [
            'enrolled',
        ]
        extra_fields = [
            'day_of_the_week',
            'owner_name'
        ]

    def validate(self, data):
        data.setdefault('title', None)
        data.setdefault('description', None)
        data.setdefault('day', None)
        data.setdefault('time_start', None)
        data.setdefault('time_end', None)
        data.setdefault('category', None)
        data.setdefault('owner', None)
        
        if None in data.values():
            raise serializers.ValidationError("Campos faltantes")
        return data