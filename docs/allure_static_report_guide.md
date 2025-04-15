# Allure 静态 HTML 报告使用指南

## 简介

Allure 提供了两种查看报告的方式：
1. **静态 HTML 报告**：生成一个可以直接在浏览器中打开的 HTML 文件
2. **Allure 服务器**：启动一个本地服务器来展示报告

本指南主要介绍如何生成和使用静态 HTML 报告。

## 生成静态 HTML 报告

### 使用命令行

```bash
# 运行测试并生成 Allure 静态 HTML 报告
python test_runner.py --allure-html
```

这个命令会：
1. 运行测试并生成 Allure 结果文件
2. 使用 Allure 命令行工具生成静态 HTML 报告
3. 自动在浏览器中打开报告

### 在代码中使用

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
    allure_report=True  # 生成 Allure 结果文件
)

# 生成静态 HTML 报告
runner.generate_allure_report()
```

## 报告位置

静态 HTML 报告默认生成在以下位置：
```
{report_dir}/allure-report/index.html
```

例如，如果你使用默认的报告目录 `test_reports`，报告将位于：
```
test_reports/allure-report/index.html
```

## 手动生成静态 HTML 报告

如果你已经有 Allure 结果文件，可以使用以下命令手动生成静态 HTML 报告：

```bash
# 使用 Allure 命令行工具生成报告
allure generate test_reports/allure-results -o test_reports/allure-report --clean

# 在浏览器中打开报告
open test_reports/allure-report/index.html  # macOS
# 或
start test_reports/allure-report/index.html  # Windows
```

## 静态 HTML 报告的优势

1. **无需运行服务器**：可以直接在浏览器中打开
2. **可以分享**：可以将报告文件夹压缩后分享给其他人
3. **可以部署**：可以将报告部署到静态网站托管服务上
4. **离线查看**：不需要网络连接

## 注意事项

1. **JavaScript 限制**：由于浏览器的安全限制，某些浏览器可能会阻止本地 HTML 文件加载 JavaScript。如果遇到这种情况，可以：
   - 使用 Firefox 浏览器（它允许本地文件加载 JavaScript）
   - 使用简单的 HTTP 服务器来提供文件，例如：
     ```bash
     cd test_reports/allure-report
     python -m http.server 8000
     ```
     然后在浏览器中访问 `http://localhost:8000`

2. **需要 Allure 命令行工具**：生成静态 HTML 报告需要安装 Allure 命令行工具。请参考 [Allure 官方文档](https://docs.qameta.io/allure/#_installing_a_commandline) 进行安装。
