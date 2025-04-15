pipeline {
    // 使用 Docker Agent，指定一个包含 Python 3.9 的镜像
    agent {
        docker {
            image 'python:3.9-slim' // 你可以选择其他 Python 版本，如 python:3.10-slim
            // 如果需要传递特殊参数给 docker run，可以在这里添加 args
            // args '-v /some/host/path:/some/container/path -u root'
        }
    }
    tools {
        allure 'Allure' // Allure 工具仍然由 Jenkins 管理，但会在容器内使用
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
                sh 'pip install -r requirements.txt'
            }
        }

        stage('运行测试') {
            steps {
                // 这些命令也在容器内执行
                sh '''
                mkdir -p test_reports/allure-results
                mkdir -p test_reports/coverage

                # 使用容器内的 python
                python -m pytest tests \
                    -v \
                    --alluredir=test_reports/allure-results \
                    --cov=codes \
                    --cov-report=term-missing \
                    --cov-report=html:test_reports/coverage \
                    --cov-report=xml:test_reports/coverage/coverage.xml
                '''

                // 这个 Python 脚本也在容器内执行
                sh '''
                python -c "
import xml.etree.ElementTree as ET
import os
import sys

print(f'Python executable: {sys.executable}')
print(f'Current working directory: {os.getcwd()}')
print(f'Checking for coverage file: test_reports/coverage/coverage.xml')

coverage_file = 'test_reports/coverage/coverage.xml'
allure_env_file = 'test_reports/allure-results/environment.properties'

# 确保 allure-results 目录存在 (pytest 应该已经创建，但以防万一)
os.makedirs(os.path.dirname(allure_env_file), exist_ok=True)

if os.path.exists(coverage_file):
    print(f'Found {coverage_file}')
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()

        if 'line-rate' in root.attrib:
            coverage_pct = float(root.attrib['line-rate']) * 100
            total_lines = int(root.attrib.get('lines-valid', 0))
            covered_lines = int(float(root.attrib.get('lines-covered', 0)))

            with open(allure_env_file, 'w') as f:
                f.write(f'Coverage={coverage_pct:.2f}%\\n')
                f.write(f'Total_Lines={total_lines}\\n')
                f.write(f'Covered_Lines={covered_lines}\\n')
                print(f'Successfully wrote coverage info to {allure_env_file}')

            print(f'已添加覆盖率信息到Allure报告：{coverage_pct:.2f}%')
        else:
            print(f'Could not find line-rate attribute in {coverage_file}')
    except ET.ParseError as e:
        print(f'Error parsing {coverage_file}: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
else:
    print(f'{coverage_file} does not exist. Skipping adding coverage to Allure.')
"
                '''
            }
        }
    }

    post {
        always {
            // Allure 报告和 HTML 发布仍在 agent 节点 (宿主机) 的上下文中运行，
            // 但它们操作的是容器执行后留在工作区的文件。
            allure([
                includeProperties: false,
                jdk: '',
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'test_reports/allure-results']] // 路径相对于工作区
            ])

            publishHTML([
                allowMissing: true, // 建议设为 true，如果测试失败可能没有覆盖率报告
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test_reports/coverage', // 路径相对于工作区
                reportFiles: 'index.html',
                reportName: '覆盖率报告',
                reportTitles: ''
            ])
        }
    }
}