""" from .models import Post, CV
from django.http import HttpResponse

class Post_Mixins(object):
    def get_post_by_id(self, request, id):
        try:
            return Post.objects.get(id = id)
        except:
            return HttpResponse("Not Found")

class CV_Mixins(object):
    def get_post_by_id(self, request, id):
        try:
            return CV.objects.get(id = id)
        except:
            return HttpResponse("Not Found")

 """