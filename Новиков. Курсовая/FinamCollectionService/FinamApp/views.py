from django.shortcuts import render
from django.http import HttpResponse

def classifier(request):
    if request.method == "GET":
        return render(request, "FinamApp/index.html")
    else:
        return HttpResponse("method not supported", status=405)

def showCollection(request):
    if request.method == "GET":
        return render(request, "FinamApp/workWithCollection.html")
    else:
        return HttpResponse("method not supported", status=405)

def addArticle(request):
    if request.method == "GET":
        return render(request, "FinamApp/addArticle.html")
    else:
        return HttpResponse("method not supported", status=405)

def showArticle(request):
    if request.method == "GET":
        return render(request, "FinamApp/article.html")
    else:
        return HttpResponse("method not supported", status=405)

def throw404(request):
    return HttpResponse("page not found", status=404)