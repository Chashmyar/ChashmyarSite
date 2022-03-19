from django.shortcuts import render
import accounts.views
from blog.models import Post

is_logged_in = False


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'is_logged_in': is_logged_in
    }
    return render(request, 'pages/index.html', context)


def about_us(request):
    return render(request, 'pages/about-us.html', {'is_logged_in': is_logged_in})


def contact(request):
    return render(request, 'pages/contact.html', {'is_logged_in': is_logged_in})
