import re

from django.contrib import admin
from .models import Blog, Category, BlogCategory, BlogTags, Tag, Image, About

# admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(BlogCategory)
admin.site.register(Tag)
admin.site.register(BlogTags)
admin.site.register(About)


class TagInline(admin.StackedInline):
    model = BlogTags
    extra = 3


class CategoryInline(admin.StackedInline):
    model = BlogCategory
    extra = 1
    max_num = 1


class ImageInline(admin.StackedInline):
    model = Image


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Blog info', {'fields': ['title', 'summary', 'is_secret', 'content']}),
        ('Date info', {'fields': ['create_time', 'update_time']}),
    ]
    inlines = [TagInline, CategoryInline, ImageInline]

    def save_model(self, request, obj, form, change):
        id = Blog.objects.all().order_by('-id')[0].id + 1
        content = obj.content
        content = "".join(content.split("\n"))
        code_language = ""
        if content[0] == '[':
            temp_list = content.split(']', 1)
            code_language = temp_list[0][1:]
            content = temp_list[1]
        style = re.findall("<head>.*?</head>", content)
        header = re.findall("<header>.*?</header>", content)
        for i in style:
            content = content.replace(i, "")
        for i in header:
            content = content.replace(i, "")
        images = re.findall("<img.*?/>", content)
        for image in images:
            src = image.split("src=\"")[1].split("\"")[0]
            filename = "".join(src.split("/")[-1].split("\'")[0].split("%20"))
            content = content.replace(src, "/media/" + str(id) + "/" + filename)
        content = content.replace("<code>", "<code class='language-"+ code_language +"'>")
        content = content.replace("class=\"code\"", "")
        obj.content = content
        super(BlogAdmin, self).save_model(request, obj, form, change)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Image)