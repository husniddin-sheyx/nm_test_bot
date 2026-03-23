import random
from typing import List
from bot.structure import QuestionBlock

class Processor:
    def __init__(self, blocks: List[QuestionBlock]):
        self.blocks = blocks

    def process(self, action: str) -> List[QuestionBlock]:
        """
        Processes the blocks based on standardized action keys:
        'shuffle', 'shuffle_answers', 'extract'
        """
        if action == "shuffle":
            return self._shuffle(shuffle_questions=True)
        elif action == "shuffle_answers":
            return self._shuffle(shuffle_questions=False)
        elif action == "extract":
            return self._extract_correct()
        return self.blocks

    def _shuffle(self, shuffle_questions: bool = True) -> List[QuestionBlock]:
        """
        1. Shuffle questions order (Optional).
        2. Shuffle answers within each question.
        """
        shuffled_questions = self.blocks.copy()
        if shuffle_questions:
            random.shuffle(shuffled_questions)
        
        for q in shuffled_questions:
            shuffled_answers = q.answers.copy()
            random.shuffle(shuffled_answers)
            q.answers = shuffled_answers
            
        return shuffled_questions

    def _extract_correct(self) -> List[QuestionBlock]:
        """
        For each question, keep ONLY the correct answer(s).
        """
        processed_questions = []
        for q in self.blocks:
            # We look for a.is_correct which is set by the parser
            correct_answers = [a for a in q.answers if a.is_correct]
            if correct_answers:
                q.answers = correct_answers
                processed_questions.append(q)
        return processed_questions
