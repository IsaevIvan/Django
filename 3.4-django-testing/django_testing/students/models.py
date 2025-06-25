from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )

    def clean(self):
        if self.students.count() > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError("Слишком много студентов на курсе!")