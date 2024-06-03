from errors import PreprocessorError
from linked_list import LinkedList
from utils import WHITE, read_file
from expressions import Program
from state import State
import parser
from logger import INFO, DEBU

class Tag:
    IMPORT = "import"
    EXPORT = "export"
    ALIAS = "alias"
    RUN = "run"


TAGS  = [getattr(Tag, attr) for attr in dir(Tag) if not callable(getattr(Tag, attr)) and not attr.startswith("__")]

class Preprocessor:
    COMMENT_INDICATOR = '#'
    MULTILINE_COMMENT_START = '-#'
    MULTILINE_COMMENT_END = '#-'
    TAG_INDICATOR = '@'

    def __init__(self, file):
        self.file = file
        self.state = State(self.file, read_file(file))
        self.scopes: list[LinkedList] = []
    
    def run_import(self):
        while WHITE.__contains__(parser.inspect(self.state)): parser.advance(self.state)

        end = self.state.source.find('\n', self.state.position)
        file = self.state.source[self.state.position:] if end == -1 else self.state.source[self.state.position:end]

        INFO(f"Importing file: ./{file}.kd")

        preprocessor = Preprocessor(f"{file}.kd")
        preprocessor.run()
        
        state = State(file, preprocessor.state.source)
        try:
            Program(state, [False])
        except KeyboardInterrupt:
            exit(1)
        
        self.scopes.append(state.scope.scopes)

    def Tag(self):
        if(parser.take_string(self.state, f"{Tag.IMPORT}")): self.run_import()
        else: PreprocessorError(self.state, "Unkown preprocessor tag").throw()

    def remove_line_starting_with(self, char):
        in_string = False
        result = []

        for line in self.state.source.split('\n'):
            new_line = ''
            i = 0
            while i < len(line):
                if line[i] == '"' and (i == 0 or line[i - 1] != '\\'):
                    in_string = not in_string
                
                if not in_string and line[i] == char:
                    break
                else:
                    new_line += line[i]
                i += 1 

            result.append(new_line) 

        self.state.source = '\n'.join(result)

    def remove_comments(self):
        self.remove_line_starting_with(Preprocessor.COMMENT_INDICATOR)

    def remove_tags(self):
        self.remove_line_starting_with(Preprocessor.TAG_INDICATOR)

    def remove_empty_lines(self):
        lines = self.source.split('\n')
        
        non_empty_lines = [line for line in lines if line.strip()]
        
        self.source = '\n'.join(non_empty_lines)

    def run(self):
        self.remove_comments()
        while parser.next(self.state) != '\0':
            if parser.inspect(self.state) == Preprocessor.TAG_INDICATOR:
                parser.advance(self.state)
                self.Tag()
            parser.advance(self.state)
        self.remove_tags()



