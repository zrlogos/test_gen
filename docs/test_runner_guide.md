# TestRunner 使用指南

## 简介

`TestRunner` 是一个用于运行测试并生成各种报告的工具，包括 HTML 报告、覆盖率报告和 Allure 报告。

## 安装依赖

首先，确保安装了所需的依赖：

```bash
pip install pytest pytest-html pytest-cov allure-pytest
```

如果要使用 Allure 报告，还需要安装 Allure 命令行工具：

- **macOS**:
  ```bash
  brew install allure
  ```

- **Windows**:
  ```bash
  scoop install allure
  ```

- **Linux**:
  ```bash
  sudo apt-add-repository ppa:qameta/allure
  sudo apt-get update
  sudo apt-get install allure
  ```

## 基本用法

### 命令行参数

`test_runner.py` 支持以下命令行参数：

- `--source`: 要统计覆盖率的源代码文件或目录路径（默认: "codes"）
- `--test-dir`: 测试文件目录（默认: "tests"）
- `--report-dir`: 测试报告输出目录（默认: "test_reports"）
- `--no-html`: 不生成 HTML 报告
- `--no-coverage`: 不生成覆盖率报告
- `--allure`: 生成 Allure 报告
- `--serve-allure`: 生成并打开 Allure 报告
- `--test-path`: 指定要运行的测试文件或目录，可多次指定

### 示例

1. **运行所有测试并生成所有报告**:
   ```bash
   python test_runner.py --allure
   ```

2. **运行特定测试文件**:
   ```bash
   python test_runner.py --test-path tests/test_example.py
   ```

3. **生成 Allure 报告并打开**:
   ```bash
   python test_runner.py --serve-allure
   ```

4. **只生成 HTML 报告，不生成覆盖率报告**:
   ```bash
   python test_runner.py --no-coverage
   ```

5. **自定义源代码和测试目录**:
   ```bash
   python test_runner.py --source src --test-dir test
   ```

## 在代码中使用

你也可以在代码中使用 `TestRunner` 类：

```python
from test_runner import TestRunner

# 创建 TestRunner 实例
runner = TestRunner(
    source="src",
    test_dir="tests",
    report_dir="reports"
)

# 运行测试
exit_code = runner.run_tests(
    html_report=True,
    coverage=True,
    allure_report=True
)

# 启动 Allure 报告服务器
runner.serve_allure_report()
```

## 报告位置

- **HTML 报告**: `{report_dir}/test_report.html`
- **覆盖率报告**: `{report_dir}/coverage/index.html`
- **Allure 报告**: `{report_dir}/allure-report/index.html`
- **Allure 结果目录**: `{report_dir}/allure-results`

## 查看 Allure 报告

有两种方式查看 Allure 报告：

1. **使用 `--serve-allure` 参数**:
   ```bash
   python test_runner.py --serve-allure
   ```

2. **手动启动 Allure 服务器**:
   ```bash
   allure serve {report_dir}/allure-results
   ```

## 注意事项

- 确保测试文件名以 `test_` 开头或以 `_test.py` 结尾
- 确保测试函数名以 `test_` 开头
- 如果要使用 Allure 装饰器，需要安装 `allure-pytest` 包
