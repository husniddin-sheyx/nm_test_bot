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
        Parses the document into QuestionBlocks.
        Returns (List[QuestionBlock], List[errors])
        """
        current_q_paragraphs = []
        current_answers = []
        
        # Temporary buffer for the current answer being built
        current_ans_paragraphs = []
        current_ans_is_correct = False
        current_ans_marker_found = False

        question_counter = 1

        for para in self.doc.paragraphs:
            text = para.text.strip()
            
            # Check for Answer Markers
            is_plus = text.startswith("+")
            is_equal = text.startswith("=")
            
            if is_plus or is_equal:
                # --- NEW ANSWER START ---
                
                # 1. Save previous answer if exists
                if current_ans_marker_found:
                    # We were already building an answer, finish it
                    current_answers.append(AnswerBlock(
                        original_paragraphs=current_ans_paragraphs,
                        is_correct=current_ans_is_correct,
                        debug_text=current_ans_paragraphs[0].text[:20] if current_ans_paragraphs else ""
                    ))
                    current_ans_paragraphs = []

                # 2. Check if we strictly moved from Question -> Answer
                if not current_answers and current_q_paragraphs:
                    # First answer for this question.
                    # Previous paragraphs were the Question.
                    pass 
                
                # 3. Start new answer
                current_ans_marker_found = True
                current_ans_is_correct = is_plus
                current_ans_paragraphs = [para] # Add this paragraph (it allows us to keep the marker or remove it later)
                
            else:
                # --- NOT A MARKER ---
                
                if current_ans_marker_found:
                    # We are currently inside an answer.
                    # Is this a continuation of the answer (e.g. formula/image/text on next line)?
                    # OR is it a NEW Question?
                    
                    # Heuristic: If it looks like a new question? 
                    # The user said: "1 savol = 1 BLOCK". 
                    # Usually, if we have answers, and then receive non-answer text, it's a New Question.
                    # BUT, multi-line answers are possible.
                    # HOWEVER, standard test formats usually have answers as single blocks.
                    # Let's assume: If we have captured some answers, and we see a paragraph that assumes to be text...
                    # Strict Mode: If it doesn't start with +/=, it's a new question IF we already have answers.
                    
                    # Let's check if the previous paragraph was empty? No.
                    
                    # DECISION: We treat it as a NEW Question ONLY IF we have at least 1 answer already recorded 
                    # AND the previous block was an answer.
                    # Actually, we are building `current_ans_paragraphs`. 
                    # If we hit a non-marked line, strict logic usually assumes it's a new question.
                    # EXCEPTION: If the line is empty?
                    if not text:
                         # Empty line - could be part of anything. Let's append to current context.
                         if current_ans_marker_found:
                             current_ans_paragraphs.append(para)
                         else:
                             current_q_paragraphs.append(para)
                         continue
                    
                    # If not empty and validation says "Valid answers must start with +/-", 
                    # then this is likely a New Question.
                    
                    # 1. Close current answer
                    current_answers.append(AnswerBlock(
                        original_paragraphs=current_ans_paragraphs,
                        is_correct=current_ans_is_correct,
                        debug_text=current_ans_paragraphs[0].text[:20]
                    ))
                    
                    # 2. Save the whole previous Question Block
                    if current_q_paragraphs:
                        q_block = QuestionBlock(
                            id=question_counter,
                            question_paragraphs=current_q_paragraphs,
                            answers=current_answers
                        )
                        self.blocks.append(q_block)
                        question_counter += 1
                    
                    # 3. Reset for new Question
                    current_q_paragraphs = [para]
                    current_answers = []
                    current_ans_paragraphs = []
                    current_ans_marker_found = False
                    current_ans_is_correct = False
                    
                else:
                    # We are NOT in an answer. So we are in a Question.
                    current_q_paragraphs.append(para)

        # End of loop - save the last chunk
        if current_ans_marker_found:
             current_answers.append(AnswerBlock(
                original_paragraphs=current_ans_paragraphs,
                is_correct=current_ans_is_correct,
                debug_text=current_ans_paragraphs[0].text[:20]
            ))
        
        if current_q_paragraphs:
            q_block = QuestionBlock(
                id=question_counter,
                question_paragraphs=current_q_paragraphs,
                answers=current_answers
            )
            self.blocks.append(q_block)
            
        return self.blocks, self.errors
