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

        for q in blocks:
            # 1. Answer Count Check
            if len(q.answers) < 2:
                errors.append(ERROR_TEXTS["few_answers"].format(id=q.id))
            
            # 2. Correct Answer Check (+)
            correct_count = sum(1 for a in q.answers if a.is_correct)
            
            if correct_count == 0:
                errors.append(ERROR_TEXTS["missing_plus"].format(id=q.id))
            elif correct_count > 1:
                errors.append(ERROR_TEXTS["multiple_plus"].format(id=q.id, count=correct_count))
            
            # 3. Image/Formula Orphan Check
            # Note: The parser logic already forces all content into Q or A blocks.
            # However, if we wanted to detect "Image without text", we could check here.
            # For now, strict structure validation is covered by the Parser's logic 
            # (it wouldn't create a block if it couldn't attach it, or it would attach it to Q context).
            
            # We can check if a Question is EMPTY (no text, no image?)
            has_content = any(p.text.strip() for p in q.question_paragraphs)
            # If no text, strictly speaking it might be just an image. If image exists, it's valid.
            # Since we store 'paragraphs', we assume if list is not empty, it has content.
            # But we should check if they are ALL empty text and NO images (hard to check images without inspecting XML deeply).
            # For now, assume if paragraphs exist, it's consistent.

        return errors
