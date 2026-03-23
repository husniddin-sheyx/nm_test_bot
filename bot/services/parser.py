from typing import List, Tuple
from docx import Document
import openpyxl
from bot.structure import QuestionBlock, AnswerBlock

class DocxParser:
    def __init__(self, file_path: str):
        self.doc = Document(file_path)
        self.blocks: List[QuestionBlock] = []
        self.errors: List[str] = []

    def parse(self) -> Tuple[List[QuestionBlock], List[str]]:
        """
        Parses the document into QuestionBlocks using markers:
        ? - Question start
        + or = - Correct answer
        - - Incorrect answer
        """
        current_q_paragraphs = []
        current_answers = []
        current_ans_paragraphs = []
        current_ans_is_correct = False
        
        question_counter = 1

        def save_current_answer():
            if current_ans_paragraphs:
                current_answers.append(AnswerBlock(
                    original_paragraphs=list(current_ans_paragraphs),
                    is_correct=current_ans_is_correct,
                    debug_text=current_ans_paragraphs[0].text[:30] if current_ans_paragraphs else ""
                ))
                current_ans_paragraphs.clear()

        def save_current_question():
            nonlocal question_counter
            save_current_answer()
            if current_q_paragraphs:
                self.blocks.append(QuestionBlock(
                    id=question_counter,
                    question_paragraphs=list(current_q_paragraphs),
                    answers=list(current_answers)
                ))
                question_counter += 1
                current_q_paragraphs.clear()
                current_answers.clear()

        for para in self.doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            # 1. Identify Markers
            is_question = text.startswith("?")
            is_plus_equal = text.startswith("+") or text.startswith("=")
            is_minus = text.startswith("-")
            
            if is_question:
                save_current_question()
                current_q_paragraphs.append(para)
            elif is_plus_equal or is_minus:
                save_current_answer()
                current_ans_is_correct = is_plus_equal
                current_ans_paragraphs.append(para)
            else:
                # Continuation of current block
                if current_ans_paragraphs:
                    current_ans_paragraphs.append(para)
                elif current_q_paragraphs:
                    current_q_paragraphs.append(para)
        
        # Save last block
        save_current_question()
            
        return self.blocks, self.errors

class XlsxParser:
    def __init__(self, file_path: str):
        self.wb = openpyxl.load_workbook(file_path, data_only=True)
        self.blocks: List[QuestionBlock] = []
        self.errors: List[str] = []

    def parse(self) -> Tuple[List[QuestionBlock], List[str]]:
        """
        Parses Excel files. We assume each non-empty cell in the first column 
        is a line of text, similar to word paragraphs.
        """
        ws = self.wb.active
        lines = []
        for row in ws.iter_rows(values_only=True):
            for cell in row:
                if cell is not None:
                    lines.append(str(cell).strip())
        
        class ExcelPara:
            def __init__(self, text):
                self.text = text

        current_q_paras = []
        current_answers = []
        current_ans_paras = []
        current_ans_is_correct = False
        question_counter = 1

        def save_current_answer():
            if current_ans_paras:
                current_answers.append(AnswerBlock(
                    original_paragraphs=list(current_ans_paras),
                    is_correct=current_ans_is_correct,
                    debug_text=current_ans_paras[0].text[:30] if current_ans_paras else ""
                ))
                current_ans_paras.clear()

        def save_current_question():
            nonlocal question_counter
            save_current_answer()
            if current_q_paras:
                self.blocks.append(QuestionBlock(
                    id=question_counter,
                    question_paragraphs=list(current_q_paras),
                    answers=list(current_answers)
                ))
                question_counter += 1
                current_q_paras.clear()
                current_answers.clear()

        for line in lines:
            if not line: continue
            
            is_question = line.startswith("?")
            is_plus_equal = line.startswith("+") or line.startswith("=")
            is_minus = line.startswith("-")
            
            para = ExcelPara(line)
            
            if is_question:
                save_current_question()
                current_q_paras.append(para)
            elif is_plus_equal or is_minus:
                save_current_answer()
                current_ans_is_correct = is_plus_equal
                current_ans_paras.append(para)
            else:
                if current_ans_paras:
                    current_ans_paras.append(para)
                elif current_q_paras:
                    current_q_paras.append(para)
        
        save_current_question()
        return self.blocks, self.errors
