from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_name = models.CharField(max_length=255)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to="images/")
    recipe_view_count = models.IntegerField(default=0)

class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department

    class Meta:
        ordering = ['department']

class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")

    def __str__(self):
        return self.subject_name

    def get_absolute_url(self):
        return reverse("subject_detail", kwargs={"pk": self.pk})

class Student(models.Model):
    department = models.ForeignKey(Department, related_name="students", on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentID, related_name="student", on_delete=models.SET_NULL, null=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()

    def __str__(self) -> str:
        return self.student_name

    class Meta:
        ordering = ['student_name']
        verbose_name = "student"

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, related_name="studentmarks", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.student.student_name} {self.subject.subject_name}'

    class Meta:
        unique_together = ['student', 'subject']
