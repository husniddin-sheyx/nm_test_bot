from typing import List, Tuple
from bot.structure import QuestionBlock
from bot.utils.lexicon import ERROR_TEXTS

class Validator:
    def validate(self, blocks: List[QuestionBlock]) -> Tuple[List[QuestionBlock], List[Tuple[QuestionBlock, List[str]]]]:
        """
        Validates a list of QuestionBlocks.
        Returns (valid_blocks, invalid_blocks_with_errors)
        """
        valid_blocks = []
        invalid_with_errors = [] # List[Tuple[QuestionBlock, List[str]]]
        
        if not blocks:
            return [], []

        # To track duplicate questions
        question_texts = {} # text -> first_id
        
        for q in blocks:
            q_errors = []
            
            # --- 1. Basic Structure Validation ---
            # Answer Count Check
            if len(q.answers) < 2:
                q_errors.append(ERROR_TEXTS["few_answers"].format(id=q.id))
            
            # Correct Answer Check (+)
            correct_count = sum(1 for a in q.answers if a.is_correct)
            
            if correct_count == 0:
                q_errors.append(ERROR_TEXTS["missing_plus"].format(id=q.id))
            elif correct_count > 1:
                q_errors.append(ERROR_TEXTS["multiple_plus"].format(id=q.id, count=correct_count))
            
            # --- 2. Duplicate Detection ---
            
            # 2.1 Duplicate Question Check
            q_text = "".join(p.text for p in q.question_paragraphs).strip()
            if q_text.startswith("?"):
                q_text = q_text[1:].strip()
                
            if q_text:
                if q_text in question_texts:
                    q_errors.append(ERROR_TEXTS["duplicate_question"].format(
                        id=q.id, 
                        first_id=question_texts[q_text]
                    ))
                else:
                    question_texts[q_text] = q.id

            # 2.2 Duplicate Answer Check (within this question)
            seen_answers = set()
            duplicates_in_q = set()
            
            for ans in q.answers:
                ans_text = "".join(p.text for p in ans.original_paragraphs).strip()
                # Remove markers from start for comparison
                if ans_text.startswith("+") or ans_text.startswith("=") or ans_text.startswith("-"):
                    ans_text = ans_text[1:].strip()
                
                if ans_text in seen_answers:
                    duplicates_in_q.add(f"`{ans_text[:30]}...`" if len(ans_text) > 30 else f"`{ans_text}`")
                else:
                    seen_answers.add(ans_text)
            
            if duplicates_in_q:
                q_errors.append(ERROR_TEXTS["duplicate_answer"].format(
                    id=q.id,
                    dupes=", ".join(duplicates_in_q)
                ))

            # --- 3. Final Categorization ---
            if q_errors:
                invalid_with_errors.append((q, q_errors))
            else:
                valid_blocks.append(q)

        return valid_blocks, invalid_with_errors
