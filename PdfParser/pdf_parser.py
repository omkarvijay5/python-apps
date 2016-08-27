#!/usr/bin/env python
#Standard imports
import logging
#Imports related to pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.psparser import PSLiteral
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdftypes import PDFObjRef
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextBoxVertical
from pdfminer.converter import PDFPageAggregator

from collections import defaultdict, namedtuple

# default configuration dictionary which will be initialized when
# PdfParser objects are created

DEFAULTS = {"input_pdf_file": "inputfile.pdf",
            #"parsed_output_text" : "hello",
            }

# dictionary of configured values
conf = {}
TextBlock= namedtuple("TextBlock", ["x", "y", "text"])

class PdfParserException(Exception):
    """ 
    Generic exception for Parsing operations 
    """
    def __init__(self):
        pass

class PdfParser:

    """ 
    This provides object to encapsulate metadata about Python parser
    """
    def __init__(self, conf):

        """
        Initialize the `PdfParser` config values.
        Contains dictionary of config values.
        """

        # Where all the output text from the pdf parser is stored. 
        #self.parsed_output_text = conf.get("parsed_output_text", \  
        #                        DEFAULTS["parsed_output_text"])

        #Initialize output text as key value pairs

        self.parsed_output_text = {}
        # Innitializing the input PDF file
        self.input_pdf_file = conf.get("input_pdf_file",  \
                              DEFAULTS["input_pdf_file"])

        #self.horizontal_tables = {}
        #initializing all the fields as blank for now
        self.company_record = {
                'id':'',
                'description':'',
                'date_uploaded': '',
                'bizfile_date':'',
                'receipt_no' : '',
                'registration_no':'',
                'company_name': '',
                'former_name':'',
                'incorp_date':'',
                'company_type':'',
                'status': '',
                'status_date':'',
                'activities_1':'',
                'activites_description':'',
                'activities_2':'',
                'activites_description_2':'',
                'registered_office_address':'',
                'date_of_address':'',
                'date_of_last_agm':'',
                'date_of_last_ar':'',
                'date_of_ac_at_last':'',
                'date_of_lodgment_of_ar':'',
                'audit_firm_name':'',
                'organization':'',
            }
    

