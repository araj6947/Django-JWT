from .models import Course
from rest_framework import serializers
'''
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['course']
'''
class CourseSerializer(serializers.ModelSerializer):
   # lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor']