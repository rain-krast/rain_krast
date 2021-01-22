from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics
from FinamApp.models import Article
from FinamCollectionService import settings
import pickle

def getCategoriesList():
    return ["Общество", "Политика", "Финансы и рынки", "Экономика"]

def getCategoriesDict():
    return {"Общество":1, "Политика":2, "Финансы и рынки":3, "Экономика":4}

def getTrainingArticles(count): #получение обчающей выборки
    categoriesDict = getCategoriesDict()
    categoriesList = getCategoriesList()
    trainingArticles = {}
    trainingArticles["text"] = []
    trainingArticles["target"] = []
    trainingArticles["names"] = categoriesList
    
    for category in categoriesList:
        articles = list(Article.objects.filter(category=category).order_by("-pk")[:count])
        trainingArticles["text"] = trainingArticles["text"] + list(map(lambda arg: arg.text, articles))
        trainingArticles["target"] = trainingArticles["target"] + list(map(lambda arg: categoriesDict[arg.category], articles))

    return trainingArticles

def getArticlesForTest(count): #получение тестовой выборки
    categoriesDict = getCategoriesDict()
    categoriesList = getCategoriesList()
    articlesForTest = {}
    articlesForTest["text"] = []
    articlesForTest["target"] = []
    articlesForTest["names"] = categoriesList
    
    for category in categoriesList:
        articles = list(Article.objects.filter(category=category).order_by("pk")[:count])
        articlesForTest["text"] = articlesForTest["text"] + list(map(lambda arg: arg.text, articles))
        articlesForTest["target"] = articlesForTest["target"] + list(map(lambda arg: categoriesDict[arg.category], articles))

    return articlesForTest

def getStopWords(): #загрузка стоп слов из файла
    listStopWords = []
    file = open(settings.BASE_DIR + "\\stopWords.txt", "r")

    for line in file:
        listStopWords.append(line.rstrip('\n'))

    return listStopWords

def saveLearnData(objectForS, filename): #сериализация и запись файл
    file = open(settings.BASE_DIR + "\\" + filename, "wb")
    pickle.dump(objectForS, file)
    file.close()

def readLearnData(filename): #десериализация и чтение с файла
    file = open(settings.BASE_DIR + "\\" + filename, "rb")
    result = pickle.load(file)
    file.close()
    return result

def classifierLearn(): #обучение модели классификатора, сохрание оценкт точности в файл, сериализация модели
    fitInformation = {}
    trainingArticles = getTrainingArticles(210)
    testArticles = getArticlesForTest(90)
    classifierObject = Pipeline([
        ('vect', CountVectorizer(stop_words=getStopWords())),
        ('clf', DecisionTreeClassifier())
    ])
    classifierObject.fit(trainingArticles["text"], trainingArticles["target"])
    saveLearnData(classifierObject, "learnedObject.txt")

    predicted = classifierObject.predict(testArticles["text"])

    fileAcc = open(settings.BASE_DIR + "\\AccuracyCl.txt", "wt")
    fileAcc.write(metrics.classification_report(testArticles["target"], predicted, target_names=getCategoriesList()))
    fileAcc.close()

def classifyArticle(text): #классификация текста
    classifierResult = {}
    categoriesList = getCategoriesList()
    classifierObject = readLearnData("learnedObject.txt")
    numberOfCategory = classifierObject.predict([text])[0]
    classifierResult["category"] = categoriesList[numberOfCategory - 1]

    return classifierResult