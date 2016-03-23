import json

from django.shortcuts import render,get_object_or_404 ,get_list_or_404
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import ListView
from django.utils.safestring import mark_safe
from django.utils.text import unescape_entities
from django.utils.html import strip_tags

from .models import Publisher, Author,Post,Project,API

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

class PublisherList(ListView):
    model = Publisher
    template_name = "practice/publisherlist.html"

class PostView(generic.ListView):
    template_name = 'practice/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'practice/blog_detail.html', {'post': post})

def api_response(request, project_name , api_name):
    project = get_object_or_404(Project, name=project_name)
    api = get_object_or_404(API, project=project , path=api_name)

    if api.content_type == "application/json":
        data = json.dumps(strip_tags(mark_safe(api.response_body)))
        data = json.loads(data)
    data = data.replace("&quot;","\"").replace("&nbsp;","")

    return HttpResponse(data, content_type=api.content_type, status=int(api.res_status))

def api_list(request, project_name):
    project_url = request.build_absolute_uri()
    project = get_object_or_404(Project, name=project_name)
    api = get_list_or_404(API.objects.order_by('path'), project=project)

    return render(request, 'practice/api_list.html', {'api_list': api,'project_name':project_name,'project_url':project_url})
