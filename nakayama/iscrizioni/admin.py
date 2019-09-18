from django.contrib import admin
from django.db.models import CharField
from django.contrib.auth import models as auth_models
from django.forms import TextInput
from . import utils

from . import models

from django.contrib.admin import SimpleListFilter


class NullListFilter(SimpleListFilter):
	def lookups(self, request, model_admin):
		return (
			('1', 'NO', ),
			('0', 'SI', ),
		)

	def queryset(self, request, queryset):
		if self.value() in ('0', '1'):
			kwargs = { '{0}__isnull'.format(self.parameter_name) : self.value() == '1' }
			return queryset.filter(**kwargs)
		return queryset


class StartNullListFilter(NullListFilter):
	title = u'Started'
	parameter_name = u'started'


class FiltroCertificatoMedico(SimpleListFilter):
	title = "certificato medico"
	parameter_name = 'certificato medico'

	def lookups(self, request, model_admin):
		return ('Yes', 'VALIDI'), ('No', 'SCADUTI'),

	def queryset(self, request, queryset):
		value = self.value()
		if value == 'Yes':
			return queryset.filter(scadenza_certificato_medico__gte=utils.get_current_date(only_date=True))
		elif value == 'No':
			return queryset.filter(scadenza_certificato_medico__lt=utils.get_current_date(only_date=True))
		return queryset


class FiltroAbbonamento(SimpleListFilter):
	title = "scadenza abbonamento"
	parameter_name = 'scadenza abbonamento'

	def lookups(self, request, model_admin):
		return ('Yes', 'VALIDI'), ('No', 'SCADUTI'),

	def queryset(self, request, queryset):
		value = self.value()
		if value == 'Yes':
			return queryset.filter(scadenza_iscrizione__gte=utils.get_current_date(only_date=True))
		elif value == 'No':
			return queryset.filter(scadenza_iscrizione__lt=utils.get_current_date(only_date=True))
		return queryset


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
		'iscritto',
		'anno_iscrizione',
		'scadenza_iscrizione',
		'scadenza_certificato_medico',
		'certificato_medico_valido',
		'abbonamento_valido',
	]

	list_filter = [
		'anno_iscrizione',
		FiltroCertificatoMedico,
		FiltroAbbonamento,
	]

	sortable_by = [
		'iscritto',
		'anno_iscrizione',
		'data_iscrizione',
		'scadenza_iscrizione',
		'scadenza_certificato_medico',
	]

	INNER_FIELDSETS = (None, {})

	FIELD_MODULI = (
				'Modulistica', {
					'fields': (
						'modulo_da_firmare',
					)
				}
			),

	fieldsets = (
			(
				None, {
					'fields': (
						'iscritto',
						('data_iscrizione', 'scadenza_iscrizione',),
						'scadenza_certificato_medico'
					)
				}
			),
	)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		obj.genera_pdf_compilato()


class IscrizioneFitnessAdmin(IscrizioneAdmin):

	fieldsets = IscrizioneAdmin.fieldsets + IscrizioneAdmin.FIELD_MODULI


class IscrizioneKarateAdmin(IscrizioneAdmin):
	formfield_overrides = {
		CharField: {'widget': TextInput(attrs={'size': '25%'})},
	}

	fieldsets = IscrizioneAdmin.fieldsets + (
		(
			'Cinture', {
				'fields': (
					('cintura_bianca', 'cintura_blu', 'cintura_3_dan',),
					('cintura_gialla', 'cintura_marrone', 'cintura_4_dan',),
					('cintura_arancio', 'cintura_1_dan', 'cintura_5_dan',),
					('cintura_verde', 'cintura_2_dan', 'cintura_6_dan',),
				)
			}
		),) + IscrizioneAdmin.FIELD_MODULI


admin.site.register(models.Tesserato, TesseratoAdmin)
admin.site.register(models.IscrizioneKarate, IscrizioneKarateAdmin)
admin.site.register(models.IscrizioneFitness, IscrizioneFitnessAdmin)

admin.site.unregister(auth_models.Group)
admin.site.unregister(auth_models.User)

admin.site.site_header = "Palestra Nakayama"
admin.site.site_title = "Nakayama"
admin.site.index_title = "Gestione iscrizioni"

