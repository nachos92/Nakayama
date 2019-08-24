from django.db import models
from django.utils.timezone import now as django_now
from . import utils


class IscrittoBase(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=30)
	cognome = models.CharField(max_length=30)
	data_di_nascita = models.DateField()
	codice_fiscale = models.CharField(max_length=16, default='')
	email = models.EmailField(blank=True)

	certificato_medico = models.FileField(blank=True)

	def __str__(self):
		return "[{0}] {1} {2}".format(self.id, self.cognome, self.nome)


class IscrittoKarate(IscrittoBase):
	note = models.TextField(max_length=100, blank=True)


class Persona(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=30)
	cognome = models.CharField(max_length=30)
	data_di_nascita = models.DateField()
	codice_fiscale = models.CharField(max_length=16, default='')
	email = models.EmailField(blank=True)

	class Meta:
		verbose_name = "Iscritto"
		verbose_name_plural = "Iscritti"

	def __str__(self):
		return "{0} {1}".format(self.cognome, self.nome)


class Iscrizione(models.Model):
	""" Iscrizione a base annuale """
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
	anno_iscrizione = models.CharField(max_length=4)

	data_iscrizione = models.DateField(default=django_now)
	certificato_medico = models.FileField(blank=True)

	class Meta:
		verbose_name = "Iscrizione"
		verbose_name_plural = "Iscrizioni"

	def __str__(self):
		return "[{0}] - {1}".format(self.anno_iscrizione, self.persona.cognome)