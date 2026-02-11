from docx import Document
from typing import List
from bot.structure import QuestionBlock
import copy

class DocxGenerator:
    def __init__(self, original_file_path: str):
        # We load the original file to keep styles and relationships (images)
        self.doc = Document(original_file_path)
        # Clear body content to start fresh (but keep styles/rels)
        self._clear_body()

    def _clear_body(self):
        # Simplest way to clear body while keeping relationships is to remove all paragraphs/tables
        # But efficiently:
        for element in self.doc.element.body:
            self.doc.element.body.remove(element)

    def generate(self, blocks: List[QuestionBlock], output_path: str):
        """
        Writes blocks to the document and saves it.
        Problem: We need to COPY paragraphs from the original parsed source.
        But 'blocks' contains references to paragraphs from a DIFFERENT Document object (the Parser's).
        
        CRITICAL: python-docx objects are bound to their parent Document. 
        We cannot simply 'append' a Paragraph from Doc A to Doc B.
        
        Solution (Image Handling):
        We must use the SAME Document object for Parsing and Generation if we want to easily preserve images by moving XML.
        OR
        We need to deep copy the XML element and insert it into the new document, 
        AND ensure relationships (images) are copied.
        
        Complexity reduction:
        Instead of creating a NEW blank document, we can:
        1. Open Original File (as Template).
        2. Clear all content (xml body).
        3. Insert the XML elements of the paragraphs we want to keep, in the new order.
        
        Blocks contain `original_paragraphs`. These are directly from `docx` library.
        Valid approach:
        1. Generate list of ALL paragraphs in correct order (Q1, A1, A2, Q2...).
        2. Create a new DOCX based on original (to keep image relationship parts).
        3. Replace body with new ordered paragraphs.
        """
        
        # This is a complex XML manipulation if we move between documents.
        # But we can re-use the parsing document logic?
        # No, 'parser' opened the doc. We should probably pass the 'doc' object or path.
        # Implemented Strategy: The 'blocks' hold references to paragraphs from the parsed document.
        # We will iterate over the blocks and append their XML to self.doc.body.
        
        pass  # Implementation detail in next step
        
        # Real implementation:
        body = self.doc.element.body
        
        for i, q in enumerate(blocks, 1):
            # 1. Question Text/Image
            for para in q.question_paragraphs:
                # We need to clone the specific paragraph element
                # Because if we just move it, it disappears from original place (which is fine if we don't need it)
                # But safer to append copy.
                self._append_element(body, para._element)
            
            # 2. Answers
            for ans in q.answers:
                for para in ans.original_paragraphs:
                    self._append_element(body, para._element)
            
            # 3. Add spacing between questions (Stage 34)
            self.doc.add_paragraph("") 

        self.doc.save(output_path)

    def _append_element(self, body, element):
        """
        Appends a copy of the element to the body.
        """
        # We need a deep copy of the XML element to avoid issues
        import copy
        new_elem = copy.deepcopy(element)
        body.append(new_elem)
