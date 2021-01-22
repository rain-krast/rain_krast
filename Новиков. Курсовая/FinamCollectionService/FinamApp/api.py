from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json
from FinamApp import xmlToSqlite
from FinamApp import workWithArticles
from FinamApp import core

@csrf_exempt
def loadXml(request): #точка входа для загрузки в бд xml файлов
    if request.method == "POST":
        xmlToSqlite.writeXmlFilesToSqlite()
        return HttpResponse("xml loaded to sqlite")
    else:
        return HttpResponse("method not supported", status=405)

@csrf_exempt
def getPageArticles(request): #точка входа для вывода определенной страницы превью новостей
    if request.method == "POST":
        if request.content_type != "application/json":
            return HttpResponse("unsupported content type", status=415)
        try:
            pageNumbInJson = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("bad request", status=400)

        if pageNumbInJson:
            reqParams = ["page"]
            if list(pageNumbInJson.keys()) != reqParams:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if pageNumbInJson["page"] is not None:
            if isinstance(pageNumbInJson["page"], int):
                if pageNumbInJson["page"] < 1:
                    return HttpResponse("bad request", status=400)
            else:
                return HttpResponse("bad request", status=400)

        ArticlesInformation = workWithArticles.articlesGet(pageNumbInJson["page"])

        if ArticlesInformation:
            for articleInf in ArticlesInformation["articles"]:
                articleInf["title"] = escape(articleInf["title"])
            return HttpResponse(json.dumps(ArticlesInformation), content_type="application/json")
        else:
            return HttpResponse("page not found", status=404)
    else:
        return HttpResponse("method not supported", status=405)

@csrf_exempt
def articlesPageFilterByCategory(request): #точка входа для вывода определенной страницы превью отфильтрованных новостей
    if request.method == "POST":
        if request.content_type != "application/json":
            return HttpResponse("unsupported content type", status=415)
        try:
            paramsInJson = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("bad request", status=400)

        if paramsInJson:
            reqParams = ["category","page"]
            if list(paramsInJson.keys()) != reqParams:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if isinstance(paramsInJson["category"], str):
            reqCategories = ["Общество", "Политика", "Финансы и рынки", "Экономика"]
            if not (paramsInJson["category"] in reqCategories):
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if paramsInJson["page"] is not None:
            if isinstance(paramsInJson["page"], int):
                if paramsInJson["page"] < 1:
                    return HttpResponse("bad request", status=400)
            else:
                return HttpResponse("bad request", status=400)

        ArticlesInformation = workWithArticles.articlesFilterByCategory(paramsInJson["category"], paramsInJson["page"])

        if ArticlesInformation:
            for articleInf in ArticlesInformation["articles"]:
                articleInf["title"] = escape(articleInf["title"])
            return HttpResponse(json.dumps(ArticlesInformation), content_type="application/json")
        else:
            return HttpResponse("page not found", status=404)
    else:
        return HttpResponse("method not supported", status=405)

@csrf_exempt
def deleteOrGetArticle(request, id): #точка входа для удаления или получения информации определенной статьи
    if request.method == "DELETE":
        deleteResult = workWithArticles.articleDelete(id)
        if deleteResult:
            return HttpResponse("delete success")
        else:
            return HttpResponse("bad request", status=400)

    if request.method == "GET":
        getResult = workWithArticles.articleGet(id)
        if getResult:
            getResult["source"] = escape(getResult["source"])
            getResult["title"] = escape(getResult["title"])
            getResult["text"] = escape(getResult["text"].strip())
            return HttpResponse(json.dumps(getResult), content_type="application/json")
        else:
            return HttpResponse("page not found", status=404)

    if request.method != "DELETE" and request.method != "GET":
        return HttpResponse("method not supported", status=405)

@csrf_exempt
def addArticle(request): #точка входа для добавления статьи в коллекцию
    if request.method == "POST":
        if request.content_type != "application/json":
            return HttpResponse("unsupported content type", status=415);
        try:
            paramsInJson = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("bad request", status=400)

        if paramsInJson:
            reqParams = ["source", "title", "category", "text"]
            if list(paramsInJson.keys()) != reqParams:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if isinstance(paramsInJson["source"], str):
            if paramsInJson["source"].strip():
                if len(paramsInJson["source"]) < 350:
                    validatorObj = URLValidator()
                    try:
                        validatorObj(paramsInJson["source"])
                    except ValidationError:
                        return HttpResponse("bad request", status=400)
                else:
                    return HttpResponse("bad request", status=400)
            else:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if isinstance(paramsInJson["title"], str):
            if paramsInJson["title"].strip():
                if len(paramsInJson["title"]) > 300:
                    return HttpResponse("bad request", status=400)
            else:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if isinstance(paramsInJson["category"], str):
            reqCategories = ["Общество", "Политика", "Финансы и рынки", "Экономика"]
            if not (paramsInJson["category"] in reqCategories):
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if isinstance(paramsInJson["text"], str):
            if paramsInJson["text"].strip():
                if len(paramsInJson["text"]) > 15000:
                    return HttpResponse("bad request", status=400)
            else:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        workWithArticles.articleAdd(paramsInJson["source"], paramsInJson["title"], paramsInJson["category"], paramsInJson["text"])
        return HttpResponse("add success")
    else:
        return HttpResponse("method not supported", status=405)

@csrf_exempt
def classifierModelLearn(request): #точка входа для переобучения модели
    if request.method == "POST":
        core.classifierLearn()
        return HttpResponse("learning model success")
    else:
        return HttpResponse("method not supported", status=405)

@csrf_exempt
def classifyArticle(request): #точка входа для классификации текста
    if request.method == "POST":
        if request.content_type != "application/json":
            return HttpResponse("bad request", status=400)

        try:
            paramsInJson = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("bad request", status=400)

        if paramsInJson:
            reqParams = ["text"]
            if list(paramsInJson.keys()) != reqParams:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        if isinstance(paramsInJson["text"], str):
            if paramsInJson["text"].strip():
                if len(paramsInJson["text"]) > 15000:
                    return HttpResponse("bad request", status=400)
            else:
                return HttpResponse("bad request", status=400)
        else:
            return HttpResponse("bad request", status=400)

        classifyResult = core.classifyArticle(paramsInJson["text"])
        return HttpResponse(json.dumps(classifyResult), content_type="application/json")

    else:
        return HttpResponse("method not supported", status=405)