import datetime
from django.db import connection


def get_current_date(only_date=False, to_string=False):

	valore = datetime.datetime.now().date() if only_date else datetime.datetime.now()
	if to_string:
		time = valore.strftime("%H:%M:%S")
		return time
	return valore


def get_current_year():
	return datetime.datetime.now().year


def get_anno_scolastico():
	""" Ritorno l'anno nel formato es. 2019/2020

	:return:
	"""

	numero_mese = datetime.datetime.now().month
	anno = datetime.datetime.now().year

	# TODO CONTROLLO SUL RANGE DI DATE

	if numero_mese >= 9:
		stringa = "{0}/{1}".format(anno, anno+1)
	else:
		stringa = "{0}/{1}".format(anno-1, anno)

	return stringa


def run_query(sql):
	with connection.cursor() as cursor:
		cursor.execute(sql)
		row = cursor.fetchone()

		return row