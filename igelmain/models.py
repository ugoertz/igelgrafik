# -*- coding: utf-8 -*-

import os
import os.path
import tempfile
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from registration.signals import user_activated
from imagekit.models import ImageSpecField
from imagekit.processors import Resize
from PIL import Image


class Kategorie(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=20, unique=True)
    intro = models.TextField(blank=True)
    details = models.TextField(blank=True)
    position = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class WhiteBackground(object):

    def process(self, image):
        bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
        bg.paste(image, (0,0), )
        return bg


class Kapitel(models.Model):
    '''Ein Kapitel des "Tutorials".'''

    KATEGORIE_CHOICES = [('0', 'Einstieg'),
                         ('1', 'Schleifen'),
                         ('2', 'Funktionen'),
                         ('3', 'Bedingungen'),
                         ('4', 'Für Fortgeschrittene'),
                        ]

    titel = models.CharField(max_length=50)
    zusammenfassung = models.TextField(max_length=500)
    kategorie = models.CharField(choices=KATEGORIE_CHOICES, max_length=2)
    platz = models.FloatField()
    quelltext = models.TextField(max_length=50000)
    doccoHTML = models.TextField(max_length=100000)
    bild = models.ImageField(upload_to='tutorial')
    docbild = ImageSpecField([WhiteBackground(), Resize(400, 400), ], source='bild', format='JPEG', )
    thumbnail = ImageSpecField([WhiteBackground(), Resize(80, 80), ], source='bild', format='JPEG', )

    def __unicode__(self):
        return u'%s (%s/%d)' % (self.titel, self.kategorie, self.platz)

    def save(self, *args, **kwargs):

        # fill doccoHTML
        sourcefile = tempfile.NamedTemporaryFile(delete=False, dir=settings.TMP_PATH, suffix='.coffee')
        sourcefile.write('# ' + self.titel.encode('utf8') + '\n')
        sourcefile.write('# ' + '-' * len(self.titel.encode('utf8')) + '\n# \n')
        sourcefile.write(self.quelltext.encode('utf8'))
        sourcefile.close()

        path = tempfile.mkdtemp(dir=settings.TMP_PATH)
        os.system('docco -t %s/template.jst -o %s %s' % (settings.DOCCO_TEMPLATE_PATH, path, sourcefile.name))

        with open(os.path.join(path, os.path.basename(sourcefile.name)[:-7] + '.html')) as resultfile:
            self.doccoHTML = resultfile.read().decode('utf8')

        super(Kapitel, self).save(*args, **kwargs)


class Beispiel(models.Model):
    '''Ein Beispiel in der Gallerie'''

    titel = models.CharField(max_length=50)
    autor = models.CharField(max_length=200)
    quelltext = models.TextField(max_length=50000)
    doccoHTML = models.TextField(max_length=100000)
    bild = models.ImageField(upload_to='tutorial')
    docbild = ImageSpecField([WhiteBackground(), Resize(400, 400), ], source='bild', format='JPEG', )
    thumbnail = ImageSpecField([WhiteBackground(), Resize(200, 200), ], source='bild', format='JPEG', )
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Kategorie, null=True, blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.titel, unicode(self.updated))

    def save(self, *args, **kwargs):

        # fill doccoHTML
        sourcefile = tempfile.NamedTemporaryFile(delete=False, dir=settings.TMP_PATH, suffix='.coffee')
        sourcefile.write('# ' + self.titel.encode('utf8') + '\n')
        sourcefile.write('# ' + '-' * len(self.titel.encode('utf8')) + '\n#\n#\n')
        if self.quelltext.startswith('#'):
            sourcefile.write('# <div style="margin-top:400px;"></div>\n\n')
        else:
            sourcefile.write('# <div style="margin-top:400px;"></div>\n\n# .\n')
        sourcefile.write(self.quelltext.encode('utf8'))
        sourcefile.close()

        path = tempfile.mkdtemp(dir=settings.TMP_PATH)
        os.system('docco -t %s/template.jst -o %s %s' % (settings.DOCCO_TEMPLATE_PATH, path, sourcefile.name))

        with open(os.path.join(path, os.path.basename(sourcefile.name)[:-7] + '.html')) as resultfile:
            self.doccoHTML = resultfile.read().decode('utf8')

        super(Beispiel, self).save(*args, **kwargs)


class Aufgabe(models.Model):
    '''Eine Aufgabe in der Aufgabensammlung'''

    KATEGORIE_CHOICES = [('0', 'Einstieg'),
                         ('1', 'Schleifen'),
                         ('2', 'Funktionen'),
                         ('3', 'Bedingungen'),
                         ('4', 'Für Fortgeschrittene'),
                        ]

    titel = models.CharField(max_length=50)
    zusammenfassung = models.TextField(max_length=500)
    kategorie = models.CharField(choices=KATEGORIE_CHOICES, max_length=2)
    platz = models.FloatField()
    quelltext = models.TextField(max_length=50000)
    doccoHTML = models.TextField(max_length=100000)
    bild = models.ImageField(upload_to='tutorial')
    docbild = ImageSpecField([WhiteBackground(), Resize(400, 400), ], source='bild', format='JPEG', )
    thumbnail = ImageSpecField([WhiteBackground(), Resize(200, 200), ], source='bild', format='JPEG', )

    def __unicode__(self):
        return u'%s (%s/%d)' % (self.titel, self.kategorie, self.platz)

    def save(self, *args, **kwargs):

        # fill doccoHTML
        sourcefile = tempfile.NamedTemporaryFile(delete=False, dir=settings.TMP_PATH, suffix='.coffee')
        sourcefile.write('# ' + self.titel.encode('utf8') + '\n')
        sourcefile.write('# ' + '-' * len(self.titel.encode('utf8')) + '\n# \n')
        sourcefile.write(self.quelltext.encode('utf8'))
        sourcefile.close()

        path = tempfile.mkdtemp(dir=settings.TMP_PATH)
        os.system('docco -t %s/template.jst -o %s %s' % (settings.DOCCO_TEMPLATE_PATH, path, sourcefile.name))

        with open(os.path.join(path, os.path.basename(sourcefile.name)[:-7] + '.html')) as resultfile:
            self.doccoHTML = resultfile.read().decode('utf8')

        super(Aufgabe, self).save(*args, **kwargs)



class Userdata(models.Model):
    user = models.OneToOneField(User)


class Skript(models.Model):
    key = models.CharField(max_length=20)
    skript = models.TextField(max_length=2000)
    ud = models.ForeignKey(Userdata)
    bild = models.ImageField(upload_to='userskripte', null=True)
    thumbnail = ImageSpecField([WhiteBackground(), Resize(150, 150), ], source='bild', format='png', )

    def __unicode__(self):
        return '%s: %s (%d)' % (self.ud.user.email, self.key, len(self.skript))



@receiver(user_activated)
def user_activated_callback(sender, user, request, **kwargs):
    ud = Userdata(user=user)
    ud.save()

