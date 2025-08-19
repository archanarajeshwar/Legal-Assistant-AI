import logging
from utils.utils import logging
import os


class DataExtractionInitialise:
	def __init__(self):
		self.datapath = 'objects/data'

	def read_files(self):
		self.filenames = os.listdir(self.datapath)
		return self.filenames


class DataExtraction:
	def __init__(self):
		self.data_extraction_init = DataExtractionInitialise()
		self.filenames = self.data_extraction_init.read_files()


	def extract_data(self):
		for filename in self.filenames:
			logging.info(filename)



if __name__=="__main__":
	data_extraction = DataExtraction()
	data_extraction.extract_data()