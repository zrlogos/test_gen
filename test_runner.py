import pytest
from typing import List, Optional
import os

class TestRunner:
    """测试运行器，用于执行pytest测试并生成报告"""
    
    def __init__(
        self,
        test_dir: str = "tests",
        report_dir: str = "test_reports"
    ):
        """初始化测试运行器
        
        Args:
            test_dir: 测试文件目录
            report_dir: 测试报告输出目录
        """
        self.test_dir = test_dir
        self.report_dir = report_dir
        
    def run_tests(
        self,
        test_paths: Optional[List[str]] = None,
        html_report: bool = True,
        coverage: bool = True
    ) -> int:
        """运行测试用例
        
        Args:
            test_paths: 指定要运行的测试文件或目录列表，为None时运行test_dir下所有测试
            html_report: 是否生成HTML格式的测试报告
            coverage: 是否生成覆盖率报告
            
        Returns:
            int: pytest.main()的返回码，0表示成功
        """
        # 准备pytest参数
        pytest_args = [
            "-v",  # 详细输出
            "--tb=short",  # 简化的traceback格式
        ]
        
        # 配置HTML报告
        if html_report:
            os.makedirs(self.report_dir, exist_ok=True)
            html_path = os.path.join(self.report_dir, "test_report.html")
            pytest_args.extend([
                "--html=" + html_path,
                "--self-contained-html"
            ])
            
        # 配置覆盖率报告
        if coverage:
            pytest_args.extend([
                "--cov=.",  # 覆盖率统计范围
                "--cov-report=term-missing",  # 终端输出未覆盖行
                f"--cov-report=html:{os.path.join(self.report_dir, 'coverage')}"  # HTML覆盖率报告
            ])
            
        # 添加测试路径
        if test_paths:
            pytest_args.extend(test_paths)
        else:
            pytest_args.append(self.test_dir)
            
        # 运行测试
        return pytest.main(pytest_args)
        
    def get_last_report_path(self) -> str:
        """获取最新生成的HTML报告路径"""
        return os.path.join(self.report_dir, "test_report.html")
        
    def get_last_coverage_path(self) -> str:
        """获取最新生成的覆盖率报告路径"""
        return os.path.join(self.report_dir, "coverage", "index.html")


# 使用示例
if __name__ == "__main__":
    runner = TestRunner()
    
    # 运行所有测试
    exit_code = runner.run_tests()
    print(f"测试完成，退出码: {exit_code}")
    print(f"测试报告路径: {runner.get_last_report_path()}")
    print(f"覆盖率报告路径: {runner.get_last_coverage_path()}")
    
    # 运行指定测试文件
    # runner.run_tests(["tests/test_code_writer.py"])