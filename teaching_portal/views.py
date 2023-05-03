from django.shortcuts import render

def index(request):
    return render(request, 'teaching_portal/tutor.html')


# def dynam(request):
#     return render(request, 'home/home.html')
