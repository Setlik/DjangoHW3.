from django.urls import path
from rest_framework.routers import SimpleRouter

from academy.apps import AcademyConfig
from academy.views import (CourseViewSet, LessonCreateAPIView,
                           LessonDestroyAPIView, LessonListAPIView,
                           LessonRetrieveAPIView, LessonUpdateAPIView,
                           PaymentListView, SubscriptionAPIView)

app_name = AcademyConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lessons_delete",
    ),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]

urlpatterns += router.urls
