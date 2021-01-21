import os
import lxml.etree as ET
from FinamApp.models import Article
from FinamCollectionService import settings

def getArticleInformation(fileName):
    fields = {}
    newTree = ET.parse(fileName)
    fields["source"] = newTree.find(".//source").text
    fields["category"] = list(map(lambda itemObj: itemObj.text, newTree.findall(".//item")))[1]
    fields["title"] = newTree.find(".//title").text
    fields["text"] = newTree.find(".//text").text
    return fields

def xmlFileToSqlite(fields):
    articleToSave = Article()
    articleToSave.source = fields["source"]
    articleToSave.category = fields["category"]
    articleToSave.title = fields["title"]
    articleToSave.text = fields["text"]

    articleToSave.save()
            
def writeXmlFilesToSqlite():
    dirName = "articles"
    newsFilesName = os.listdir(settings.BASE_DIR + "\\" + dirName)
    Article.objects.all().delete()

    for fileName in newsFilesName:
        fields = getArticleInformation(settings.BASE_DIR + "\\" + dirName + "\\" + fileName)
        xmlFileToSqlite(fields)
