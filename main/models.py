from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


def default_creater():
    return User.objects.first().pk


class Task(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=50, blank=True)
    creator = models.ForeignKey(User, related_name='tasks_created', on_delete=models.SET_DEFAULT, default=default_creater)
    completor = models.ForeignKey(User, null=True, related_name='tasks_completed', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='%d/%m/%Y', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name[:50])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('task_detail', args=[self.slug])

