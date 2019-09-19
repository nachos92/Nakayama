from django.core.exceptions import ValidationError

MAX_MB_SIZE_FOTOTESSERA = 5


def validate_file_size(value):
	filesize = value.size

	if filesize > 10485760/10 * MAX_MB_SIZE_FOTOTESSERA:
		raise ValidationError("L'immagine e' troppo pesante (max 5MB)")
	else:
		return value