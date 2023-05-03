from django.shortcuts import render

def index(request):
    return render(request, 'learning/index.html')
    # learning/ depicts the folder named learning 
    # which will contain the templates for that specific app

