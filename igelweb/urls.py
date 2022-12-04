from django.urls import include, re_path
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from igelmain.views import (
    igel_kapitel, aufgaben, zeige_aufgabe, gallerie, zeige_beispiel,
    igel_beispiel, uebersicht, zeige_kapitel, skripte, zeige_skript, ajaxladen,
    skriptloeschen, speichern, einreichen, zeige_lokales_skript, contact,
)

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


urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^igel/$', IgelView.as_view(), name='igel'),
    # url(r'^canvas/$',CanvasView.as_view(), name='canvas'),
    re_path(r'^igel/tutorial/(?P<id>\d+)/$', igel_kapitel, name='igel'),
    re_path(r'^aufgaben/$', aufgaben, ),
    re_path(r'^aufgabe/(?P<id>\d+)/$', zeige_aufgabe, ),
    re_path(r'^gallerie/$', gallerie, ),
    re_path(r'^beispiel/(?P<id>\d+)/$', zeige_beispiel, ),
    re_path(r'^igel/beispiel/(?P<id>\d+)/$', igel_beispiel, name='igel'),
    re_path(r'^tutorial/$', uebersicht, ),
    re_path(r'^tutorial/(?P<id>\d+)/$', zeige_kapitel, ),
    re_path(r'^skripte/$', skripte),
    re_path(r'^skripte/laden/(?P<id>\d+)/$', zeige_skript),
    re_path(r'^skripte/ajaxladen/$', ajaxladen),
    re_path(r'^skripte/loeschen/(?P<id>\d+)/$', skriptloeschen),
    re_path(r'^skripte/speichern/$', speichern),
    re_path(r'^skripte/einreichen/$', einreichen),
    re_path(r'^skripte/lokal/(?P<key>\w+)/$', zeige_lokales_skript),
    re_path(r'^kontakt/$', contact, name='contact'),
    url(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('registration.backends.default.urls')),
    re_path(r'^robots\.txt$', robottxt.as_view()),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

