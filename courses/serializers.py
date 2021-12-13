from rest_framework import serializers
from . import models

class CourseSerializer(serializers.ModelSerializer):
    day_of_the_week = serializers.CharField(read_only=True,
                                            source='get_day_of_the_week')
    owner_name = serializers.CharField(read_only=True,
                                        source='get_owner_full_name')

    class Meta:
        model = models.Course
        fields = [
            'id',
            'title',
            'description',
            'day_of_the_week',
            'time_start',
            'time_end',
            'owner',
            'owner_name'
        ]

    def get_day_of_the_week(self):
        return self.Meta.model.get_day_of_the_week()

    def get_owner_full_name(self):
        return self.Meta.model.get_owner_full_name()
