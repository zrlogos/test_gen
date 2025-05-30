import pytest
import subprocess
import shutil
from typing import List, Optional
import os
from pathlib import Path
import json


class TestRunner:
    """测试运行器，用于执行pytest测试并生成Allure报告"""

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
            allure_report: bool = True,
            coverage: bool = True,
            serve_report: bool = False
    ) -> int:
        """运行测试用例

        Args:
            test_paths: 指定要运行的测试文件或目录列表，为None时运行test_dir下所有测试
            allure_report: 是否生成Allure格式的测试报告
            coverage: 是否生成覆盖率报告
            serve_report: 是否在测试完成后直接启动Allure服务器展示报告

        Returns:
            int: pytest.main()的返回码，0表示成功
        """
        pytest_args = ["-v"]

        # 配置Allure测试报告
        allure_results_dir = None
        coverage_dir = None
        
        if allure_report:
            allure_results_dir = self.report_dir / "allure-results"
            allure_results_dir.mkdir(exist_ok=True)
            pytest_args.extend([
                f"--alluredir={allure_results_dir}"
            ])

        # 配置覆盖率报告
        if coverage:
            coverage_dir = self.report_dir / "coverage"
            source_path = self.source.relative_to(self.project_root)
            pytest_args.extend([
                f"--cov={source_path}",
                "--cov-branch",  # ✅ 启用分支覆盖率统计
                "--cov-report=term-missing",  # 终端输出缺失分支信息
                f"--cov-report=html:{coverage_dir}",  # 生成 HTML 报告
                f"--cov-report=xml:{coverage_dir}/coverage.xml",  # 生成 XML 报告
            ])


        # 添加测试路径
        if test_paths:
            pytest_args.extend(test_paths)
        else:
            pytest_args.append(str(self.test_dir))

        print(f"运行测试，参数: {pytest_args}")
        exit_code = pytest.main(pytest_args)
        
        # 处理Allure报告
        if allure_report and allure_results_dir:
            if coverage and coverage_dir and coverage_dir.exists():
                # 将覆盖率报告添加到Allure结果中
                self._add_coverage_to_allure(allure_results_dir, coverage_dir)

            if serve_report:
                # 直接启动Allure服务器展示报告
                self.serve_allure_report(allure_results_dir)
            else:
                # 生成静态HTML报告
                self._generate_allure_html(allure_results_dir)
            
        return exit_code

    def _add_coverage_to_allure(self, allure_results_dir: Path, coverage_dir: Path) -> None:
        """将覆盖率报告添加到Allure结果中

        Args:
            allure_results_dir: Allure结果目录路径
            coverage_dir: 覆盖率报告目录路径
        """
        try:
            # 创建环境属性文件，添加覆盖率信息
            try:
                # 从 coverage.xml 文件提取覆盖率信息
                xml_path = coverage_dir / "coverage.xml"
                if xml_path.exists():
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(xml_path)
                    root = tree.getroot()

                    # 提取语句覆盖率信息
                    coverage_percentage = float(root.attrib.get('line-rate', 0.0)) * 100
                    total_lines = int(root.attrib.get('lines-valid', 0))
                    covered_lines = int(root.attrib.get('lines-covered', 0))

                    # 提取分支覆盖率信息
                    total_branches = int(root.attrib.get('branches-valid', 0))
                    covered_branches = int(root.attrib.get('branches-covered', 0))

                    branch_coverage_percentage = 0.0
                    if total_branches > 0:
                        branch_coverage_percentage = (covered_branches / total_branches) * 100

                    # 创建环境属性文件
                    with open(allure_results_dir / "environment.properties", 'w') as f:
                        f.write(f"Coverage={coverage_percentage:.2f}%\n")
                        f.write(f"Total_Lines={total_lines}\n")
                        f.write(f"Covered_Lines={covered_lines}\n")
                        f.write(f"Branch_Coverage={branch_coverage_percentage:.2f}%\n")
                        f.write(f"Total_Branches={total_branches}\n")
                        f.write(f"Covered_Branches={covered_branches}\n")

                    print(f"✅ 已添加语句覆盖率到 Allure：{coverage_percentage:.2f}%")
                    print(f"✅ 已添加分支覆盖率到 Allure：{branch_coverage_percentage:.2f}%")

            except Exception as e:
                print(f"❌ 处理覆盖率 XML 文件时出错: {e}")

            # 复制覆盖率HTML报告到Allure结果目录
            if coverage_dir.exists() and coverage_dir.is_dir():
                try:
                    # 创建包含HTML报告链接的附件
                    with open(allure_results_dir / "coverage-report.html", 'w') as f:
                        f.write("""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>覆盖率报告</title>
                            <style>
                                body { font-family: Arial, sans-serif; margin: 20px; }
                                .link { padding: 10px; background: #f0f0f0; display: inline-block; }
                            </style>
                        </head>
                        <body>
                            <h2>测试覆盖率报告</h2>
                            <div class="link">
                                <a href="../coverage/index.html" target="_blank">查看完整覆盖率报告</a>
                            </div>
                        </body>
                        </html>
                        """)

                    # 添加环境摘要信息
                    with open(allure_results_dir / "coverage-attachment.json", 'w') as f:
                        json.dump({
                            "name": "覆盖率报告",
                            "source": str(allure_results_dir / "coverage-report.html"),
                            "type": "text/html",
                            "size": 0
                        }, f)

                    print("已添加覆盖率HTML报告链接到Allure结果")
                except Exception as e:
                    print(f"添加覆盖率报告链接时出错: {e}")
        except Exception as e:
            print(f"添加覆盖率报告到Allure结果时出错: {e}")

    def _generate_allure_html(self, allure_results_dir: Path) -> None:
        """生成Allure静态HTML报告

        Args:
            allure_results_dir: Allure结果目录路径
        """
        allure_report_dir = self.report_dir / "allure-report"
        try:
            print(f"正在生成Allure静态HTML报告...")
            subprocess.run(
                [
                    "allure", "generate", 
                    str(allure_results_dir), 
                    "-o", str(allure_report_dir), 
                    "--clean"
                ],
                check=True
            )
            print(f"Allure报告已生成: {allure_report_dir}")
        except subprocess.CalledProcessError as e:
            print(f"生成Allure报告失败: {e}")
        except FileNotFoundError:
            print("未找到allure命令，请确保已安装Allure命令行工具")
    
    def serve_allure_report(self, allure_results_dir: Path) -> None:
        """启动Allure服务器展示报告

        启动一个Web服务器，实时展示Allure报告。
        此方法会阻塞当前进程，直到用户手动终止（通常使用Ctrl+C）。

        Args:
            allure_results_dir: Allure结果目录路径
        """
        try:
            print(f"正在启动Allure服务器，将自动打开浏览器展示报告...")
            print(f"按Ctrl+C终止服务器")
            
            # 运行allure serve命令
            subprocess.run(
                ["allure", "serve", str(allure_results_dir)],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"启动Allure服务器失败: {e}")
        except FileNotFoundError:
            print("未找到allure命令，请确保已安装Allure命令行工具")
        except KeyboardInterrupt:
            print("\nAllure服务器已终止")


# 使用示例
if __name__ == "__main__":
    runner = TestRunner(
        source="codes",
        test_dir="../tests",
        report_dir="test_reports"
    )

    # 运行测试并生成静态HTML报告（默认）
    # exit_code = runner.run_tests()
    
    # 或者运行测试并启动Allure服务器
    exit_code = runner.run_tests(serve_report=True)

    # 打印报告位置
    print(f"\n测试完成，退出码: {exit_code}")
    if not runner.run_tests.__defaults__[3]:  # 检查serve_report的默认值
        print(f"Allure报告位置: {runner.report_dir}/allure-report/index.html")
    print(f"覆盖率报告位置: {runner.report_dir}/coverage/index.html")
