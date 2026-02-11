from docx import Document
from bot.structure import QuestionBlock, AnswerBlock
from typing import List, Tuple

class DocxParser:
    def __init__(self, file_path: str):
        self.doc = Document(file_path)
        self.blocks: List[QuestionBlock] = []
        self.errors: List[str] = []

    def parse(self) -> Tuple[List[QuestionBlock], List[str]]:
        """
        Parses the document into QuestionBlocks using markers:
        ? - Question start
        + - Correct answer
        - or = - Incorrect answer
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
            is_plus = text.startswith("+")
            is_minus_equal = text.startswith("-") or text.startswith("=")
            
            if is_question:
                save_current_question()
                current_q_paragraphs.append(para)
            elif is_plus or is_minus_equal:
                save_current_answer()
                current_ans_is_correct = is_plus
                current_ans_paragraphs.append(para)
            else:
                # Continuation of current block
                if current_ans_paragraphs:
                    current_ans_paragraphs.append(para)
                elif current_q_paragraphs:
                    current_q_paragraphs.append(para)
                # If neither (e.g. text before first question), ignore or treat as question part?
                # User documents usually start with a question or title.
                # Let's ignore text until the first '?' to be safe, or treat as part of Q1 if it exists.
        
        # Save last block
        save_current_question()
            
        return self.blocks, self.errors
