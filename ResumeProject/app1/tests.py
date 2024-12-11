from django.test import TestCase

# Create your tests here.
from pypdf import PdfReader

# reader = # creating a pdf reader object
reader = PdfReader('C://Users/sachi/Downloads/Nilesh-Resume_my.pdf.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# creating a page object
page = reader.pages[0]

# extracting text from page
print(page.extract_text())


# from ironpdf import *     # License.LicenseKey = " Your License Ket "
# # Load Scanned PDF document
# pdf = PdfDocument.FromFile("C:/Users/buttw/INV_2023_00008.pdf")
# # Extract text from PDF document
# all_text = pdf.ExtractAllText()
# print(all_text)
