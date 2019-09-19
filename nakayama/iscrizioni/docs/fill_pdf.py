from __future__ import print_function
from mailmerge import MailMerge
from django.conf import settings

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2


def popola_doc(data_dict, filename, tipo_iscrizione):
	""" Abbina ai tag del template i valori passati in ingresso

	:param data_dict: bindings nome_tag -> valore
	:param filename: nome+estensione del file (.docx)
	:param tipo_iscrizione: Karate/Fitness (K/F)
	:return:
	"""

	output_file_path = 'docs/modulistica/{filename}'.format(**locals())
	INVOICE_OUTPUT_PATH = settings.MEDIA_ROOT + output_file_path

	if tipo_iscrizione == 'F':
		INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/base/template_fitness.docx'
	else:
		INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/base/template_karate.docx'

	document = MailMerge(INVOICE_TEMPLATE_PATH)
	document.merge(**data_dict)
	document.write(INVOICE_OUTPUT_PATH)    # sovrascrive se esistente

	doc = DocxTemplate(INVOICE_OUTPUT_PATH)
	context = data_dict.copy()
	
	# aggiungo fototessera se presente
	if data_dict.get('fototessera'):
		path_immagine = data_dict['fototessera']
		myimage = InlineImage(doc, path_immagine, height=Mm(45), width=Mm(30))
		context['foto'] = myimage

	jinja_env = jinja2.Environment(autoescape=True)

	doc.render(context, jinja_env)
	doc.save(INVOICE_OUTPUT_PATH)

	return output_file_path


