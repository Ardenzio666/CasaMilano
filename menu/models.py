from django.db import models
from django.conf import settings

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
    
    @property
    def approved_comments(self):
        return self.comments.filter(is_approved=True)




class DishComment(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # Per ora può essere NULL perché non hai ancora gli account attivi.
    # In futuro diventerà obbligatorio.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dish_comments",
        null=True,
        blank=True,
    )

    text = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Commento piatto"
        verbose_name_plural = "Commenti piatti"

    def __str__(self):
        author = self.user.username if self.user else "Anonimo"
        return f"Commento di {author} su {self.dish.title}"