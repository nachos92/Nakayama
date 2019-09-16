from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now as django_now
from django.contrib import admin
from .docs import fill_pdf

from . import utils


class Tesserato(models.Model):
	id = models.AutoField(primary_key=True)

	nome = models.CharField(max_length=30, default='')
	cognome = models.CharField(max_length=30, default='')

	foto_tessera = models.ImageField(blank=True, verbose_name='Fototessera', upload_to='fototessere/')

	residenza = models.CharField(max_length=30, default='')
	cap = models.CharField(max_length=5, default='42123')
	via = models.CharField(max_length=50, default='')
	numero_civico = models.CharField(max_length=6, default='')
	telefono = models.CharField(max_length=20, default='')

	citta_di_nascita = models.CharField(max_length=30, default='')
	provincia_di_nascita = models.CharField(max_length=2, default='')
	data_di_nascita = models.DateField()

	codice_fiscale = models.CharField(max_length=16, default='')
	email = models.EmailField(blank=True)

	professione = models.CharField(max_length=40, default='')
	documento_di_riconoscimento = models.CharField(max_length=30, default='')

	class Meta:
		verbose_name = "Persona"
		verbose_name_plural = "Persone"

	def __str__(self):
		return "{0} {1}".format(self.cognome, self.nome)


class Iscrizione(models.Model):
	""" Iscrizione a base annuale """
	# id = models.AutoField(primary_key=True)
	iscritto = models.ForeignKey(Tesserato, on_delete=models.CASCADE)
	data_iscrizione = models.DateField(default=django_now)
	scadenza_iscrizione = models.DateField(blank=False, default=django_now)
	anno_iscrizione = models.CharField(max_length=9, default=utils.get_anno_scolastico())

	scadenza_certificato_medico = models.DateField(default=django_now)

	note = models.TextField(blank=True, default='')

	flag_fitness = models.BooleanField(default=False, verbose_name="Fitness")
	flag_karate = models.BooleanField(default=False, verbose_name="Karate")
	flag_corsi = models.BooleanField(default=False, verbose_name="Corsi")

	modulo_da_firmare = models.FileField(
		blank=True,
		help_text="Stampare e fare firmare",
		upload_to='moduli_iscrizione/'
	)

	def __str__(self):
		return "{0} {1} - {2}".format(
			self.iscritto.cognome.upper(),
			self.iscritto.nome.upper(),
			self.anno_iscrizione
		)

	class Meta:
		abstract = True
		verbose_name = "Iscrizione"
		verbose_name_plural = "Iscrizioni"
		unique_together = ('iscritto',)

	def clean(self):
		if not (self.flag_corsi or self.flag_fitness or self.flag_karate):
			raise ValidationError("Selezionare attività")

	def has_certificato_medico(self):
		test = self.scadenza_certificato_medico < utils.get_current_date()
		return test

	def genera_pdf_compilato(self):
		fill_pdf.popola_doc()


class IscrizioneKarate(Iscrizione):
	flag_karate = models.BooleanField(default=True, verbose_name="Karate")

	cintura_bianca = models.CharField(max_length=50, default='', blank=True)
	cintura_gialla = models.CharField(max_length=50, default='', blank=True)
	cintura_arancio = models.CharField(max_length=50, default='', blank=True)
	cintura_verde = models.CharField(max_length=50, default='', blank=True)
	cintura_blu = models.CharField(max_length=50, default='', blank=True)
	cintura_marrone = models.CharField(max_length=50, default='', blank=True)

	cintura_1_dan = models.CharField(max_length=50, default='', blank=True)
	cintura_2_dan = models.CharField(max_length=50, default='', blank=True)
	cintura_3_dan = models.CharField(max_length=50, default='', blank=True)
	cintura_4_dan = models.CharField(max_length=50, default='', blank=True)
	cintura_5_dan = models.CharField(max_length=50, default='', blank=True)
	cintura_6_dan = models.CharField(max_length=50, default='', blank=True)

	class Meta:
		verbose_name = "Iscrizione Karate"
		verbose_name_plural = "Iscrizioni Karate"
		unique_together = ('iscritto',)


class IscrizioneFitness(Iscrizione):
	flag_fitness = models.BooleanField(default=True, verbose_name="Fitness")

	class Meta:
		verbose_name = "Iscrizione Fitness"
		verbose_name_plural = "Iscrizioni Fitness"
		unique_together = ('iscritto',)