import datetime


def get_current_date():
	return datetime.datetime.now()


def get_current_year():
	return datetime.datetime.now().year


def get_anno_scolastico():
	numero_mese = datetime.datetime.now().month
	anno = datetime.datetime.now().year

	if numero_mese >= 9:
		return anno+1

	return anno
