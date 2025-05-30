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
        stage('运行测试并处理覆盖率') { // Renamed stage for clarity
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
                    # --cov-branch IS ALREADY HERE, which is correct!
                    python -m pytest tests \
                        -v \
                        --alluredir=test_reports/allure-results \
                        --cov=codes \
                        --cov-branch \
                        --cov-report=term-missing \
                        --cov-report=html:test_reports/coverage \
                        --cov-report=xml:test_reports/coverage/coverage.xml \
                        --cov-report=json:test_reports/coverage/coverage.json \
                        --cov-report=annotate:test_reports/coverage/annotated \
                        --durations=10 \
                        --verbose \
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

coverage_xml_file = 'test_reports/coverage/coverage.xml'
allure_env_file = 'test_reports/allure-results/environment.properties'

properties_to_write = []

# Check if coverage XML exists
if os.path.exists(coverage_xml_file):
    try:
        tree = ET.parse(coverage_xml_file)
        root = tree.getroot()

        # --- Line Coverage ---
        line_rate_str = root.get('line-rate') # Use .get for safety
        lines_valid_str = root.get('lines-valid', '0') # Default to '0' if missing
        lines_covered_str = root.get('lines-covered', '0') # Default to '0' if missing

        if line_rate_str is not None:
            try:
                line_coverage_pct = float(line_rate_str) * 100
                total_lines = int(lines_valid_str)
                covered_lines = int(lines_covered_str)

                properties_to_write.append(f'Line_Coverage={line_coverage_pct:.2f}%\\n')
                properties_to_write.append(f'Total_Lines={total_lines}\\n')
                properties_to_write.append(f'Covered_Lines={covered_lines}\\n')
                print(f'INFO: Parsed Line Coverage: {line_coverage_pct:.2f}% ({covered_lines}/{total_lines})')
            except ValueError as e:
                print(f'WARN: Could not parse line coverage numbers: {e}')
        else:
            print('WARN: line-rate attribute not found in coverage.xml for line coverage.')

        # --- Branch Coverage ---
        # coverage.xml attributes for branches are typically:
        # 'branches-covered', 'branches-valid', 'branch-rate'
        branches_covered_str = root.get('branches-covered', '0')
        branches_valid_str = root.get('branches-valid', '0')
        # branch_rate_str = root.get('branch-rate') # Optional: can use this directly if preferred

        try:
            total_branches = int(branches_valid_str)
            covered_branches = int(branches_covered_str)
            branch_coverage_pct = 0.0
            if total_branches > 0:
                branch_coverage_pct = (covered_branches / total_branches) * 100.0

            # Even if total_branches is 0, branch_rate might be 1.0 (100%)
            # It's good to record the numbers.
            properties_to_write.append(f'Branch_Coverage={branch_coverage_pct:.2f}%\\n')
            properties_to_write.append(f'Total_Branches={total_branches}\\n')
            properties_to_write.append(f'Covered_Branches={covered_branches}\\n')
            print(f'INFO: Parsed Branch Coverage: {branch_coverage_pct:.2f}% ({covered_branches}/{total_branches})')

        except ValueError as e:
            print(f'WARN: Could not parse branch coverage numbers: {e}')

        # --- Write all properties to file ---
        if properties_to_write:
            # Overwrite the file with all collected properties
            with open(allure_env_file, 'w') as f:
                for prop_line in properties_to_write:
                    f.write(prop_line)
            print(f'INFO: Allure environment properties file updated/created at {allure_env_file}')
        else:
            print(f'WARN: No coverage properties were parsed to write to {allure_env_file}')

    except ET.ParseError as e:
        print(f'WARN: Could not parse coverage XML file {coverage_xml_file}: {e}')
    except Exception as e:
        print(f'WARN: An unexpected error occurred processing coverage: {e}')
else:
    print(f'WARN: Coverage XML file not found: {coverage_xml_file}. Cannot add coverage to Allure environment.')
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
                includeProperties: false, // environment.properties is generated manually by our script
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