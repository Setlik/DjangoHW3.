from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from academy.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="krolikset@gmail.com")
        self.course = Course.objects.create(course_name="Программист", owner=self.user)
        self.lesson = Lesson.objects.create(
            lesson_name="Python", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrive(self):
        url = reverse("academy:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("course_name"), self.course.course_name)

    def test_subscribe_to_course(self):
        url = reverse("academy:subscription")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("academy:subscription")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="test@gmail.com", password="password"
        )
        self.course = Course.objects.create(course_name="Программист", owner=self.user)
        self.lesson = Lesson.objects.create(
            lesson_name="Python",
            course=self.course,
            owner=self.user,
            video_link="http://youtube.com/java_video",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("academy:lessons_create")
        data = {
            "lesson_name": "Java",
            "course": self.course.id,
            "video_link": "http://youtube.com/java_video",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_read_lesson(self):
        url = reverse("academy:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertTrue(any(lesson["lesson_name"] == "Python" for lesson in results))

    def test_update_lesson(self):
        url = reverse("academy:lessons_update", args=(self.lesson.pk,))
        data = {
            "lesson_name": "Python Advanced",
            "course": self.course.id,
            "video_link": "http://youtube.com/java_video1",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.lesson_name, "Python Advanced")

    def test_delete_lesson(self):
        url = reverse("academy:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    # def test_permission_denied_on_create_lesson(self):
    #     self.client.logout()
    #     url = reverse("academy:lessons_create")
    #     data = {
    #         'lesson_name': 'Unauthorized Lesson',
    #         'course': self.course.id,
    #         'video_link': 'http://example.com/unauthorized_video',
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_denied_on_update_lesson(self):
        another_user = User.objects.create_user(
            username="user1", email="anotheruser@gmail.com", password="password"
        )
        self.client.force_authenticate(user=another_user)
        url = reverse("academy:lessons_update", args=(self.lesson.pk,))
        data = {"lesson_name": "Unauthorized Update"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
