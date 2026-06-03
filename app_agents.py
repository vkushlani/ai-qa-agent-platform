from langchain_openai import ChatOpenAI

from app_tools import (
    save_test_cases,
    save_traceability_report,
    save_defect_report,
    save_regression_report,
    run_mock_login_test
)



llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)

# ======================================
# TEST CASE AGENT
# ======================================

def test_case_agent(context, question):

    prompt = f"""
You are a Senior QA Test Design Agent.

Generate:

1. Positive test cases
2. Negative test cases
3. Edge cases
4. Regression scenarios

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    file_path = save_test_cases(
        response.content
    )
    return response.content
#     return f"""
# {response.content}

# --------------------------

# Exported To:

# {file_path}
# """


# ======================================
# DEFECT AGENT
# ======================================

def defect_analysis_agent(
    context,
    question
):

    prompt = f"""
You are a Senior Defect Analysis Agent.

Analyze:

- Root Cause
- Impact
- Severity
- Priority
- Recommendations

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    file_path = save_defect_report(
        response.content
    )
    return response.content
#     return f"""
# {response.content}

# --------------------------

# Exported To:

# {file_path}
# """


# ======================================
# TRACEABILITY AGENT
# ======================================

def requirement_traceability_agent(
    context,
    question
):

    prompt = f"""
You are a Requirement Traceability Agent.

Create:

- Requirement Mapping
- Coverage Matrix
- Missing Coverage
- Recommendations

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    file_path = save_traceability_report(
        response.content
    )
    return response.content
#     return f"""
# {response.content}

# --------------------------

# Exported To:

# {file_path}
# """


# ======================================
# REGRESSION AGENT
# ======================================

def regression_risk_agent(
    context,
    question
):

    prompt = f"""
You are a Regression Risk Agent.

Analyze:

- High Risk Areas
- Impacted Modules
- Regression Scope
- Priorities

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    file_path = save_regression_report(
        response.content
    )

    return response.content
#     return f"""
# {response.content}

# --------------------------

# Exported To:

# {file_path}
# """


# ======================================
# QA REPORT AGENT
# ======================================

def qa_report_agent(context):

    prompt = f"""
You are a QA Reporting Agent.

Create:

- Executive Summary
- Risks
- Findings
- Recommendations

Context:
{context}
"""

    response = llm.invoke(prompt)

    return response.content


# ======================================
# COVERAGE PIPELINE
# ======================================

def coverage_analysis_pipeline(
    context,
    question
):

    traceability_output = (
        requirement_traceability_agent(
            context,
            question
        )
    )

    test_output = (
        test_case_agent(
            traceability_output,
            question
        )
    )

    risk_output = (
        regression_risk_agent(
            test_output,
            question
        )
    )

    combined = f"""

TRACEABILITY

{traceability_output}

TEST CASES

{test_output}

REGRESSION

{risk_output}
"""

    final_report = qa_report_agent(
        combined
    )

    return final_report


# ======================================
# AUTOMATION AGENT
# ======================================

def automation_agent(question):

    result = run_mock_login_test()

    return result


# ======================================
# COORDINATOR AGENT
# ======================================

def coordinator_agent(
    query_type,
    context,
    question
):

    if query_type == "test_case":

        return test_case_agent(
        context,
        question
    )

    elif query_type == "defect_analysis":

        return defect_analysis_agent(
            context,
            question
        )

    elif query_type == "traceability":

        return requirement_traceability_agent(
            context,
            question
        )

    elif query_type == "regression_risk":

        return regression_risk_agent(
            context,
            question
        )

    elif query_type == "coverage_pipeline":

        return coverage_analysis_pipeline(
            context,
            question
        )
    elif query_type == "website_testing":

        return website_testing_agent(
        context,
        question
    )
    elif query_type == "planning":

        return planning_agent(
        question
    )
    elif query_type == "automation":

        return automation_agent(
            question
        )

    return "No suitable agent found."

def website_testing_agent(
    context,
    question
):
    prompt = f"""
You are a Senior Website Testing Agent.

Generate:

1. Functional Tests

2. UI Tests

3. Negative Tests

4. Security Tests

5. Performance Risks

Question:

{question}
"""
    response = llm.invoke(prompt)

    return response.content

def planning_agent(question):
    prompt = f"""
You are an AI Planning Agent.

Your job is to break the user's request
into logical QA tasks.

Question:

{question}

Return:

1. Step-by-step plan
2. Recommended QA activities
"""
    response = llm.invoke(prompt)

    return response.content