from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now as django_now
from django.contrib import admin

from . import utils


class Tesserato(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=30)
	cognome = models.CharField(max_length=30)
	data_di_nascita = models.DateField()
	codice_fiscale = models.CharField(max_length=16, default='')
	email = models.EmailField(blank=True)

	foto_tessera = models.ImageField(blank=True)

	class Meta:
		verbose_name = "Tesserato"
		verbose_name_plural = "Tesserati"

	def __str__(self):
		return "{0} {1}".format(self.cognome, self.nome)


class Iscrizione(models.Model):
	""" Iscrizione a base annuale """
	iscritto = models.ForeignKey(Tesserato, on_delete=models.CASCADE)
	data_iscrizione = models.DateField(default=django_now)

	anno_iscrizione = models.CharField(
		max_length=4,
		default=utils.get_current_year()
	)

	certificato_medico = models.FileField(blank=True)

	note = models.TextField(blank=True, default='')

	flag_fitness = models.BooleanField(default=False, verbose_name="Fitness")
	flag_karate = models.BooleanField(default=False, verbose_name="Karate")
	flag_corsi = models.BooleanField(default=False, verbose_name="Corsi")

	class Meta:
		verbose_name = "Iscrizione"
		verbose_name_plural = "Iscrizioni"

	def clean(self):
		if not (self.flag_corsi or self.flag_fitness or self.flag_karate):
			raise ValidationError("Selezionare attività")

	def __str__(self):
		return "{0} {1} - {2}".format(
			self.iscritto.cognome,
			self.iscritto.nome,
			self.anno_iscrizione
		)