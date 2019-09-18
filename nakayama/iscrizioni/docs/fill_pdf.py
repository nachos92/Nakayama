from __future__ import print_function
from mailmerge import MailMerge
from django.conf import settings

import os

IS_PROD = False


def popola_doc(data_dict, filename, tipo_iscrizione):
	output_file_path = 'docs/modulistica/{filename}'.format(**locals())

	if tipo_iscrizione == 'F':
		INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/base/template_fitness.docx'
	else:
		INVOICE_TEMPLATE_PATH = settings.MEDIA_ROOT + 'docs/base/template_karate.docx'

	INVOICE_OUTPUT_PATH = settings.MEDIA_ROOT + output_file_path

	document = MailMerge(INVOICE_TEMPLATE_PATH)
	print(document.get_merge_fields())

	document.merge(**data_dict)
	document.write(INVOICE_OUTPUT_PATH)    # sovrascrive se esistente

	return output_file_path

