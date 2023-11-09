class TextProcessor:
    # def __init__(self):
    #     pass

    def is_arabic(self,text):
        for char in text:
            if 0x0600 <= ord(char) <= 0x06FF:
                return True
        return False

    def is_english(self,text):
        for char in text:
            if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                return True
        return False


    def convert_to_ucs2(self,text):
        ucs2_chars = [format(ord(char), '04X') for char in text]
        ucs2_str = ''.join(ucs2_chars)
        return ucs2_str

