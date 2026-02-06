import random
from typing import List
from bot.structure import QuestionBlock
from bot.utils.lexicon import BUTTONS

class Processor:
    def __init__(self, blocks: List[QuestionBlock]):
        self.blocks = blocks

    def process(self, action: str) -> List[QuestionBlock]:
        """
        Processes the blocks based on the action (Shuffle or Extract).
        Returns the modified list of blocks.
        """
        if action == BUTTONS["user"]["shuffle"]:
            return self._shuffle(shuffle_questions=True)
        elif action == BUTTONS["user"]["shuffle_answers"]:
            return self._shuffle(shuffle_questions=False)
        elif action == BUTTONS["user"]["extract"]:
            return self._extract_correct()
        return self.blocks

    def _shuffle(self, shuffle_questions: bool = True) -> List[QuestionBlock]:
        """
        1. Shuffle questions order (Optional).
        2. Shuffle answers within each question.
        """
        if shuffle_questions:
            shuffled_questions = self.blocks.copy()
            random.shuffle(shuffled_questions)
        else:
            # Keep original question order
            shuffled_questions = self.blocks.copy()
        
        for q in shuffled_questions:
            # Create a copy of answers to shuffle
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
            correct_answers = [a for a in q.answers if a.is_correct]
            if correct_answers:
                # We modify the block to only have correct answers
                q.answers = correct_answers
                processed_questions.append(q)
        return processed_questions
