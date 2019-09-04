from django.contrib import admin
from django.contrib.auth import models
from django.contrib.auth import models as auth_models

from . import models


admin.site.site_header = ("Palestra Nakayama")
admin.site.site_title = ("Nakayama")
admin.site.index_title = ("Gestione iscrizioni")


class TesseratoAdmin(admin.ModelAdmin):

	list_display = [
		'id',
		'nome',
		'cognome'
	]

	search_fields = ['nome', 'cognome']
	# fields = ('nome', 'cognome',)


class IscrizioneAdmin(admin.ModelAdmin):
	list_filter = ['anno_iscrizione', 'flag_karate', 'flag_corsi', 'flag_fitness']
	autocomplete_fields = ['iscritto']
	search_fields = ['iscritto__nome', 'iscritto__cognome']
	list_display = [
		'id',
		'iscritto',
		'anno_iscrizione',
		'data_iscrizione',
		'flag_karate',
		'flag_fitness',
		'flag_corsi',
	]

	sortable_by = ['anno_iscrizione', 'iscritto', 'data_iscrizione']
	fieldsets = (
			(
				None, {
					'fields': ('iscritto', 'data_iscrizione')
				}
			),
				(
					'Attività', {
						'fields': (
							('flag_karate', 'flag_fitness', 'flag_corsi'),
							'note'
						)
					}
				),
	)

admin.site.register(models.Tesserato, TesseratoAdmin)
admin.site.register(models.Iscrizione, IscrizioneAdmin)

admin.site.unregister(auth_models.Group)
admin.site.unregister(auth_models.User)

