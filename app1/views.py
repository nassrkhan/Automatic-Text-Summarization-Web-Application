from django.shortcuts import render, HttpResponse
# For Flash Messages
from django.contrib import messages

# Create your views here.
def main(request):
    messages.success(request, 'The post has been created successfully.')
    #return HttpResponse("Hello, World!")
    return render(request,'message.html')
