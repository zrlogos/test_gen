import pytest
from typing import List, Optional
import os
from pathlib import Path


class TestRunner:
    """测试运行器，用于执行pytest测试并生成报告"""

    def __init__(
            self,
            source: str,
            test_dir: str = "tests",
            report_dir: str = "test_reports"
    ):
        """初始化测试运行器

        Args:
            source: 要统计覆盖率的源代码文件或目录路径
            test_dir: 测试文件目录
            report_dir: 测试报告输出目录
        """
        self.project_root = Path(os.getcwd()).absolute()
        self.source = (self.project_root / source).absolute()
        self.test_dir = (self.project_root / test_dir).absolute()
        self.report_dir = (self.project_root / report_dir).absolute()

        # 确保报告目录存在
        self.report_dir.mkdir(parents=True, exist_ok=True)

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
        pytest_args = ["-v"]

        # 配置HTML测试报告
        if html_report:
            html_path = self.report_dir / "test_report.html"
            pytest_args.extend([
                f"--html={html_path}",
                "--self-contained-html"
            ])

        # 配置覆盖率报告
        if coverage:
            coverage_dir = self.report_dir / "coverage"
            source_path = self.source.relative_to(self.project_root)
            pytest_args.extend([
                f"--cov={source_path}",
                "--cov-report=term-missing",  # 终端输出
                f"--cov-report=html:{coverage_dir}",  # HTML报告
                "--cov-report=xml:{coverage_dir}/coverage.xml",  # XML报告（可选）
            ])

        # 添加测试路径
        if test_paths:
            pytest_args.extend(test_paths)
        else:
            pytest_args.append(str(self.test_dir))

        print(f"Running tests with args: {pytest_args}")
        return pytest.main(pytest_args)


# 使用示例
if __name__ == "__main__":
    runner = TestRunner(
        source="codes",
        test_dir="tests",
        report_dir="test_reports"
    )

    exit_code = runner.run_tests()

    # 打印报告位置
    print(f"\n测试完成，退出码: {exit_code}")
    print(f"测试报告位置: {runner.report_dir}/test_report.html")
    print(f"覆盖率报告位置: {runner.report_dir}/coverage/index.html")
