import re

class SpecialCharacterRemover:
    def __init__(self):
        self.special_char_pattern = re.compile(r'[^ a-zA-Z0-9\n\t.,;:!?()\'[\\]"<>]+')
        self.special_char_pattern1 = re.compile(r'\t')

    def remove_special_chars(self, text):
        # Remove special characters while preserving HTML tags
        cleaned_text = self.special_char_pattern.sub('', text)
        cleaned_text = self.special_char_pattern1.sub('    ', text)
        return cleaned_text
    
    def extract_text(self, input_string, start_delimiter="response\":"):
        try:
            start = input_string.index(start_delimiter)
            return input_string[start:]
        except ValueError:
            return ""  # or handle the error as needed