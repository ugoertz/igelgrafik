from igelmain.models import Kapitel, Beispiel, Aufgabe, Kategorie, Skript
from django.contrib import admin

class KapitelAdmin(admin.ModelAdmin):
    fields = ['titel', 'kategorie', 'platz', 'zusammenfassung', 'quelltext', 'bild', ]

    class Media:
        css = {'all': ('css/admin.css', ), }


admin.site.register(Kapitel, KapitelAdmin)

class KategorieAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'intro', 'details', 'position']

    class Media:
        css = {'all': ('css/admin.css', ), }

admin.site.register(Kategorie, KategorieAdmin)

class BeispielAdmin(admin.ModelAdmin):
    fields = ['titel', 'autor', 'quelltext', 'bild', 'category' ]

    class Media:
        css = {'all': ('css/admin.css', ), }

admin.site.register(Beispiel, BeispielAdmin)

class AufgabeAdmin(admin.ModelAdmin):
    fields = ['titel', 'kategorie', 'platz', 'zusammenfassung', 'quelltext', 'bild', ]

    class Media:
        css = {'all': ('css/admin.css', ), }

admin.site.register(Aufgabe, AufgabeAdmin)


class SkriptAdmin(admin.ModelAdmin):
    pass
admin.site.register(Skript, SkriptAdmin)
