from typing import Optional, Dict
from code_reader import CodeReader
from code_writer import CodeWriter
from llm_client import LLMChat
import re


class TestGenerator:
    """测试代码生成器"""

    def __init__(
            self,
            model: str = "deepseek-chat",
            system_prompt: str = "你是一个专业的测试开发工程师，擅长编写单元测试。"
    ):
        """初始化测试生成器
        
        Args:
            model: 使用的模型名称
            system_prompt: 系统提示词
        """
        self.llm = LLMChat(
            model=model,
            system_prompt=system_prompt
        )

        self.test_template = """
                请为以下Python代码生成单元测试：
                要求：
                1. 使用pytest框架
                2. 包含多个测试用例，覆盖主要功能点
                3. 包含正常场景和异常场景测试
                4. 使用pytest fixture处理测试依赖
                5. 添加适当的测试注释
                6. 确保测试代码规范且易于维护
                
                请直接返回完整的测试代码，不需要解释。测试文件名应为 test_{original_name}
                """

    def generate_test(
            self,
            source_file: str,
            output_dir: Optional[str] = None,
            custom_template: Optional[str] = None
    ) -> bool:
        """生成测试代码
        
        Args:
            source_file: 源代码文件路径
            output_dir: 输出目录，默认与源文件同目录
            custom_template: 自定义提示模板
            
        Returns:
            bool: 是否成功生成测试代码
        """
        try:
            # 读取源代码
            reader = CodeReader(source_file)
            code = reader.read_code()

            # 准备输出路径
            import os
            source_name = os.path.basename(source_file)
            source_name_without_ext = os.path.splitext(source_name)[0]
            test_file_name = f"test_{source_name_without_ext}.py"

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, test_file_name)
            else:
                output_path = os.path.join(os.path.dirname(source_file), test_file_name)

            # 生成测试代码
            template = custom_template or self.test_template
            prompt = template.format(
                code=code,
                original_name=source_name_without_ext
            )

            response = self.llm.chat(
                prompt,
                temperature=0.7,
                max_tokens=8192
            )

            # 提取代码块内容
            test_code = self.extract_code_blocks(response)

            # 写入测试文件
            writer = CodeWriter(output_path)
            success = writer.write_code(test_code)

            if success:
                print(f"测试代码已生成: {output_path}")
            return success

        except Exception as e:
            print(f"生成测试代码时出错: {str(e)}")
            return False

    def extract_code_blocks(self, markdown_text: str) -> str:
        """
        从 Markdown 文本中提取代码块。

        Args:
            markdown_text: 包含 Markdown 格式文本的字符串。

        Returns:
            str: 提取的第一个代码块的内容。如果没有找到代码块，返回空字符串。
        """
        # 匹配以 ``` 开头，可选语言标识符，然后是代码，最后以 ``` 结尾的代码块
        pattern = re.compile(r"```([a-zA-Z]*)?\n(.*?)\n```", re.DOTALL)
        matches = pattern.findall(markdown_text)

        if matches:
            # 返回第一个代码块的内容
            return matches[0][1].strip()
        return ""


# 使用示例
if __name__ == "__main__":
    # 创建测试生成器
    generator = TestGenerator()

    # 为单个文件生成测试
    generator.generate_test(
        "code_writer.py",
        output_dir="tests"
    )
