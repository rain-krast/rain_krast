from django.conf.urls import include, url
from django.views.static import serve
from FinamCollectionService import settings
from FinamApp import api
from FinamApp import views

urlpatterns = [
    url(r'^$', views.classifier),
    url(r'^articles-collection$', views.showCollection),
    url(r'^add-article$', views.addArticle),
    url(r'^articles/[0-9]+$', views.showArticle),
    url(r'^api/load-xml$', api.loadXml),
    url(r'^api/articles$', api.addArticle),
    url(r'^api/articles/all$', api.getPageArticles),
    url(r'^api/articles/filter-by-category$', api.articlesPageFilterByCategory),
    url(r'^api/articles/(?P<id>[0-9]+)$', api.deleteOrGetArticle),
    url(r'^api/classify$', api.classifyArticle),
    url(r'^api/model-learn$', api.classifierModelLearn),
	url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
]

handler404 = views.throw404
