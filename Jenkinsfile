pipeline {
    // 使用 Docker Agent，指定一个包含 Python 3.9 的镜像
    agent {
        // --- 修正的部分：使用 dockerContainer 而不是 docker ---
        dockerContainer {
            image 'python:3.9-slim' // 你可以选择其他 Python 版本，如 python:3.10-slim
            // 如果需要传递特殊参数给 docker run，可以在这里添加 args
            // 例如，如果你需要挂载卷或以特定用户运行：
            // args '-v /some/host/path:/some/container/path -u root'
            // 注意：如果 Jenkins Docker 插件配置了默认参数，这里的 args 会附加或覆盖它们
            // 通常 $HOME/.m2 这类挂载对 Maven 更常见，Python 项目通常不需要挂载缓存目录，
            // 除非你有特定的本地包或配置需要映射。
            // 如果 Jenkins Agent 运行 Docker 需要特殊标签，可以添加：
            // label 'docker-agent' // 取消注释并替换为你的 Docker agent 标签 (如果需要)
        }
        // --- 修正结束 ---
    }
    tools {
        // 确保 Jenkins -> Manage Jenkins -> Global Tool Configuration 中配置了名为 'Allure' 的 Allure Commandline 安装
        allure 'Allure' // Allure 工具仍然由 Jenkins 管理，但会在容器内使用 (Jenkins 会处理路径映射)
    }
    stages {
        // stage('检出代码') { // 这个阶段可以省略，因为 agent 会自动检出 SCM
        //     steps {
        //         checkout scm
        //     }
        // }

        stage('安装依赖') {
            steps {
                // 这些 sh 命令现在会在 Docker 容器内部执行
                sh 'python --version' // 验证容器内的 Python 版本
                sh 'pip --version'    // 验证容器内的 pip
                // 最好加上 --no-cache-dir 避免不必要的缓存占用，或者使用 --cache-dir 指定容器内的缓存位置
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('运行测试') {
            steps {
                // 这些命令也在容器内执行
                sh '''
                # 确保报告目录存在
                mkdir -p test_reports/allure-results
                mkdir -p test_reports/coverage

                echo "Running tests with Pytest..."
                # 使用容器内的 python
                python -m pytest tests \
                    -v \
                    --alluredir=test_reports/allure-results \
                    --cov=codes \
                    --cov-report=term-missing \
                    --cov-report=html:test_reports/coverage \
                    --cov-report=xml:test_reports/coverage/coverage.xml

                echo "Pytest finished."
                # 可以在这里检查 pytest 的退出码，如果非 0 则可能需要失败构建
                # sh 'if [ $? -ne 0 ]; then echo "Pytest failed"; exit 1; fi' # (可选)
                '''

                // 这个 Python 脚本也在容器内执行
                sh '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys

print(f'--- Python Script for Allure Environment ---')
print(f'Python executable: {sys.executable}')
print(f'Current working directory: {os.getcwd()}')

coverage_file = 'test_reports/coverage/coverage.xml'
allure_env_file = 'test_reports/allure-results/environment.properties'

print(f'Checking for coverage file: {coverage_file}')
print(f'Target Allure environment file: {allure_env_file}')

# 确保 allure-results 目录存在
allure_dir = os.path.dirname(allure_env_file)
if not os.path.exists(allure_dir):
    print(f'Creating directory: {allure_dir}')
    os.makedirs(allure_dir, exist_ok=True)

if os.path.exists(coverage_file):
    print(f'Found {coverage_file}. Parsing...')
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()

        # Cobertura format often uses 'line-rate'
        if 'line-rate' in root.attrib:
            coverage_pct = float(root.attrib['line-rate']) * 100
            total_lines = int(root.attrib.get('lines-valid', 0)) # lines-valid might not always be present
            covered_lines = int(float(root.attrib.get('lines-covered', 0))) # lines-covered might not always be present

            print(f'Coverage Percentage: {coverage_pct:.2f}%')
            print(f'Total Valid Lines (approx): {total_lines}')
            print(f'Covered Lines (approx): {covered_lines}')

            # 写入 Allure environment 文件
            print(f'Writing coverage info to {allure_env_file}')
            with open(allure_env_file, 'w', encoding='utf-8') as f:
                f.write(f'Coverage={coverage_pct:.2f}%\\n') # 使用 \\n 转义换行符
                if total_lines > 0: # 只有当获取到有效行数时才写入
                    f.write(f'Total_Lines={total_lines}\\n')
                    f.write(f'Covered_Lines={covered_lines}\\n')
            print(f'Successfully wrote coverage info to {allure_env_file}')

        # 有些 coverage.xml 可能直接在 <coverage> 标签下有 line-rate
        elif root.tag == 'coverage' and 'line-rate' in root.attrib:
             coverage_pct = float(root.attrib['line-rate']) * 100
             # 其他属性可能不同，这里只取百分比
             print(f'Coverage Percentage (from root): {coverage_pct:.2f}%')
             with open(allure_env_file, 'w', encoding='utf-8') as f:
                f.write(f'Coverage={coverage_pct:.2f}%\\n')
             print(f'Successfully wrote coverage percentage to {allure_env_file}')
        else:
            print(f'Could not find "line-rate" attribute in the root element of {coverage_file}. Root attributes: {root.attrib}')
            # 尝试查找 <package> 或 <class> 级别的覆盖率 (更复杂，通常不需要)

    except ET.ParseError as e:
        print(f'Error parsing XML file {coverage_file}: {e}')
    except KeyError as e:
        print(f'Missing expected attribute in {coverage_file}: {e}')
    except Exception as e:
        print(f'An unexpected error occurred while processing {coverage_file}: {e}')
else:
    print(f'Coverage file {coverage_file} does not exist. Skipping adding coverage info to Allure environment.')

print(f'--- Finished Python Script ---')
'''
            }
        }
    }

    post {
        // always 块确保无论构建成功或失败，都会尝试执行这些步骤
        always {
            echo "Executing post-build actions..."
            // Allure 报告生成步骤
            // 这个步骤会在 Jenkins Agent (宿主机或指定的 Agent 节点) 上运行，
            // 使用 Jenkins 配置的 Allure Commandline 工具。
            // 它会读取工作区内的 test_reports/allure-results 目录。
            echo "Generating Allure report..."
            allure(
                includeProperties: false, // 通常设为 false，因为我们手动生成了 environment.properties
                jdk: '', // 通常留空，除非你需要指定特定的 JDK
                properties: [], // 可以添加额外的属性
                reportBuildPolicy: 'ALWAYS', // 每次都生成报告
                results: [[path: 'test_reports/allure-results']] // 指定 Allure 结果目录，路径相对于工作区
            )
            echo "Allure report generation attempted."

            // 发布 HTML 覆盖率报告
            // 这个步骤也会在 Jenkins Agent 上运行，读取工作区内的文件。
            echo "Publishing HTML coverage report..."
            publishHTML(
                allowMissing: true, // 允许报告目录或文件丢失 (例如测试失败未生成)
                alwaysLinkToLastBuild: true, // 总是链接到最新构建的报告
                keepAll: true, // 保留所有历史报告 (注意磁盘空间)
                reportDir: 'test_reports/coverage', // 覆盖率报告目录，路径相对于工作区
                reportFiles: 'index.html', // 要链接的主文件
                reportName: 'Coverage Report', // 报告在 Jenkins UI 中显示的名称
                reportTitles: '' // 可选的报告标题
            )
            echo "HTML coverage report publishing attempted."
        }
        success {
            echo "Build successful!"
        }
        failure {
            echo "Build failed!"
            // 可以在这里添加失败时的通知，例如发送邮件或 Slack 消息
        }
        unstable {
             echo "Build unstable (e.g., tests failed but post actions ran)."
        }
    }
}