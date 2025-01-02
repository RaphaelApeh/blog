from django.db import models
from django.http import HttpRequest
from django.utils.crypto import get_random_string
from django.utils.text import slugify, Truncator
from django.template.response import TemplateResponse

from nanodjango import Django

from decouple import config

SECRET_KEY = config("DJANGO_SECRET_KEY", default="")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)


app = Django()
    
# models.py

class CATEGORIES_CHOICES(models.TextChoices):
    SPORT = "sport", "Sport"
    ENTERTAINMENT = "entertainment", "Entertainment"
    TECHNOLOGY = "technology", "Technology"
    FASHION = "fashion", "Fashion"


@app.admin
class Post(models.Model):
    username = models.CharField(max_length=20, db_index=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    category = models.CharField(max_length=15, choices=CATEGORIES_CHOICES.choices, default=CATEGORIES_CHOICES.SPORT)
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def comments(self):
        return self.comment_set.all()
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            title = Truncator(self.title).chars(15).replace('.',"")
            self.slug = slugify(title)
        super().save(*args, **kwargs)
            

@app.admin
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# views.py

@app.route('/')
def home_page_view(request: HttpRequest):
    if request.method == 'POST':
        return f"{get_random_string(10)}"
    return TemplateResponse(request, 'blog/base.html')



if __name__ == '__main__':
    app.run()