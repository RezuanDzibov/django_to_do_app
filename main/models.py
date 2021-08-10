from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Task(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=50, blank=True)
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

    def save(self):
        self.slug = slugify(self.name[:50])
        super().save()

    def get_absolute_url(self):
        return reverse('task_detail', args=[self.slug])