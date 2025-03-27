from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from academy.models import Course, Lesson, Subscription
from academy.validators import validate_youtube_url
from users.models import Payment


class LessonSerializer(ModelSerializer):
    video_link = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class CourseDetailSerializer(ModelSerializer):
    count_course_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_course_lessons(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("course_name", "description", "count_course_lessons", "lessons")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
