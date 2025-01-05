from __future__ import annotations

import json
import datetime
from typing import Literal, List

from django.db import models
from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.conf.urls.static import static
from django.utils.text import slugify, Truncator
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from nanodjango import Django
from nanodjango.urls import urlpatterns

from decouple import config

SECRET_KEY = config("DJANGO_SECRET_KEY", default="")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)


app = Django(EXTRA_APPS=['django.contrib.humanize'])

if DEBUG:
    urlpatterns += static(app.settings.MEDIA_URL, document_root=app.settings.MEDIA_ROOT)

# models.py

class CATEGORIES_CHOICES(models.TextChoices):
    SPORTS = "sports", "Sports"
    ENTERTAINMENT = "entertainment", "Entertainment"
    TECHNOLOGY = "technology", "Technology"
    FASHION = "fashion", "Fashion"


@app.admin
class Post(models.Model):
    username = models.CharField(max_length=20, db_index=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    category = models.CharField(max_length=15, choices=CATEGORIES_CHOICES.choices, default=CATEGORIES_CHOICES.SPORTS)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_posts', default="default.jpg")
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

    def get_absolute_url(self):
        return reverse("detail-page", kwargs={'slug': self.slug})
            

@app.admin
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# api.py

class PostSchema(app.ninja.ModelSchema):

    class Meta:
        model = Post
        fields = ['username', 'title', 'text', 'image']


@app.api.get('/posts', response=List[PostSchema])
def posts_api_view(request: HttpRequest):
    return Post.objects.all()

@app.api.post('/create')
def posts_create_view(request: HttpRequest, payload: PostSchema):
    value = json.loads(request.body)
    if Post.objects.filter(**payload.dict()).exists():
        return {'Error': "Post already exists"}
    obj = Post.objects.create(**payload.dict())
    return {'title': obj.title, "username": obj.username, "slug":obj.slug, "text": obj.text}
    

# views.py

@app.route('/', name="home-page")
def home_page_view(request: HttpRequest):
    qs = Post.objects.all().order_by('-timestamp')
    current_year = datetime.datetime.now().year
    pagination = Paginator(qs, 5)
    page = request.GET.get("page", 1)
    newqs = pagination.get_page(page)
    if request.method == 'POST':
        return f"{get_random_string(10)}"
    context = {
        "qs":newqs,
        'year':current_year
    }
    return TemplateResponse(request, 'blog/base.html', context)


@app.route('/posts/<slug:slug>/', name="detail-page")
def detail_page_view(request: HttpRequest, slug: str):
    
    obj = get_object_or_404(Post, slug__iexact=slug)
    categories = CATEGORIES_CHOICES.choices
    context = {
        'object': obj,
        'categories':[x[1] for x in categories] # example: ["sports", ...]
    }
    return TemplateResponse(request, "blog/detail.html", context)



@app.route("/create/", name="post-create")
def create_post_view(request: HttpRequest):
    if request.method == "POST":
        print(request.body)
    return TemplateResponse(request, "blog/create.html")



if __name__ == '__main__':
    app.run()