from typing import List
from bot.structure import QuestionBlock
from bot.utils.lexicon import ERROR_TEXTS

class Validator:
    def validate(self, blocks: List[QuestionBlock]) -> List[str]:
        """
        Validates a list of QuestionBlocks.
        Returns a list of error messages (empty if valid).
        """
        errors = []
        
        if not blocks:
            errors.append(ERROR_TEXTS["no_questions"])
            return errors

        # To track duplicate questions
        question_texts = {} # text -> first_id
        
        for q in blocks:
            # --- 1. Basic Structure Validation ---
            # Answer Count Check
            if len(q.answers) < 2:
                errors.append(ERROR_TEXTS["few_answers"].format(id=q.id))
            
            # Correct Answer Check (+)
            correct_count = sum(1 for a in q.answers if a.is_correct)
            
            if correct_count == 0:
                errors.append(ERROR_TEXTS["missing_plus"].format(id=q.id))
            elif correct_count > 1:
                errors.append(ERROR_TEXTS["multiple_plus"].format(id=q.id, count=correct_count))
            
            # --- 2. Duplicate Detection (New Features) ---
            
            # 2.1 Duplicate Question Check
            q_text = "".join(p.text for p in q.question_paragraphs).strip()
            if q_text.startswith("?"):
                q_text = q_text[1:].strip()
                
            if q_text:
                if q_text in question_texts:
                    errors.append(ERROR_TEXTS["duplicate_question"].format(
                        id=q.id, 
                        first_id=question_texts[q_text]
                    ))
                else:
                    question_texts[q_text] = q.id

            # 2.2 Duplicate Answer Check (within this question)
            answer_texts = []
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
                errors.append(ERROR_TEXTS["duplicate_answer"].format(
                    id=q.id,
                    dupes=", ".join(duplicates_in_q)
                ))

        return errors
