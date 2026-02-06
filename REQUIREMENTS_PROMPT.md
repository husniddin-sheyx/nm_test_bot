# Test Bot Requirements & Prompt

## 🖼️ IMAGE HANDLING REQUIREMENTS (VERY IMPORTANT)

When shuffling questions and answers:

* Images MUST be treated as **part of the block**, not as standalone elements
* An image that belongs to a **question** must always remain with that question
* An image that belongs to an **answer option** must remain with that exact answer
* Images must NOT:

  * move to another question
  * detach from their original text
  * be reordered independently

### Shuffling Rules for Images

* Shuffle ONLY at the **question block level**
* Shuffle ONLY at the **answer block level**
* A block may contain:

  * text
  * formulas
  * images
* The internal structure of a block MUST NOT be modified

### Validation Rules for Images

Detect and report errors if:

* An image exists without an associated question
* An image is detected between questions without context
* An answer contains only an image without a `+` or `=` marker

Example error message:

> ❗ Question 6: image detected but not attached to any answer or question text

---

## 🔒 DATA INTEGRITY GUARANTEE

The bot must guarantee that:

* No image is lost after processing
* No image is duplicated
* No image changes its semantic meaning
* The shuffled DOCX visually matches the original structure, only reordered

---

## 🧠 IMPLEMENTATION NOTE (for AI)

* Use DOCX relationships to track images
* Bind images to their parent paragraph/run
* Reinsert images during export using the same relationship mapping
