from __future__ import print_function
from mailmerge import MailMerge
from django.conf import settings
import os

IS_PROD = False

def popola_doc(data_dict, filename, tipo_iscrizione):

	if tipo_iscrizione == 'F':
		INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/template_fitness.docx'
	else:
		INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/template_karate.docx'

	INVOICE_OUTPUT_PATH = settings.MEDIA_ROOT + 'docs/{filename}'.format(**locals())

	document = MailMerge(INVOICE_TEMPLATE_PATH)
	print(document.get_merge_fields())

	document.merge(**data_dict)
	document.write(INVOICE_OUTPUT_PATH)    # sovrascrive se esistente

	if IS_PROD:
		os.system("abiword --to=pdf {}".format(INVOICE_OUTPUT_PATH))
		os.system("rm {}".format(INVOICE_OUTPUT_PATH))

