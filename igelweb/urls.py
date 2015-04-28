from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

class HomeView(TemplateView):
    template_name = "home.html"

class CanvasView(TemplateView):
    template_name = "canvas.html"

class IgelView(TemplateView):
    template_name = "igel.html"

class robottxt(TemplateView):
    template_name = "robots.txt"
    mimetype = "text/plain"


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^igel/$', IgelView.as_view(), name='igel'),
    # url(r'^canvas/$',CanvasView.as_view(), name='canvas'),
    url(r'^igel/tutorial/(?P<id>\d+)/$', 'igelmain.views.igel_kapitel', name='igel'),
    url(r'^aufgaben/$', 'igelmain.views.aufgaben', ),
    url(r'^aufgabe/(?P<id>\d+)/$', 'igelmain.views.zeige_aufgabe', ),
    url(r'^gallerie/$', 'igelmain.views.gallerie', ),
    url(r'^beispiel/(?P<id>\d+)/$', 'igelmain.views.zeige_beispiel', ),
    url(r'^igel/beispiel/(?P<id>\d+)/$', 'igelmain.views.igel_beispiel', name='igel'),
    url(r'^tutorial/$', 'igelmain.views.uebersicht', ),
    url(r'^tutorial/(?P<id>\d+)/$', 'igelmain.views.zeige_kapitel', ),
    url(r'^skripte/$', 'igelmain.views.skripte'),
    url(r'^skripte/laden/(?P<id>\d+)/$', 'igelmain.views.zeige_skript'),
    url(r'^skripte/ajaxladen/$', 'igelmain.views.ajaxladen'),
    url(r'^skripte/loeschen/(?P<id>\d+)/$', 'igelmain.views.skriptloeschen'),
    url(r'^skripte/speichern/$', 'igelmain.views.speichern'),
    url(r'^skripte/einreichen/$', 'igelmain.views.einreichen'),
    url(r'^skripte/lokal/(?P<key>\w+)/$', 'igelmain.views.zeige_lokales_skript'),
    url(r'^kontakt/$', 'igelmain.views.contact', name='contact'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^robots\.txt$', robottxt.as_view()),
)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

