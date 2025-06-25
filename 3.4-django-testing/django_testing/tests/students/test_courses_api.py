import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker
from rest_framework import status
from students.models import Course, Student
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory(name="Python")
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Python"


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    course_factory(_quantity=5)
    url = "/api/v1/courses/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_filter_course_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = f"/api/v1/courses/?id={courses[0].id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["id"] == courses[0].id


@pytest.mark.django_db
def test_filter_course_by_name(api_client, course_factory):
    course_factory(name="Django")
    course_factory(name="Flask")
    url = "/api/v1/courses/?name=Django"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["name"] == "Django"


@pytest.mark.django_db
def test_create_course(api_client):
    url = "/api/v1/courses/"
    data = {"name": "New Course"}
    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == 1


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name="Old Name")
    url = f"/api/v1/courses/{course.id}/"
    data = {"name": "Updated Name"}
    response = api_client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert Course.objects.get(id=course.id).name == "Updated Name"


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_max_students_per_course(settings, course_factory, student_factory):
    settings.MAX_STUDENTS_PER_COURSE = 2
    course = course_factory()
    students = student_factory(_quantity=3)


    course.students.add(students[0], students[1])


    course.students.add(students[2])
    with pytest.raises(ValidationError):
        course.full_clean()