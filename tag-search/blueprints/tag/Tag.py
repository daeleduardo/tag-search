import re
from ...ext.constants import regex_pattern
class Tag():

    @staticmethod
    def is_invalid_tags(str_tags): 
        if str_tags is None:
            return True

        if  isinstance(str_tags, list):
            for tag in str_tags:
                if re.search(regex_pattern.NON_WORDS, tag.replace(",", "")):
                    return True
        else:
            if re.search(regex_pattern.NON_WORDS, str_tags.replace(",", "")):
                return True
        return False

        
