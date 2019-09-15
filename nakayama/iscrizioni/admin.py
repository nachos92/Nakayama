from django.contrib import admin
from django.db.models import CharField
from django.contrib.auth import models as auth_models
from django.forms import TextInput, Textarea


from . import models

from django.contrib.admin import SimpleListFilter


class NullListFilter(SimpleListFilter):
	def lookups(self, request, model_admin):
		return (
			('1', 'Null', ),
			('0', '!= Null', ),
		)

	def queryset(self, request, queryset):
		if self.value() in ('0', '1'):
			kwargs = { '{0}__isnull'.format(self.parameter_name) : self.value() == '1' }
			return queryset.filter(**kwargs)
		return queryset


class StartNullListFilter(NullListFilter):
	title = u'Started'
	parameter_name = u'started'


class SomeModelAdmin(admin.ModelAdmin):
	list_filter = (StartNullListFilter, )


def null_filter(field, title_=None):
	""" Per poter aggiungere il filtro per vedere se un campo e' valorizzato o meno

	:param field:
	:param title_:
	:return:
	"""

	class NullListFieldFilter(NullListFilter):
		parameter_name = field
		title = title_ or parameter_name
	return NullListFieldFilter


class TesseratoAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'nome',
		'cognome',
	]

	search_fields = ['nome', 'cognome']
	# fields = ('nome', 'cognome',)
	list_filter = [
		# null_filter('foto_tessera')
		# 'residenza',
	]


class IscrizioneAdmin(admin.ModelAdmin):
	autocomplete_fields = ['iscritto']
	search_fields = ['iscritto__nome', 'iscritto__cognome']
	list_display = [
		# 'id',
		'iscritto',
		'anno_iscrizione',
		'scadenza_certificato_medico',
		# 'data_iscrizione',
		'flag_karate',
		'flag_fitness',
		'flag_corsi',
	]

	list_filter = [
		'anno_iscrizione',
		# 'flag_karate',
		# 'flag_corsi',
		# 'flag_fitness'
	]

	sortable_by = ['anno_iscrizione', 'iscritto', 'data_iscrizione', 'scadenza_certificato_medico']
	fieldsets = (
			(
				None, {
					'fields': ('iscritto', 'data_iscrizione', 'scadenza_certificato_medico')
				}
			),
			(
				'Attivita', {
					'fields': (
						# ('flag_karate', 'flag_fitness', 'flag_corsi'),
						'note',
					)
				}
			),
			(
				'Modulistica', {
					'fields': (
						('modulo_da_firmare',),
					)
				}
			)

	)

	def certificato_medico_salvato(self, obj):
		return obj.has_certificato_medico()
	certificato_medico_salvato.boolean = True


class IscrizioneKarateAdmin(IscrizioneAdmin):
	formfield_overrides = {
		CharField: {'widget': TextInput(attrs={'size': '25%'})},
	}

	fieldsets = (
		(
			None, {
				'fields': ('iscritto', 'data_iscrizione', 'scadenza_certificato_medico')
			}
		),
		(
			'Cinture', {
				'fields': (
					('cintura_bianca', 'cintura_blu', 'cintura_3_dan',),
					('cintura_gialla', 'cintura_marrone', 'cintura_4_dan',),
					('cintura_arancio', 'cintura_1_dan', 'cintura_5_dan',),
					('cintura_verde', 'cintura_2_dan', 'cintura_6_dan',),
				)
			}
		),
		(
			'Altro', {
				'fields': (
					('note', 'modulo_da_firmare',),
				)
			}
		)
	)

	def save_model(self, request, obj, form, change):
		super(IscrizioneKarateAdmin, self).save_model(request, obj, form, change)
		#todo genero il pdf
		obj.note = '666'
		obj.save()


admin.site.register(models.Tesserato, TesseratoAdmin)
admin.site.register(models.IscrizioneKarate, IscrizioneKarateAdmin)
admin.site.register(models.IscrizioneFitness, IscrizioneAdmin)

admin.site.unregister(auth_models.Group)
admin.site.unregister(auth_models.User)

admin.site.site_header = ("Palestra Nakayama")
admin.site.site_title = ("Nakayama")
admin.site.index_title = ("Gestione iscrizioni")

