import re
from utils import read_file

class Preprocessor:
    def __init__(self, file):
        self.file = file
        self.source = read_file(file)

    def remove_comments(self):
        string_pattern = re.compile(r'(["\'])(?:(?=(\\?))\2.)*?\1')
        comment_pattern = re.compile(r'#.*')

        def remove_comment_from_line(line):
            matches = list(string_pattern.finditer(line))
            
            result = []
            last_end = 0

            for match in matches:
                result.append(re.sub(comment_pattern, '', line[last_end:match.start()]))
                result.append(match.group(0))
                last_end = match.end()

            result.append(re.sub(comment_pattern, '', line[last_end:]))

            return ''.join(result)

        processed_lines = []
        for line in self.source.split('\n'):
            processed_line = remove_comment_from_line(line)
            processed_lines.append(processed_line)

        self.source = '\n'.join(processed_lines)

    def remove_empty_lines(self):
        lines = self.source.split('\n')
        
        non_empty_lines = [line for line in lines if line.strip()]
        
        self.source = '\n'.join(non_empty_lines)

    def run(self):
        self.remove_comments()
        # self.remove_empty_lines()


