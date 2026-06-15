from difflib import SequenceMatcher
import re

class Match:
        def __init__(self):
                return

        def fuzzy_match_ratio(self, str1, str2):
                return SequenceMatcher(None, str1, str2).ratio()


        def fuzzy_best_match(self, str, arr):
                max_score = 0
                for elem in arr:
                        max_score = max(self.fuzzy_match_ratio(str, elem), max_score)
                return max_score
        
        def match_units(self, str, unit_str):
                pattern = r"(\d+\.?\d*)\s*(kg|cm|mL)"
                first_match = re.search(pattern, str)
                if first_match:
                        return True if self.fuzzy_match_ratio(first_match, unit_str) >= 0.9 else False



