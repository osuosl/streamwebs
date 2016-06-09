from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
#    return HttpResponse("Hey, you've reached the index.")
    return render_to_string('streamwebs/index.html')
