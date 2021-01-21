from FinamApp.models import Article

def getPageLimit():
    return 50

def getPageBorders(page, pageLimit, querySet):
    lenQuerySet = len(querySet)
    startElement = pageLimit * (page - 1)
    endElement = (pageLimit * page)
    if (startElement < lenQuerySet):
        if (endElement > lenQuerySet):
             endElement = lenQuerySet
    else:
        return False
    return querySet[startElement:endElement]

def articlesGet(page):
    pageLimit = getPageLimit()
    getResult = {}
    getResult["articles"] = []

    querySetObject = Article.objects.all().order_by("-pk")

    getResult["len"] = len(querySetObject)
    getResult["pageLimit"] = pageLimit

    if page is not None:
        querySetObject = getPageBorders(page, pageLimit, querySetObject)
        if querySetObject is False:
            return False

    for article in querySetObject:
        articleInformation = {}
        articleInformation["id"] = article.pk
        articleInformation["title"] = article.title
        articleInformation["category"] = article.category
        getResult["articles"].append(articleInformation)

    return getResult

def articlesFilterByCategory(category, page):
    pageLimit = getPageLimit()
    filterResult = {}
    filterResult["articles"] = []

    querySetObject = Article.objects.filter(category=category).order_by("-pk")

    filterResult["len"] = len(querySetObject)
    filterResult["pageLimit"] = pageLimit

    if page is not None:
        querySetObject = getPageBorders(page, pageLimit, querySetObject)
        if querySetObject is False:
            return False

    for article in querySetObject:
        articleInformation = {}
        articleInformation["id"] = article.pk
        articleInformation["title"] = article.title
        articleInformation["category"] = article.category
        filterResult["articles"].append(articleInformation)

    return filterResult

def articleDelete(id):
    queryForDelete = Article.objects.filter(pk=id)
    if queryForDelete.exists():
        queryForDelete.delete()
        return True
    else:
        return False

def articleGet(id):
    queryForGet = Article.objects.filter(pk=id)
    if queryForGet.exists():
        articleFullInformation = {}
        articleFullInformation["source"] = queryForGet[0].source
        articleFullInformation["title"] = queryForGet[0].title
        articleFullInformation["category"] = queryForGet[0].category
        articleFullInformation["text"] = queryForGet[0].text
        return articleFullInformation
    else:
        return False

def articleAdd(source, title, category, text):
    articleForAdd = Article()
    articleForAdd.source = source
    articleForAdd.title = title
    articleForAdd.category = category
    articleForAdd.text = text

    articleForAdd.save()