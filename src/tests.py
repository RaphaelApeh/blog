import random

from django.apps import apps
from django.utils.lorem_ipsum import COMMON_WORDS, words
from django.test import TestCase

if not apps.is_installed("app"):
    raise ImportError("app is not Installed.")

Post = apps.get_model("app", "Post")
Comment = apps.get_model("app", "Comment")


class PostTestCase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(username="test_user", title=words(random.randint(5, 15)), text=" ".join(COMMON_WORDS))

        self.comment = Comment.objects.create(post=self.post, name=words(random.randint(5, 15)), text=" ".join(COMMON_WORDS))

    def test_post_exists(self):
        posts = Post.objects.all()

        self.assertTrue(posts.exists())

    def test_post_comments_relationship(self):
        posts = Post.objects.all()
        post = posts.last()

        self.assertEqual(post.comments.count(), 1)
        self.assertTrue(post.comments.contains(self.comment))