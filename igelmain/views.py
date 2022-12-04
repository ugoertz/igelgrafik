# -*- coding: utf-8 -*-

import base64
import json
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.base import ContentFile
#from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from django.core.mail import send_mail, send_mass_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from igelmain.models import Kapitel, Aufgabe, Beispiel, Skript, Kategorie


# ---------- Contact -----------------------------------------------------------

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {'size': 40, 'style': 'width:500px;'}))
    email = forms.EmailField(widget = forms.TextInput(attrs = {'size': 40, 'style': 'width:500px;'}))
    betreff = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 40, 'style': 'width:500px;'}))
    nachricht = forms.CharField(widget = forms.Textarea(attrs = {'cols':80, 'rows':13, 'style': 'width:500px;'}))

class ContactFormCC(ContactForm):
    kopie = forms.BooleanField(help_text='Bitte ankreuzen, wenn Du eine Kopie dieser Email erhalten möchtest', required=False)

def contact(request):
    if request.user.is_authenticated:
        CFC = ContactFormCC
    else:
        CFC = ContactForm
    if request.POST:
        form = CFC(request.POST)
        if form.is_valid():
            recipient_list = settings.SEND_MESSAGES_TO

            # evaluate cc_myself
            if request.user.is_authenticated:
                if form.cleaned_data['kopie']:
                    recipient_list.append(form.cleaned_data['email'])

            # send email
            try:
                send_mail('Nachricht von %s: %s' % (form.cleaned_data['name'], form.cleaned_data['betreff']),
                          form.cleaned_data['nachricht'],
                          form.cleaned_data['email'], recipient_list, fail_silently=False)
                messages.success(request, 'Danke für die Nachricht!')
            except:
                messages.error(request, 'Leider ist etwas schiefgegangen. Du kannst auch eine Email schreiben an ug@geometry.de')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Bitte berichtige die Fehler unten.')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name()
            initial['email'] = request.user.email
        form = CFC(initial=initial)
    return render(request, 'contact.html', {'form': form, })


# ----------- AJAX to load/save scripts ---------------------------------------------

@login_required
def ajaxladen(request):
    try:
        skript = request.user.userdata.skript_set.get(key=request.GET['key']).skript
        return HttpResponse(json.dumps({'skript': skript }))
    except:
        return HttpResponse(json.dumps({'skript': ''}))

@login_required
def einreichen(request):
    if not request.POST:
        return HttpResponse()
    try:
        t = request.POST['skript'] + '\n\n-----------------------\n\n'
        t += request.user.username + '\n' + request.user.email
        assert len(t) < 10000
        send_mail('Igelgrafik Gallerie', t, 'ug@geometry.de', ['ug@geometry.de'])
    except:
        return HttpResponse(json.dumps('Fehler'))
    return HttpResponse(json.dumps('Eingereicht - vielen Dank!'))

@login_required
def speichern(request):
    try:
        ud = request.user.userdata
        assert ud.skript_set.count() < 1000
        if 'key' in request.POST:
            try:
                skript = ud.skript_set.get(key=request.POST['key'])
            except:
                skript = Skript(ud=ud, key=request.POST['key'])
            assert request.POST['skript'].strip() != ''
            skript.skript = request.POST['skript']
            skript.save()

            if 'img' in request.POST:
                img_data = request.POST['img'].replace("data:image/png;base64,", "")
                f = ContentFile(base64.b64decode(img_data))
                skript.bild.save('img_' + str(skript.id) + '.png', f)
        elif 'skriptliste' in request.POST:
            for key, skr in json.loads(request.POST['skriptliste']):
                skript = Skript(ud=ud, key=key, skript=skr)
                skript.save()
    except:
        return HttpResponse(json.dumps('Fehler'))
    return HttpResponse(json.dumps('Abgespeichert'))

@login_required
def skriptloeschen(request, id):
    try:
        request.user.userdata.skript_set.get(id=id).delete()
        return HttpResponse(json.dumps('Gelöscht.'))
    except:
        return HttpResponse(json.dumps('Fehler'))



# ----------- View Code -------------------------------------------------------------

def skripte(request):
    if request.user.is_authenticated:
        try:
            ud = request.user.userdata
            skripte = Skript.objects.filter(ud=ud)
            print('Skripte:', len(skripte))
            return render(request, 'skripte.html', { 'skripte': skripte })
        except:
            pass
    return render(request, 'skripte.html', { })


def zeige_lokales_skript(request, key):
    return render(request, 'igel.html', { 'key': key, })

@login_required
def zeige_skript(request, id):
    try:
        skript = request.user.userdata.skript_set.get(id=id)
        return render(request, 'igel.html', { 'key': skript.key, 'skript': skript.skript, })
    except:
        return render(request, 'igel.html')


def zeige_kapitel(request, id):
    kapitel = Kapitel.objects.get(id=int(id))
    return render(request, 'tutorial.html', { 'kapitel': kapitel, 'typ': 'tutorial', })

def igel_kapitel(request, id):
    kapitel = Kapitel.objects.get(id=int(id))
    quelltext = '\n'.join([l for l in kapitel.quelltext.split('\n') if not l.startswith('#')])
    return render(request, 'igel.html', { 'skript': quelltext })

def uebersicht(request):
    kapitelliste = Kapitel.objects.all().order_by('kategorie', 'platz')
    return render(request, 'uebersicht.html', {'kapitelliste': kapitelliste, })


# ------------ Aufgaben ----------------------------------------------------------

def aufgaben(request):
    aufgabenliste = Aufgabe.objects.all().order_by('kategorie', 'platz')
    return render(request, 'aufgaben.html', {'aufgabenliste': aufgabenliste, })

def zeige_aufgabe(request, id):
    aufgabe = Aufgabe.objects.get(id=int(id))
    return render(request, 'aufgabe.html', { 'aufgabe': aufgabe, })

# ------------- Gallerie ----------------------------------------------------------

def gallerie(request):
    beispielliste = Beispiel.objects.all().order_by('-updated')
    return render(request, 'gallerie.html', {'categories': Kategorie.objects.all().order_by('position'), })

def zeige_beispiel(request, id):
    beispiel = Beispiel.objects.get(id=int(id))
    return render(request, 'tutorial.html', { 'kapitel': beispiel, 'typ': 'beispiel', })

def igel_beispiel(request, id):
    beispiel = Beispiel.objects.get(id=int(id))
    quelltext = '\n'.join([l for l in beispiel.quelltext.split('\n') if not l.startswith('# ')])
    return render(request, 'igel.html', { 'skript': quelltext })

