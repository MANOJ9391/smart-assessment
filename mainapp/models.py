from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Chapter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    question_text = models.TextField()

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct_option = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text


class Resource(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.URLField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.png')

    # NEW FIELDS
    full_name = models.CharField(max_length=100, blank=True)
    student_class = models.CharField(max_length=50, blank=True)
    college = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(
    upload_to='profile_pics/',
    default='default.png',   # 👈 important
    blank=True
)

    def __str__(self):
        return self.user.username




class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    
    chapter_stats = models.JSONField(null=True, blank=True)
    recommendations = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)