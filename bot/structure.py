from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class AnswerBlock:
    """
    Represents a single answer option.
    """
    original_paragraphs: List[Any]  # List of python-docx Paragraph objects (or their internal elements)
    is_correct: bool = False
    debug_text: str = ""  # For logging/debugging (first few words)

@dataclass
class QuestionBlock:
    """
    Represents a full question unit (Question + Answers).
    """
    id: int  # Sequential ID 1, 2, 3...
    question_paragraphs: List[Any]  # The question text/images
    answers: List[AnswerBlock] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        # Basic logical validation
        correct_count = sum(1 for a in self.answers if a.is_correct)
        return correct_count == 1 and len(self.answers) >= 2
