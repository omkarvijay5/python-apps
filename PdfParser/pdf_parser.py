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

        #self.parsed_output_text = conf.get("parsed_output_text", \
        #                          DEFAULTS["parsed_output_text"])

        self.parsed_output_text = {}
        # Innitializing the input PDF file
        self.input_pdf_file = conf.get("input_pdf_file",  \
                              DEFAULTS["input_pdf_file"])

        self.horizontal_tables = {}

        # Number of pages in the document
        # self.number_of_pages = conf.get("number_of_pages", \
        #                       DEFAULTS["number_of_pages"])
        
        #TODO : Not a good design to include temporary tables in Parser object
        #Need to fix this. 
    

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
      
        #Create PDF aggregator object
        pdf_aggregator_obj = PDFPageAggregator(resource_manager_obj, laparams=laparams)

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
        temporary_text_1 = []
        temporary_horizontal_table_1 = {}
        temporary_horizontal_table_2 = {}
        temporary_vertical_table = {}
        layout = pdf_aggregator_obj.get_result()
        for layout_obj in layout:
            if isinstance( layout_obj, LTTextBoxHorizontal ):
                if layout_obj.get_text().strip():
                    temporary_text.append( TextBlock(layout_obj.x0, layout_obj.y1, layout_obj.get_text().strip()) )
                    if layout_obj.y1 in temporary_horizontal_table_1.keys():
                        #parser_obj.horizontal_tables[temporary_horizontal_table[layout_obj.y1]] = layout_obj.get_text().strip()   
                        #parser_obj.horizontal_tables[layout_obj.get_text().strip()] = parser_obj.temporary_horizontal_table[layout_obj.y1]
                        temporary_horizontal_table_2[layout_obj.y1] = layout_obj.get_text().strip()
                    else:
                        temporary_horizontal_table_1[layout_obj.y1] = layout_obj.get_text().strip()
    

        for key, value in temporary_horizontal_table_1.iteritems():
            print key, "\t", value.rstrip(), "\t"
            if key in temporary_horizontal_table_2.keys():
                print temporary_horizontal_table_2[key].strip()
            else:
                print "Blank"
            print "\n"

            #    temporary_text.append(layout_obj.get_text().strip())
            #if isinstance( layout_obj, LTTextBoxVertical ):
            #    temporary_text_1.append(layout_obj.get_text().strip())
        return temporary_text

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
    for i in parser_object.parsed_output_text:
    	print parser_object.parsed_output_text.values()
    #print parser_object.parsed_output_text
    
    #for i in parser_object.horizontal_tables
    #    print parser_object.horizontal_tables.keys(i), "\t" , parser_object.horizontal_tables.values(i)
    #for key, value in parser_object.temporary_horizontal_table_2.iteritems():
    #    print key, "\t", value, "\t"
    #    if key in parser_object.temporary_horizontal_table_1.keys():
    #        print parser_object.temporary_horizontal_table_1[key]
    #    else:
    #        print "Blank"
        #print "\n"

if __name__ == "__main__":
    run_pdf_parser()

