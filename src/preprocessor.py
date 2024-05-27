from utils import read_file

class Preprocessor:
    COMMENT = '#'
    MULTILINE_COMMENT_START = '-#'
    MULTILINE_COMMENT_END = '#-'
    TAG_INDICATOR = '!'

    def __init__(self, file):
        self.file = file
        self.source = read_file(file) 

    def remove_comments(self):
        in_string = False
        result = []

        for line in self.source.split('\n'):
            new_line = ''
            i = 0
            while i < len(line):
                if line[i] == '"' and (i == 0 or line[i - 1] != '\\'):
                    in_string = not in_string
                
                if not in_string and line[i] == Preprocessor.COMMENT:
                    break
                else:
                    new_line += line[i]
                i += 1 

            result.append(new_line) 

        self.source = '\n'.join(result)

    def remove_empty_lines(self):
        lines = self.source.split('\n')
        
        non_empty_lines = [line for line in lines if line.strip()]
        
        self.source = '\n'.join(non_empty_lines)

    def run(self):
        self.remove_comments()


