import re

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Blog, Category, Tag, BlogCategory, BlogTags, About
from .pagination import Pagination
from django.core.mail import send_mail


# Create your views here.


def get_home(request):
    blogs = Blog.objects.all().order_by("-update_time")[:4]
    return render(request, "index.html", {"blogs": blogs})


def get_about(request):
    about = About.objects.all().order_by("-update_time")[0]
    return render(request, "about.html", {"about": about})


def get_menu(request):
    category_id = request.GET.get('category', 0)
    tag_id = request.GET.get('tag', 0)
    category_name = ""
    tag_name = ""
    if not category_id == 0:
        bcs = BlogCategory.objects.filter(category_id=category_id)
        blogs = BlogCategory.get_blogs(bcs)
        category_name = Category.objects.get(id=category_id).name
    elif not tag_id == 0:
        bts = BlogTags.objects.filter(tag_id=tag_id)
        blogs = BlogTags.get_blogs(bts)
        tag_name = Tag.objects.get(id=tag_id).name
    else:
        blogs = Blog.objects.all().order_by("-create_time")
    categories = Category.get_categories()
    tags = Tag.get_tags()
    pager = Pagination(request.GET.get('page', '1'), len(blogs), per_num=5, max_show=7)
    return render(request, "menu.html", {"blogs": blogs[pager.start:pager.end], "categories": categories, "tags": tags,
                                         "page_html": pager.page_html, "last_page": pager.page_num,
                                         "category_name": category_name, "tag_name": tag_name})


def get_blog(request):
    blog_id = request.GET.get("blog", 0)
    blog = Blog.objects.get(id=blog_id)
    return render(request, "blog.html", {"blog": blog})


def get_contact(request):
    return render(request, "contact.html")


def contact_me(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    message = request.POST.get("message")
    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(str, email):
        email_subject = "Website Contact Form: " + name
        email_body = "You have received a new message from your website contact form.\n\n" \
                     "Here are the details:\n\nName: {0}\n\nEmail: {1}\n\nPhone: {2}\n\nMessage: \n{3}".format(
            name, email, phone, message)
        send_mail(email_subject, email_body, '2608880870@qq.com',
                  ['1256819071@qq.com'], fail_silently=False)
        return JsonResponse({"msg": "success"})
    else:
        return HttpResponse("500")


def page_not_found(request, exception):
    return render(request, '404.html')
