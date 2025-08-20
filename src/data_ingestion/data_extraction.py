import logging
import os
from PyPDF2 import PdfReader

from src.utils.logger import logging

class DataExtractionInitialise:
	def __init__(self):
		self.datapath = 'objects/data'
		self.start_page = 1
		self.end_page = -1

	def read_file_names(self):
		try:
			self.filenames = ["COI_2024.pdf"] #os.listdir(self.datapath)
			return self.filenames
		except Exception as e:
			logging.error(f"Error occured during reading filepath. {e}")


class DataExtraction:
	def extract_data(self, filepath):
		try:
			text = ""
			reader = PdfReader(filepath)
			for page_num in range(len(reader.pages)):
				if page_num <=10:
					page = reader.pages[page_num]
					text += " " + page.extract_text()
					logging.info(f"Extracted page {page_num}")
			return text

		except Exception as e:
			logging.error(f"Error occured during reading file. {e}")


	def filter_text(self, text):
		formatted_text = list(text.replace('\n', ' ').strip())
		final_text = []
		for char in formatted_text:
			if char.isalpha() or char.isdigit() or char == ' ':
				final_text.append(char)
		return final_text



def Extraction():
	data_extraction_init = DataExtractionInitialise()
	filenames = data_extraction_init.read_file_names()

	data_extraction = DataExtraction()
	data = []
	for filename in filenames[:1]: # currently reading only the first file
		filepath = os.path.join(data_extraction_init.datapath, filename)
		logging.info(filepath)

		text = data_extraction.extract_data(filepath)
		data.append(''.join(data_extraction.filter_text(text)))
	return data




if __name__=="__main__":
	data = Extraction()
	print(data)