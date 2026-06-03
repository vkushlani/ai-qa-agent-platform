# tools.py

import os

EXPORT_FOLDER = "exports"

os.makedirs(
    EXPORT_FOLDER,
    exist_ok=True
)

# =====================================
# SAVE TEST CASES
# =====================================

def save_test_cases(test_cases):

    file_path = os.path.join(
        EXPORT_FOLDER,
        "generated_test_cases.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(test_cases)

    return file_path


# =====================================
# SAVE TRACEABILITY REPORT
# =====================================

def save_traceability_report(report):

    file_path = os.path.join(
        EXPORT_FOLDER,
        "traceability_report.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    return file_path


# =====================================
# SAVE DEFECT REPORT
# =====================================

def save_defect_report(report):

    file_path = os.path.join(
        EXPORT_FOLDER,
        "defect_analysis_report.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    return file_path


# =====================================
# SAVE REGRESSION REPORT
# =====================================

def save_regression_report(report):

    file_path = os.path.join(
        EXPORT_FOLDER,
        "regression_risk_report.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    return file_path


# =====================================
# MOCK AUTOMATION TOOL
# =====================================

def run_mock_login_test():

    return """
LOGIN TEST RESULTS

Open Login Page ........ PASS
Enter Username ......... PASS
Enter Password ......... PASS
Click Login ............ PASS

OVERALL RESULT: PASS
"""