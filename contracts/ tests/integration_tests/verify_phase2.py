(
echo import json
echo import os
echo.
echo def run_phase2_verification():
echo     report_path = os.path.join(os.path.dirname(__file__), 'INTEGRATION_REPORT_PHASE2.json')
echo     if not os.path.exists(report_path^):
echo         print("ERROR: INTEGRATION_REPORT_PHASE2.json not found!")
echo         return False
echo     with open(report_path, 'r') as f:
echo         data = json.load(f)
echo     print("=" * 50)
echo     print("PHASE 2 - MANUAL TESTING VERIFICATION")
echo     print("=" * 50)
echo     print(f"Report ID: {data['report_id']}")
echo     print(f"Status: {data['status']}")
echo     print("-" * 50)
echo     total_passed = 0
echo     total_failed = 0
echo     for category in data['detailed_results']:
echo         cat_name = category['category']
echo         print(f"\nCategory: {cat_name}")
echo         for test in category['tests']:
echo             if test['status'] == 'PASS':
echo                 print(f"  [PASS] {test['id']}: {test['name']} - {test['result']}")
echo                 total_passed += 1
echo             else:
echo                 print(f"  [FAIL] {test['id']}: {test['name']}")
echo                 total_failed += 1
echo     print("-" * 50)
echo     print(f"SUMMARY: {total_passed} passed, {total_failed} failed")
echo     if total_failed == 0:
echo         print("\nALL PHASE 2 TESTS PASSED")
echo         return True
echo     else:
echo         return False
echo.
echo if __name__ == "__main__":
echo     run_phase2_verification()
) > verify_phase2.py
if __name__ == "__main__":
    run_integration_verification()
