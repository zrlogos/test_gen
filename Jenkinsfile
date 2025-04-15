pipeline {
    agent any
    tools {
        allure 'Allure' // 使用在全局工具配置中定义的Allure
    }
    stages {
        stage('检出代码') {
            steps {
                checkout scm
            }
        }
        stage('安装依赖') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('运行测试') {
            steps {
                // 与test_runner_allure.py相同的功能：
                // 1. 运行pytest并生成Allure结果
                // 2. 生成覆盖率报告
                sh '''
                mkdir -p test_reports/allure-results
                mkdir -p test_reports/coverage

                python -m pytest tests \
                    -v \
                    --alluredir=test_reports/allure-results \
                    --cov=codes \
                    --cov-report=term-missing \
                    --cov-report=html:test_reports/coverage \
                    --cov-report=xml:test_reports/coverage/coverage.xml
                '''

                // 添加覆盖率信息到Allure结果中
                sh '''
                python -c "
import xml.etree.ElementTree as ET
import os

# 读取覆盖率XML
if os.path.exists('test_reports/coverage/coverage.xml'):
    tree = ET.parse('test_reports/coverage/coverage.xml')
    root = tree.getroot()

    # 提取覆盖率数据
    if 'line-rate' in root.attrib:
        coverage_pct = float(root.attrib['line-rate']) * 100
        total_lines = int(root.attrib.get('lines-valid', 0))
        covered_lines = int(float(root.attrib.get('lines-covered', 0)))

        # 创建环境属性文件
        with open('test_reports/allure-results/environment.properties', 'w') as f:
            f.write(f'Coverage={coverage_pct:.2f}%\\n')
            f.write(f'Total_Lines={total_lines}\\n')
            f.write(f'Covered_Lines={covered_lines}\\n')

        print(f'已添加覆盖率信息到Allure报告：{coverage_pct:.2f}%')
"
                '''
            }
        }
    }

    post {
        always {
            // 生成Allure报告
            allure([
                includeProperties: false,
                jdk: '',
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'test_reports/allure-results']]
            ])

            // 归档覆盖率报告
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test_reports/coverage',
                reportFiles: 'index.html',
                reportName: '覆盖率报告',
                reportTitles: ''
            ])
        }
    }
}