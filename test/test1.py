from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os

# I will use docling for parsing the pdf because it can also extract scanned pdfs

# Docling PDF Parsing
def parse_with_docling(pdf_path):
    """
    Parses a PDF using Docling, extracts markdown content, 
    and prints the full extracted content.
    """
    # I have to prepare the pdf for the LLM, these are common steps in a RAG pipeline
    # markdown uses simple syntax like hashes, stars to represent tables, all paras
    # llms are able to easily understand this formatting, and make sense of it.
    try:
        # ensure file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")

        # Initialize Docling Converter
        converter = DocumentConverter()
        markdown_document = converter.convert(pdf_path).document.export_to_markdown()

        # we use headers for semantic chunking, llms have a limit on how much 
        # text they can read at once, which is called the context window
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        
        # Initialize Markdown Splitter
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        docs_list = markdown_splitter.split_text(markdown_document)

        # Print full extracted sections
        print("Full Extracted Content (Docling):")
        for idx, doc in enumerate(docs_list):
            print(f"\n🔹 Section {idx + 1}:\n{doc}\n" + "-"*80)

        return docs_list

    except Exception as e:
        print(f"Error during Docling processing: {e}")
        return []

### 🔹 LangChain PDF Parsing
def parse_with_langchain(pdf_path):
    """
    Parses a PDF using LangChain's PyPDFLoader and prints the full extracted text.
    """
    try:
        # Ensure file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")

        # Load PDF using PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Extract text from all pages
        text = "\n\n".join([page.page_content for page in pages])

        # Print full extracted content
        print("\nFull Extracted Content (LangChain):\n")
        print(text)
        print("\n" + "="*100)

        return text

    except Exception as e:
        print(f" Error during LangChain processing: {e}")
        return ""

