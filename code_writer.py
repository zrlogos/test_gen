from typing import Optional
import os

class CodeWriter:
    """代码写入工具类"""
    
    def __init__(self, file_path: str):
        """初始化代码写入器
        
        Args:
            file_path: 目标文件路径
        """
        self.file_path = file_path
        
    def write_code(self, code: str, mode: str = 'w', encoding: str = 'utf-8') -> bool:
        """将代码写入文件
        
        Args:
            code: 要写入的代码内容
            mode: 写入模式 ('w'覆盖, 'a'追加)
            encoding: 文件编码
            
        Returns:
            bool: 写入是否成功
        """
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
            
            # 写入文件
            with open(self.file_path, mode, encoding=encoding) as f:
                f.write(code)
            return True
            
        except Exception as e:
            print(f"写入文件时出错: {str(e)}")
            return False
    
    def append_code(self, code: str, encoding: str = 'utf-8') -> bool:
        """追加代码到文件末尾
        
        Args:
            code: 要追加的代码内容
            encoding: 文件编码
            
        Returns:
            bool: 追加是否成功
        """
        return self.write_code(code, mode='a', encoding=encoding)

# 使用示例
if __name__ == "__main__":
    # 创建写入器实例
    writer = CodeWriter("test_output.py")
    
    # 写入新代码
    code = """
def hello_world():
    print("Hello, World!")
    
if __name__ == "__main__":
    hello_world()
"""
    if writer.write_code(code):
        print("代码写入成功!")
    
    # 追加代码
    additional_code = """
# 添加新的函数
def greet(name):
    print(f"Hello, {name}!")
"""
    if writer.append_code(additional_code):
        print("代码追加成功!") 