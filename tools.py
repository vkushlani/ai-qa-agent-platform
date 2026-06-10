import os
from tavily import TavilyClient

def web_search(query):

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "TAVILY_API_KEY is not configured."

    client = TavilyClient(api_key=api_key)

    results = client.search(
        query=query,
        max_results=5
    )

    return results

def analyze_risk(module_name):
    
    risks = {
        "payment": "High regression risk due to transaction handling.",
        "checkout": "Medium risk due to session changes.",
        "login": "High security testing required.",
        "cart": "Performance regression risk exists."
    }
    
    return risks.get(module_name.lower(),
        "No specific risk identified."
        )
    
def generate_test_cases(module_name):

    test_cases = {
        "payment": [
            "Validate retry handling",
            "Verify failed transaction recovery",
            "Test timeout behavior"
        ],

        "login": [
            "Verify MFA flow",
            "Test invalid password handling",
            "Validate password reset"
        ]
    }

    return test_cases.get(
        module_name.lower(),
        ["No test cases available."]
    )

def generate_testing_strategy(module_name):

    strategies = {

        "payment": """
        - Validate retries
        - Verify transaction rollback
        - Test timeout handling
        - Validate fraud detection
        """,

        "login": """
        - Test MFA
        - Validate password reset
        - Verify session handling
        - Test invalid login attempts
        """,

        "checkout": """
        - Verify discounts
        - Validate cart totals
        - Test session expiration
        """
    }

    return strategies.get(
        module_name.lower(),
        "No strategy available."
    )