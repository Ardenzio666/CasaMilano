from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_intro = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    experience_text = models.TextField(blank=True)
    image = models.ImageField(upload_to='menus/')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    layout_reverse = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
    
class MenuCourse(models.Model):
    menu = models.ForeignKey(Menu, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)   # es. "Antipasto"
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.menu.title} - {self.title}"
    

class Dish(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='dishes/')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Piatto"
        verbose_name_plural = "Piatti"

    def __str__(self):
        return self.title