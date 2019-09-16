from __future__ import print_function
import pdfrw
import pypdftk
from mailmerge import MailMerge


from django.conf import settings

# INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/invoice_template.pdf'
INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/template_fitness.docx'
INVOICE_OUTPUT_PATH = settings.MEDIA_ROOT + 'docs/compilato_xx.docx'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def write_fillable_pdf(data_dict, input_pdf_path=INVOICE_TEMPLATE_PATH, output_pdf_path=INVOICE_OUTPUT_PATH):
	""" Genera il pdf a partire dal template e popolando i campi

	:param input_pdf_path: Percorso del pdf compilabile
	:param output_pdf_path: Percorso file di output
	:param data_dict: Coppie campo_pdf-valore
	:return:
	"""
	print("Inizio a scrivere il pdf...")
	template_pdf = pdfrw.PdfReader(input_pdf_path)
	annotations = template_pdf.pages[0][ANNOT_KEY]
	for annotation in annotations:
		if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
			if annotation[ANNOT_FIELD_KEY]:
				key = annotation[ANNOT_FIELD_KEY][1:-1]
				if key in data_dict.keys():
					annotation.update(
						pdfrw.PdfDict(V='{}'.format(data_dict[key]))
					)
	pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
	print("PDF creato!")



def popola_pdf():
	data_dict = {
		'cognome': 'Pasticcia',
		'nome': 'Ciccia'
	}
	generated_pdf = pypdftk.fill_form(INVOICE_TEMPLATE_PATH, data_dict)
	out_pdf = pypdftk.concat([INVOICE_OUTPUT_PATH, generated_pdf])


def popola_doc():
	document = MailMerge(INVOICE_TEMPLATE_PATH)
	print(document.get_merge_fields())

	data_dict = {
		'cognome': 'Pasticcia',
		'nome': 'Ciccia'
	}
	document.merge(**data_dict)
	document.write(INVOICE_OUTPUT_PATH)
