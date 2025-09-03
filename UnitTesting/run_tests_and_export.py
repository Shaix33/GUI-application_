# run_tests_and_export.py
# run_tests_and_export.py
import subprocess
import json
import pandas as pd
import os
from datetime import datetime

# 1. First, run pytest with JSON reporting to generate the report file
print("Running tests and generating JSON report...")
result = subprocess.run(
    ['python', '-m', 'pytest', 'test_garden.py', '-v', '--json-report', '--json-report-file=test_report.json'],
    capture_output=True,
    text=True
)

# Check if the report file was created
if not os.path.exists('test_report.json'):
    print("ERROR: test_report.json was not created. Pytest output:")
    print(result.stdout)
    print(result.stderr)
    exit(1)

# 2. Load the JSON report
print("Loading test results...")
with open('test_report.json', 'r') as f:
    report_data = json.load(f)

# 3. Define our test cases with their metadata for the Excel report
test_case_mapping = {
    'test_frost_alert_positive': {
        'ID': 'TC-PY-01',
        'Scenario': 'Frost Alert - Positive Temperature (-1°C)',
        'Input Data': 'temperature = -1',
        'Expected Output': 'True'
    },
    'test_frost_alert_zero': {
        'ID': 'TC-PY-02',
        'Scenario': 'Frost Alert - Boundary Temperature (0°C)',
        'Input Data': 'temperature = 0',
        'Expected Output': 'True'
    },
    'test_frost_alert_negative': {
        'ID': 'TC-PY-03',
        'Scenario': 'Frost Alert - Negative Test (5°C)',
        'Input Data': 'temperature = 5',
        'Expected Output': 'False'
    },
    'test_frost_alert_none': {
        'ID': 'TC-PY-04',
        'Scenario': 'Frost Alert - None Input',
        'Input Data': 'temperature = None',
        'Expected Output': 'False'
    },
    'test_harvest_date_calculation': {
        'ID': 'TC-PY-05',
        'Scenario': 'Calculate Harvest Date',
        'Input Data': 'planted_date=2024-01-01, days_to_maturity=75',
        'Expected Output': '2024-03-16'
    },
    'test_pest_search_by_name': {
        'ID': 'TC-PY-06',
        'Scenario': 'Pest Search - By Name',
        'Input Data': 'search_term = "Aphid"',
        'Expected Output': 'List with 1 result: Aphid'
    },
    'test_pest_search_by_description': {
        'ID': 'TC-PY-07',
        'Scenario': 'Pest Search - By Description',
        'Input Data': 'search_term = "fungal"',
        'Expected Output': 'List with 1 result: Powdery Mildew'
    },
    'test_pest_search_not_found': {
        'ID': 'TC-PY-08',
        'Scenario': 'Pest Search - Not Found',
        'Input Data': 'search_term = "rabbit"',
        'Expected Output': 'Empty list'
    },
    'test_pest_search_empty_term': {
        'ID': 'TC-PY-09',
        'Scenario': 'Pest Search - Empty Term',
        'Input Data': 'search_term = ""',
        'Expected Output': 'Empty list'
    }
}

# 4. Parse the pytest results and combine with our mapping
excel_data = []
for test in report_data['tests']:
    nodeid = test['nodeid'] # e.g., 'test_garden.py::test_frost_alert_positive'
    test_name = nodeid.split('::')[-1] # Just get the function name
    
    if test_name in test_case_mapping:
        test_info = test_case_mapping[test_name]
        outcome = test['outcome']
        
        excel_data.append({
            'Test Case ID': test_info['ID'],
            'Test Scenario': test_info['Scenario'],
            'Input Data': test_info['Input Data'],
            'Expected Output': test_info['Expected Output'],
            'Actual Output': 'Pass' if outcome == 'passed' else 'Fail',
            'Test Result': outcome.upper(), # 'PASS' or 'FAIL'
            'Date Executed': datetime.now().strftime("%Y-%m-%d")
        })

# 5. Create a DataFrame and export to Excel
if excel_data:
    df = pd.DataFrame(excel_data)
    # Reorder columns to match your requested format
    df = df[['Test Case ID', 'Test Scenario', 'Input Data', 'Expected Output', 'Actual Output', 'Test Result', 'Date Executed']]

    try:
        with pd.ExcelWriter('Unit_Test_Results.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Test Results', index=False)
            # Auto-adjust columns' width
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Test Results'].column_dimensions[chr(65 + col_idx)].width = column_width + 2
        print("SUCCESS: Test results exported to 'Unit_Test_Results.xlsx'")
        print(f"Total tests exported: {len(excel_data)}")
    except Exception as e:
        print(f"ERROR: Could not write to Excel file. {e}")
else:
    print("WARNING: No test data found to export.")