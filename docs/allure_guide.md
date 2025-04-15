# Allure 报告使用指南

## 简介

Allure 是一个轻量级、灵活的多语言测试报告工具，它不仅可以以简单的 Web 报告形式显示测试结果，还可以提供测试的历史趋势、分类、标签等功能，使测试报告更加直观和有用。

## 安装

### 1. 安装 Allure 命令行工具

#### macOS:
```bash
brew install allure
```

#### Windows:
```bash
scoop install allure
```

#### Linux:
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### 2. 安装 Python 依赖

```bash
pip install allure-pytest
```

## 在测试中使用 Allure

### 基本装饰器

```python
import allure

@allure.epic("项目名称")
@allure.feature("功能模块")
@allure.story("用户故事")
@allure.title("测试用例标题")
@allure.description("详细描述")
@allure.severity(allure.severity_level.CRITICAL)  # 严重程度
def test_something():
    # 测试代码
    pass
```

### 测试步骤

```python
def test_with_steps():
    with allure.step("第一步"):
        # 步骤1的代码
        pass
        
    with allure.step("第二步"):
        # 步骤2的代码
        pass
```

### 添加附件

```python
def test_with_attachment():
    allure.attach(
        "文本内容", 
        name="text_attachment.txt",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # 添加图片
    with open("screenshot.png", "rb") as file:
        allure.attach(
            file.read(),
            name="screenshot.png",
            attachment_type=allure.attachment_type.PNG
        )
```

## 使用 TestRunner 生成 Allure 报告

### 基本用法

```python
from test_runner import TestRunner

runner = TestRunner(
    source="your_source_code",
    test_dir="tests",
    report_dir="test_reports"
)

# 运行测试并生成 Allure 报告
exit_code = runner.run_tests(
    allure_report=True  # 启用 Allure 报告
)
```

### 高级用法

```python
# 按特性筛选测试
exit_code = runner.run_tests(
    allure_report=True,
    allure_features=["登录功能", "用户管理"]
)

# 按史诗筛选测试
exit_code = runner.run_tests(
    allure_report=True,
    allure_epics=["用户模块"]
)

# 查看 Allure 报告
runner.serve_allure_report(port=8080)
```

## 查看报告

生成报告后，可以通过以下方式查看：

1. **生成静态报告**：
   ```bash
   allure generate test_reports/allure-results -o test_reports/allure-report --clean
   ```
   然后在浏览器中打开 `test_reports/allure-report/index.html`

2. **启动报告服务器**：
   ```bash
   allure serve test_reports/allure-results
   ```
   这将自动在浏览器中打开报告

## 报告特性

Allure 报告提供以下功能：

- **概览**：测试执行的总体情况
- **分类**：按不同类别查看测试结果
- **时间线**：测试执行的时间线
- **行为**：按 Epic > Feature > Story 层次结构查看测试
- **分类**：按严重程度、标签等分类查看测试
- **包**：按包结构查看测试
- **历史趋势**：查看测试执行的历史趋势（需要配置）

## 更多资源

- [Allure 官方文档](https://docs.qameta.io/allure/)
- [Allure-Pytest 文档](https://docs.qameta.io/allure/#_pytest)
