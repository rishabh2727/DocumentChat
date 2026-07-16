from docling.document_converter import DocumentConverter
import os

converter = DocumentConverter()
result = converter.convert("example_pdfs/Rishabh_Mehra_Resume_2026.pdf")
print(result)

class Document_Processor:
    def __init__(self,cache_dir = "./processed_chunks"):
        
        # instance attributes for the class
        #  predefined header structure for Markdown-based chunking
        self.headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
        self.cache_dir = cache_dir
        
        # if the folder does not exist yet, this will create it
        os.makedirs(self.cache_dir, exist_ok = True)
        
    
    # compute the total size of files to see within limit
    def validate_files(self):
        pass

    def process_pdf(self):
        # check if a cached version of this pdf already exists
        if self.cache_dir:
            
        
        


# what are the steps in order?
# 1. load the pdf
# 2. turn document into text/markdown
# 3. break text into smaller pieces(chunks)
# 4. start a local database , here I will use chroma db
# 5. i need to save those pieces with some ids and names
