from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
import os
import hashlib
from pathlib import Path
import pickle


class Document_Processor:

    def __init__(self, cache_folder="smart_cache"):
        # We use Pathlib here instead of os.path
        self.cache_dir = Path(cache_folder)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_file_fingerprint(self, file_path: str) -> str:
        """
        Reads a file and generates a unique string based on its contents.
        If the file changes even slightly, this string will completely change.
        """
        # 1. opening the file in read-binary mode to read raw data, not text
        with open(file_path, "rb") as file:
            raw_bytes = file.read()
            
        # 2. use SHA-256 math to turn those bytes into a unique string of text
        fingerprint = hashlib.sha256(raw_bytes).hexdigest()
        
        return fingerprint
    

    def parse_and_split(self, file_path: str) -> list:
            """
            Converts a PDF to Markdown and splits it cleanly using headers.
            """
            print(f"Starting conversion for: {file_path}")
            
            # Convert the PDF to a single big Markdown string using Docling
            converter = DocumentConverter()
            result = converter.convert(file_path)
            markdown_text = result.document.export_to_markdown()

            # Define the header hierarchy for LangChain
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2")
            ]

            # Creating the splitter tool
            splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
            
            # 4. Doing the actual cutting, by creating chunks
            chunks = splitter.split_text(markdown_text)

            print(f"Successfully split into {len(chunks)} chunks!")
            return chunks
        
    # compute the total size of files to see within limit
    # def validate_files(self):
    #     pass
    
    # # this function is to make life easier by generating a clean cache name,
    # def _get_cache_path(self, pdf_path):
    #     '''
    #     takes in a string, pdf_path and returns a string, which is new cache file path
    #     '''
    #     # basename strips off all folder names, and leaves only the name of the file
    #     # If pdf_path is "users/documents/resumes/my_resume.pdf", it returns
    #     # my_resume_chunks.json
    #     basename = os.path.basename(pdf_path)
    #     json_name = os.path.splitext(basename)[0] + "_chunks.json"
    #     os.path.join(self.cache_dir, json_name)
    # we dont use this, we do hashing which avoids loading old cache by mistake
        

    def process_document(self, file_path: str) -> list:
        """
        The main engine. It checks the cache using the file's fingerprint.
        If cached, it loads it instantly. If not, it parses and saves it.
        """
        print(f"--- Processing: {file_path} ---")
        
        # 1. Get the unique digital fingerprint of the file
        fingerprint = self.get_file_fingerprint(file_path)
        
        # 2. Create the cache file path (e.g., smart_cache/a3f9b2...pkl)
        cache_file = self.cache_dir / f"{fingerprint}.pkl"
        
        # 3. THE SHORTCUT: Check if we already did this work
        if cache_file.exists() and cache_file.stat().st_size > 0:
            print("-> Match found in cache! Loading instantly...")
            # "rb" means read binary. Pickle thaws the objects.
            with open(cache_file, "rb") as f:
                cached_chunks = pickle.load(f)
            return cached_chunks
            
        # 4. THE LONG WAY: No cache found. We have to do the hard work.
        print("-> No cache found. Passing to Docling and LangChain...")
        chunks = self.parse_and_split(file_path)
        
        # 5. Save the work for next time
        # "wb" means write binary. Pickle freezes the objects to the disk.
        with open(cache_file, "wb") as f:
            pickle.dump(chunks, f)
            
        print(f"-> Saved to cache: {cache_file.name}")
        return chunks


if __name__ == "__main__":
    processor = Document_Processor()
    
    # Replace this with a real PDF path on your computer
    test_pdf = "example_pdfs/Rishabh_Mehra_Resume_2026.pdf" 
    
    # Run it once (Will take a few seconds to process)
    chunks_run_1 = processor.process_document(test_pdf)
    
    # Run it again (Will be instant!)
    chunks_run_2 = processor.process_document(test_pdf)
    
    # Look at how smart LangChain is:
    print("\n--- Let's look at the first chunk! ---")
    print("Metadata (The Headers):", chunks_run_1[0].metadata)
    print("Content:", chunks_run_1[0].page_content[:100], "...\n")
    
    
# what are the steps in order?
# 1. load the pdf
# 2. turn document into text/markdown
# 3. break text into smaller pieces(chunks)
# 4. start a local database , here I will use chroma db
# 5. i need to save those pieces with some ids and names
