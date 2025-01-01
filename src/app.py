import pathlib

from django.db import models
from django.template.response import TemplateResponse

from nanodjango import Django

from decouple import config

SECRET_KEY = config("DJANGO_SECRET_KEY", default="")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

app = Django()


@app.admin
class Post(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@app.admin
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



@app.route('/')
def home_page_view(request):
    return TemplateResponse(request, 'blog/base.html')


if __name__ == '__main__':
    app.run()