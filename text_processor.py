import re

class TextProcessor:

    def is_hexadecimal(self,text):
        hex_pattern = r'^[0-9A-Fa-f]+$'
        return bool(re.match(hex_pattern, text))
    
    def hex_to_human_readable(self,hex_message):
        segments        = [hex_message[i:i+4] for i in range(0, len(hex_message), 4)]
        decoded_message = ''.join([chr(int(segment, 16)) for segment in segments])
        return decoded_message

    def is_arabic(self,text):
        for char in text:
            if 0x0600 <= ord(char) <= 0x06FF:
                return True
        return False

    def convert_to_ucs2(self,text):
        ucs2_chars = [format(ord(char), '04X') for char in text]
        ucs2_str = ''.join(ucs2_chars)
        return ucs2_str


# Message Index: 44
# Status: REC READ
# Phone Number Sender: 002B003900360032003700380039003200320031003700360039
# Timestamp: 23/11/09 15:38:40+12
# Message: اللغز الذي نبحث عن مكانه، الحياة ذاك الشيء البعيد الذي نعيش به ولأج


# Message Index: 72
# Status: REC READ
# Phone Number Sender: 002B003900360032003700380039003200320031003700360039
# Timestamp: 23/11/09 15:38:47+12
# Message: له، ولكننا غير مدركين السر الذي سيوصلنا للنجاة، لمعنى أن نصبح أُناس
# ------------------

# Message Index: 73
# Status: REC READ
# Phone Number Sender: 002B003900360032003700380039003200320031003700360039
# Timestamp: 23/11/09 15:38:50+12
# Message: اً قادرين على مواجهتها بقوة وحزم أشد واقوى