class PdfParserProvider:

    """
    This class is used to provide the implementation for the PdfParser class
    """
    def load_pdf_file(self,parser_obj):

    	print parser_obj.input_pdf_file
        print parser_obj.parsed_output_text
        # Open the PDF file 
    	file_obj = open(parser_obj.input_pdf_file,'rb')
        
        # Create the parser object associated with the file object
        pdf_parser_obj = PDFParser(file_obj)

        # Create the pdf document object that stores the 
        # document structure
        document_obj = PDFDocument(pdf_parser_obj)

        # Connect the parser and the document objects
        pdf_parser_obj.set_document(document_obj)
     
        # document_obj.set_parser(parser_obj)

        # Create a resource manager object that stores 
        # shared resources
        resource_manager_obj = PDFResourceManager()

        #Set parameters for analysis
        laparams = LAParams(detect_vertical=True, all_texts=True)
      
        #laparams = LAParams(detect_vertical=True,line_margin=0.3)
        #Create PDF aggregator object
        pdf_aggregator_obj = PDFPageAggregator(resource_manager_obj, \
                                                  laparams=laparams)

        # Create a PDF interpreter object.
        interpreter_obj = PDFPageInterpreter(resource_manager_obj, \
                                               pdf_aggregator_obj)
       
        # Create page aggregator object
        # Process each page contained in the document.
        for page_num, page in enumerate(PDFPage.create_pages(document_obj)):
            interpreter_obj.process_page(page)
            if page.annots:
                self._build_annotations( page )
            page_text = self._get_text(parser_obj, pdf_aggregator_obj)
            #TODO: Need to copy the data into parsed_output_text variable
            parser_obj.parsed_output_text[page_num + 1] = page_text
            #parser_obj.parsed_output_text.append(page_text)
            #print page_text
       
    """
    To fetch the text from the pdf_aggregator_obj
    """
    def _get_text(self, parser_obj, pdf_aggregator_obj):
        temporary_text = []
        temporary_horizontal_table = {}
        layout = pdf_aggregator_obj.get_result()
        for layout_obj in layout:
            if isinstance( layout_obj, LTTextBoxHorizontal ):
                if layout_obj.get_text().strip():
                    temporary_text.append( TextBlock(layout_obj.x0, \
                            layout_obj.y1, layout_obj.get_text().strip()) )
                    #TODO: Not the pythonic way to write the code
                    #Need to fix it
                    if layout_obj.y1 in temporary_horizontal_table.keys():
                        temporary_horizontal_table[layout_obj.y1].append( \
                                layout_obj.get_text().strip())
                    elif (layout_obj.y1 + 4) in temporary_horizontal_table.keys():
                        temporary_horizontal_table[layout_obj.y1 + 4].append( \
                                layout_obj.get_text().strip())
                    elif (layout_obj.y1 - 4) in temporary_horizontal_table.keys():
                        temporary_horizontal_table[layout_obj.y1 - 4].append( \
                                layout_obj.get_text().strip())
                    else:
                        temporary_horizontal_table[layout_obj.y1] = \
                        [layout_obj.get_text().strip()]

        #Appending the key value pairs in the dictionary
        self.populate_company_record_table(parser_obj,temporary_horizontal_table)
        temporary_text.sort( key=lambda row: (row.x, -row.y) )
        return temporary_text


    """
    Populates records in company records table
    """
    def populate_company_record_table(self,parser_obj,temporary_horizontal_table):
        for key, value in temporary_horizontal_table.iteritems():
            #print key, "\t", value, "\t"
            if 'Registration No.' in value:
                parser_obj.company_record['registration_no'] = value[0]
            elif 'Company Name.' in value:
                parser_obj.company_record['company_name'] = value[0]
            elif 'Former Name if any' in value:
                parser_obj.company_record['former_name'] = value[0]
            elif 'Incorporation Date.' in value:
                parser_obj.company_record['incorp_date'] = value[0]
            elif 'Company Type' in value:
                parser_obj.company_record['company_type'] = value[0]
            elif 'Status' in value:
                parser_obj.company_record['status'] = value[0]
            elif 'Status Date' in value:
                parser_obj.company_record['status_date'] = value[0]
            elif 'Activities (I)' in value:
                parser_obj.company_record['activities_1'] = value[0]
            elif 'Activities (II)' in value:
                parser_obj.company_record['activities_2'] = value[0]
            elif 'Description' in value:
                parser_obj.company_record['activities_description'] = value[0]
            elif 'Registered Office Address' in value:
                parser_obj.company_record['registered_office_address'] = value[0]
            elif 'Date of Address' in value:
                parser_obj.company_record['date_of_address'] = value[0]
            elif 'Date of Last AGM' in value:
                parser_obj.company_record['date_of_last_agm'] = value[0]
            elif 'Date of Last AR' in value:
                parser_obj.company_record['date_of_last_ar'] = value[0]
            elif 'Date of A/C Laid at Last AGM' in value:
                parser_obj.company_record['date_of_ac_at_last'] = value[0]
            elif 'Date of Lodgment of AR, A/C' in value:
                parser_obj.company_record['date_of_lodgment_of_ar'] = value[0]



    def _build_annotations( self, parser_obj, page ):
        for annot in page.annots.resolve():
            if isinstance( annot, PDFObjRef ):
                annot= annot.resolve()
                assert annot['Type'].name == "Annot", repr(annot)
                if annot['Subtype'].name == "Widget":
                    if annot['FT'].name == "Btn":
                        assert annot['T'] not in self.fields
                        self.fields[ annot['T'] ] = annot['V'].name
                    elif annot['FT'].name == "Tx":
                        assert annot['T'] not in self.fields
                        self.fields[ annot['T'] ] = annot['V']
                    elif annot['FT'].name == "Ch":
                        assert annot['T'] not in self.fields
                        self.fields[ annot['T'] ] = annot['V']
                        # Alternative choices in annot['Opt'] )
                    else:
                        raise Exception( "Unknown Widget" )
            else:
                raise Exception( "Unknown Annotation" )

def run_pdf_parser():
    parser_object = PdfParser(conf)
    provider_object = PdfParserProvider()
    provider_object.load_pdf_file(parser_object)
    #for i in parser_object.parsed_output_text:
    #	print parser_object.parsed_output_text.values()
    for key, value in parser_object.company_record.iteritems():
        print key, "\t", value
if __name__ == "__main__":
    run_pdf_parser()

