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
        # converts the pdf to markdown, cut it by its headers,
        # cache it and then return the chunks.
        """
        Converts PDF to Markdown, cuts it by headers, caches it, and returns the chunks.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Source PDF not found at: {pdf_path}")

        cache_file = self._get_cache_path(pdf_path)

        # Step A: Check if we have already processed this file in the past
        if os.path.exists(cache_file):
            print(f"-> Found cached chunks for {os.path.basename(pdf_path)}. Loading from disk...")
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)

        # Step B: No cache found. Let's parse!
        print(f"-> Parsing {os.path.basename(pdf_path)} with Docling (this may take a moment)...")
        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        markdown_content = result.document.export_to_markdown()

        # Step C: Chunk the document by Level 2 headers (##)
        print("-> Splitting document into structural chunks...")
        raw_parts = markdown_content.split("\n## ")
        chunks = []
        for part in raw_parts:
            cleaned = part.strip()
            if cleaned:
                # Put the header marker back so the text retains its structural context
                chunks.append(f"## {cleaned}")

        # Step D: Save to cache so we never have to parse this exact file again
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        print(f"-> Chunks successfully saved to cache: {cache_file}")

        return chunks
            
        
        


# what are the steps in order?
# 1. load the pdf
# 2. turn document into text/markdown
# 3. break text into smaller pieces(chunks)
# 4. start a local database , here I will use chroma db
# 5. i need to save those pieces with some ids and names
