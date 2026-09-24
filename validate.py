from pathlib import Path
import pandas as pd
import engine

BASE = Path(__file__).parent
required_files = [
    BASE / "app.py", BASE / "engine.py", BASE / "requirements.txt",
    BASE / "data" / "purchase_register.csv", BASE / "data" / "gstr2b_demo.csv",
    BASE / "docs" / "BUSINESS_PLAN.md", BASE / "docs" / "AUTOMATION_MAP.md",
    BASE / "docs" / "PITCH_2_MINUTES.md", BASE / "docs" / "JUDGE_QA.md", BASE / "docs" / "DEMO_SCRIPT.md",
]
for f in required_files:
    assert f.exists(), f"Missing {f}"
books, filing = engine.load_demo()
engine.validate_columns(books, "Purchase Register")
engine.validate_columns(filing, "GST Filing")
result = engine.reconcile(books, filing, 1.0)
assert len(result) > 0
assert "Exception Type" in result.columns
assert "Priority" in result.columns
assert result["Exposure"].ge(0).all()
print("VALIDATION PASSED")
print(f"Purchase records: {len(books)}")
print(f"Filing records: {len(filing)}")
print(f"Output rows: {len(result)}")
print("Exceptions:")
print(result["Exception Type"].value_counts().to_string())
