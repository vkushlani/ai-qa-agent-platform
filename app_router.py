def classify_question(question):

    question = question.lower()

    if any(word in question for word in [
        "compare",
        "difference",
        "similarities",
        "different"
    ]):
        return "comparison"

    elif any(word in question for word in [
    "how many documents",
    "number of documents",
    "how many files",
    "number of files",
    "how many uploaded",
    "how many document"
]):
        return "document_count"
    
    elif any(word in question for word in [
    "test case",
    "testing scenarios",
    "generate tests"
    ]):
        return "test_case"
    
    elif any(word in question for word in [
    "defect",
    "bug",
    "failure",
    "root cause"
    ]):
        return "defect_analysis"

    elif any(word in question for word in [
    "traceability",
    "requirement mapping",
    "coverage"
    ]):
        return "traceability"
    
    elif any(word in question for word in [

    "website testing",

    "website test",

    "web testing",

    "test website"

]):
        return "website_testing"
    
    elif any(word in question for word in [

    "release readiness",

    "production readiness",

    "go live readiness",

    "ready to release",

    "ready for release",

    "ready for production",

    "release review",
    "release",

    "production",

    "go live",

    "readiness"


]):

        return "planning"

    elif any(word in question for word in [
    "regression",
    "risk",
    "impacted modules"
    ]):
        return "regression_risk"   
     
    elif any(word in question for word in [
        "summary",
        "summarize"
    ]):
        return "summary"
    elif any(word in question for word in [
        "coverage analysis"
    ]):
        return "coverage_pipeline"
    elif any(word in question for word in [
    "latest",
    "current",
    "today",
    "recent",
    "new books",
    "book references",
    "latest version"
]):
        return "web_search"

    elif any(word in question for word in [
        "run test"
        ,"execute test",
        "test execution"
    ]):
        return "automation"
    
    elif any(word in question for word in [
    "name of uploaded document",
    "name of the uploaded document",
    "names of uploaded documents",
    "uploaded document name",
    "uploaded file name",
    "uploaded file names",
    "what document did i upload",
    "which document did i upload"
]):
        return "document_names"
    
    elif any(word in question for word in [
    "latest",
    "current",
    "recent",
    "new",
    "news",
    "web search",
    "internet",
    "online",
    "book references",
    "books",
    "references",
    "latest version"
]):
        return "web_search"

    else:
        return "rag_search"
    
