pipeline {
    agent any // Still runs on the controller node or any available agent
    tools {
        allure 'Allure' // Use Allure defined in Global Tool Configuration
    }
    stages {
        stage('检出代码') {
            steps {
                // Clean workspace before checkout is often a good idea
                // cleanWs()
                checkout scm
            }
        }
        stage('安装依赖') {
            steps {
                // Use sh block for multiple commands
                sh '''
                    echo "INFO: Checking Python version..."
                    python3 --version || python --version // Check which command works

                    echo "INFO: Setting up virtual environment..."
                    # Use python3 preferably, fallback to python if needed
                    python3 -m venv venv || python -m venv venv

                    echo "INFO: Activating virtual environment..."
                    source venv/bin/activate

                    echo "INFO: Upgrading pip..."
                    pip install --upgrade pip

                    echo "INFO: Installing requirements..."
                    pip install -r requirements.txt

                    echo "INFO: Deactivating (automatic on script exit)..."
                    # deactivate command is usually not needed here as the shell step ends
                '''
            }
        }
        stage('运行测试') {
            steps {
                // Activate venv *before* running pytest
                sh '''
                    echo "INFO: Activating virtual environment for tests..."
                    source venv/bin/activate

                    echo "INFO: Creating report directories..."
                    mkdir -p test_reports/allure-results
                    mkdir -p test_reports/coverage

                    echo "INFO: Running pytest with coverage..."
                    # 使用重定向和忽略失败状态
                    python -m pytest tests \
                        -v \
                        --alluredir=test_reports/allure-results \
                        --cov=codes \
                        --cov-report=term-missing \
                        --cov-report=html:test_reports/coverage \
                        --cov-report=xml:test_reports/coverage/coverage.xml \
                        --no-summary -q || true
                '''

                // Activate venv *before* running the inline python script
                sh '''
                    echo "INFO: Activating virtual environment for coverage processing..."
                    source venv/bin/activate

                    echo "INFO: Adding coverage info to Allure environment..."
                    # Use 'python' which should now point to the venv's python
                    python -c "
import xml.etree.ElementTree as ET
import os

coverage_file = 'test_reports/coverage/coverage.xml'
allure_env_file = 'test_reports/allure-results/environment.properties'

# Check if coverage XML exists
if os.path.exists(coverage_file):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()

        # Extract coverage data Safely
        line_rate = root.get('line-rate') # Use .get for safety
        lines_valid = root.get('lines-valid', '0') # Default to '0' if missing
        lines_covered = root.get('lines-covered', '0') # Default to '0' if missing

        if line_rate is not None:
            try:
                coverage_pct = float(line_rate) * 100
                total_lines = int(lines_valid)
                covered_lines = int(lines_covered) # Was float before, should likely be int

                # Create/Append environment properties file
                mode = 'a' if os.path.exists(allure_env_file) else 'w'
                with open(allure_env_file, mode) as f:
                    if mode == 'a': # Add newline if appending
                        f.write('\\n')
                    f.write(f'Coverage={coverage_pct:.2f}%\\n')
                    f.write(f'Total_Lines={total_lines}\\n')
                    f.write(f'Covered_Lines={covered_lines}\\n')

                print(f'INFO: Added coverage info to Allure: {coverage_pct:.2f}%')
            except ValueError as e:
                print(f'WARN: Could not parse coverage numbers: {e}')
        else:
            print('WARN: line-rate attribute not found in coverage.xml')

    except ET.ParseError as e:
        print(f'WARN: Could not parse coverage XML file {coverage_file}: {e}')
    except Exception as e:
        print(f'WARN: An unexpected error occurred processing coverage: {e}')
else:
    print(f'WARN: Coverage file not found: {coverage_file}')
"
                '''
            }
        }
    }

    post {
        always {
            // Generate Allure report using the configured tool
            // results path is relative to workspace root
            allure([
                includeProperties: false, // environment.properties is generated manually
                jdk: '', // Use default JDK
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'test_reports/allure-results']]
            ])

            // Archive HTML coverage report
            publishHTML([
                allowMissing: true, // Set to true if tests might fail before generating report
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test_reports/coverage', // Relative to workspace root
                reportFiles: 'index.html',
                reportName: 'Coverage Report', // Updated name
                reportTitles: '' // Optional: Title for the frame
            ])
        }
    }
}