import os
import uuid
import re

from django.db import models
from datetime import datetime

namespace = uuid.NAMESPACE_URL
name = 'image'


def get_path(instance, filename):
    filename = filename.split("\\")[-1]
    filename = "".join(filename.split())
    # ext = filename.split('.').pop()
    # filename = '{0}.{1}'.format(uuid.uuid3(namespace, name), ext)
    return os.path.join(str(instance.blog_id) + '/', filename)


# Create your models here.

class Blog(models.Model):
    id = models.AutoField
    title = models.CharField(default="", max_length=50, verbose_name="文章标题")
    content = models.TextField(default="", verbose_name="文章内容")
    is_secret = models.IntegerField(default=0, verbose_name="是否开放")
    summary = models.CharField(max_length=200, default="", verbose_name="摘要")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    def __str__(self):
        return self.title

    def get_tags(self):
        bts = BlogTags.objects.filter(blog_id=self.id)
        tags = []
        for bt in bts:
            tags.append(bt.tag)
        return tags


class Category(models.Model):
    id = models.AutoField
    name = models.CharField(default="", max_length=50, verbose_name="类别名称")

    def __str__(self):
        return self.name

    def count(self):
        return BlogCategory.objects.filter(category_id=self.id).count()

    @staticmethod
    def get_categories():
        categories = list(Category.objects.all())
        for category in categories:
            if category.count() == 0:
                categories.remove(category)
        return categories


class Tag(models.Model):
    id = models.AutoField
    name = models.CharField(default="", max_length=20, verbose_name="标签名称")

    def __str__(self):
        return self.name

    def count(self):
        return BlogTags.objects.filter(tag_id=self.id).count()

    @staticmethod
    def get_tags():
        tags = list(Tag.objects.all())
        for tag in tags:
            if tag.count() == 0:
                tags.remove(tag)
        return tags


class Image(models.Model):
    id = models.AutoField
    img = models.ImageField(upload_to=get_path)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="博客")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        content = self.blog.content
        filename = self.img.url.split("/")[-1]
        file = filename.rsplit("_", 1)[0]
        images = re.findall("<img.*?/>", content)
        for image in images:
            src = image.split("src=\"")[1].split("\"")[0]
            filename = "".join(src.split("/")[-1].split("\'")[0].split())
            if filename.rsplit("_", 1)[0] == file:
                content = content.replace(src, "/media/" + self.img.url)
        super(Image, self).save()


class BlogCategory(models.Model):
    id = models.AutoField
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="博客")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="类别")

    @staticmethod
    def get_blogs(bcs):
        id_list = []
        for bc in bcs:
            id_list.append(bc.blog_id)
        blogs = Blog.objects.filter(id__in=id_list).order_by("-create_time")
        return blogs


class BlogTags(models.Model):
    id = models.AutoField
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="博客")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签")

    @staticmethod
    def get_blogs(bts):
        id_list = []
        for bt in bts:
            id_list.append(bt.blog_id)
        blogs = Blog.objects.filter(id__in=id_list).order_by("-create_time")
        return blogs


class About(models.Model):
    id = models.AutoField
    content = models.TextField(default="", verbose_name="关于内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")
