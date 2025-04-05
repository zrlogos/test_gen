class CodeReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_code(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()
        

if __name__ == "__main__":
    code_reader = CodeReader("")
    code = code_reader.read_code()
    print(code)


