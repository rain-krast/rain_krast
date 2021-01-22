import os
import lxml.etree as ET
from FinamApp.models import Article
from FinamCollectionService import settings

def getArticleInformation(fileName): #парсим xml файл со статьей
    fields = {}
    newTree = ET.parse(fileName)
    fields["source"] = newTree.find(".//source").text
    fields["category"] = list(map(lambda itemObj: itemObj.text, newTree.findall(".//item")))[1]
    fields["title"] = newTree.find(".//title").text
    fields["text"] = newTree.find(".//text").text
    return fields

def xmlFileToSqlite(fields): #сохраняем модель статьи в бд
    articleToSave = Article()
    articleToSave.source = fields["source"]
    articleToSave.category = fields["category"]
    articleToSave.title = fields["title"]
    articleToSave.text = fields["text"]

    articleToSave.save()
            
def writeXmlFilesToSqlite(): #переводим xml файлы в бд, проходясь по заданной папке
    dirName = "articles"
    newsFilesName = os.listdir(settings.BASE_DIR + "\\" + dirName)
    Article.objects.all().delete()

    for fileName in newsFilesName:
        fields = getArticleInformation(settings.BASE_DIR + "\\" + dirName + "\\" + fileName)
        xmlFileToSqlite(fields)
