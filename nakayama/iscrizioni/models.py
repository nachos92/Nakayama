import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now as django_now
from .validators import validate_file_size

from .docs import fill_pdf


from . import utils


class Tesserato(models.Model):
	id = models.AutoField(primary_key=True)

	nome = models.CharField(max_length=30, default='')
	cognome = models.CharField(max_length=30, default='')

	foto_tessera = models.ImageField(
		blank=True, verbose_name='Fototessera',
		upload_to='fototessere/',
		validators=[validate_file_size]
	)

	residenza = models.CharField(max_length=30, default='')
	cap = models.CharField(max_length=5, default='42123')
	indirizzo = models.CharField(max_length=50, default='')
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
		return "{0} {1}".format(self.cognome.upper(), self.nome.upper())

	def to_dict(self, uppercase=False):
		data = {
			'cognome_nome': '{0} {1}'.format(self.cognome, self.nome),
			'nome': self.nome,
			'cognome': self.cognome,
			'residenza': self.residenza,
			'indirizzo': self.indirizzo,
			'cap': self.cap,
			'numero_civico': self.numero_civico,
			'telefono': self.telefono,
			'citta_di_nascita': self.citta_di_nascita,
			'data_di_nascita': self.data_di_nascita.strftime("%d/%m/%Y"),
			'provincia_di_nascita': self.provincia_di_nascita,
			'codice_fiscale': self.codice_fiscale,
			'email': self.email,
			'professione': self.professione,
			'documento_di_riconoscimento': self.documento_di_riconoscimento,
			'fototessera': self.foto_tessera.path if self.foto_tessera else None,
		}

		if uppercase:
			campi_da_non_toccare = ['fototessera', 'email']
			for key, value in data.items():
				if key in campi_da_non_toccare:
					continue

				data[key] = value.upper()

		return data


class Iscrizione(models.Model):
	""" Iscrizione a base annuale """
	# id = models.AutoField(primary_key=True)
	iscritto = models.ForeignKey(Tesserato, on_delete=models.CASCADE)
	data_iscrizione = models.DateField(default=django_now)
	scadenza_iscrizione = models.DateField(blank=False, default=django_now, verbose_name='Scadenza abbonamento')
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

	nome_file = "{cognome}_{nome}_{tipo}_{anno}.docx"
	_tipo_iscrizione = ''

	def get_name(self):
		return "Ciao"

	class Meta:
		abstract = True
		verbose_name = "Iscrizione"
		verbose_name_plural = "Iscrizioni"
		unique_together = ('iscritto',)
		ordering = ('iscritto__cognome',)

	def __str__(self):
		return "{0} {1} - {2}".format(
			self.iscritto.cognome.upper(),
			self.iscritto.nome.upper(),
			self.anno_iscrizione
		)

	def to_dict(self):
		dati_persona = self.iscritto.to_dict(True)
		return dati_persona

	def clean(self):
		if not (self.flag_corsi or self.flag_fitness or self.flag_karate):
			raise ValidationError("Selezionare attività")

	def get_lettera_tipo_iscrizione(self):
		return self._tipo_iscrizione

	def has_certificato_medico(self):
		test = self.scadenza_certificato_medico < utils.get_current_date()
		return test

	def anno_iscrizione_string(self):
		stringa = self.anno_iscrizione
		stringa = stringa.replace('/', '_')
		return stringa

	def genera_pdf_compilato(self):
		data_dict = self.to_dict()
		nome_file = self.nome_file.format(
			cognome=self.iscritto.cognome,
			nome=self.iscritto.nome,
			tipo=self.get_lettera_tipo_iscrizione(),
			anno=self.anno_iscrizione_string()
		)

		# creo il .docx
		filepath = fill_pdf.popola_doc(data_dict, nome_file, self.get_lettera_tipo_iscrizione())

		self.modulo_da_firmare = filepath
		self.save()

	def certificato_medico_valido(self):
		return self.scadenza_certificato_medico >= utils.get_current_date(only_date=True)

	def abbonamento_valido(self):
		return self.scadenza_iscrizione >= utils.get_current_date(only_date=True)

	abbonamento_valido.boolean = True
	certificato_medico_valido.boolean = True


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

	_tipo_iscrizione = 'K'

	class Meta:
		verbose_name = "Iscrizione Karate"
		verbose_name_plural = "Iscrizioni Karate"
		unique_together = ('iscritto',)

	def to_dict(self):
		data_persona = super().to_dict()

		data = {
			'cintura_bianca': self.cintura_bianca,
			'cintura_gialla': self.cintura_gialla,
			'cintura_arancio': self.cintura_arancio,
			'cintura_verde': self.cintura_verde,
			'cintura_blu': self.cintura_blu,
			'cintura_marrone': self.cintura_marrone,
			'cintura_1_dan': self.cintura_1_dan,
			'cintura_2_dan': self.cintura_2_dan,
			'cintura_3_dan': self.cintura_3_dan,
			'cintura_4_dan': self.cintura_4_dan,
			'cintura_5_dan': self.cintura_5_dan,
			'cintura_6_dan': self.cintura_6_dan,
		}
		data.update(data_persona)
		return data


class IscrizioneFitness(Iscrizione):
	flag_fitness = models.BooleanField(default=True, verbose_name="Fitness")

	_tipo_iscrizione = 'F'

	class Meta:
		verbose_name = "Iscrizione Fitness"
		verbose_name_plural = "Iscrizioni Fitness"
		unique_together = ('iscritto',)
