import json
import os

def run_phase2_verification():
    """
    Verifies Phase 2 manual testing results from JSON report.
    """
    report_path = os.path.join(os.path.dirname(__file__), 'PHASE2_REPORT.json')
    
    if not os.path.exists(report_path):
        print("❌ ERROR: PHASE2_REPORT.json not found!")
        return False
    
    with open(report_path, 'r') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("PHASE 2 - MANUAL TESTING VERIFICATION")
    print("=" * 60)
    print(f"Report ID: {data['report_id']}")
    print(f"Timestamp: {data['timestamp']}")
    print(f"Status: {data['status']}")
    print("-" * 60)
    
    total_passed = 0
    total_failed = 0
    categories = data['detailed_results']
    
    for category in categories:
        cat_name = category['category']
        tests = category['tests']
        print(f"\n📁 {cat_name}: {len(tests)} tests")
        
        for test in tests:
            if test['status'] == 'PASS':
                print(f"  ✅ {test['id']}: {test['name']} - {test.get('result', test.get('decision', 'PASS'))}")
                total_passed += 1
            else:
                print(f"  ❌ {test['id']}: {test['name']} - FAILED")
                total_failed += 1
    
    print("-" * 60)
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   Total Tests: {total_passed + total_failed}")
    print(f"   PASSED: {total_passed}")
    print(f"   FAILED: {total_failed}")
    
    print(f"\n🔍 VERIFICATION READ METHODS:")
    verif = data.get('verification_read_methods', {})
    print(f"   get_threshold: {verif.get('get_threshold', 'N/A')}")
    print(f"   executors count: {len(verif.get('get_executors', []))}")
    print(f"   consensus: {verif.get('consensus', 'N/A')}")
    
    if total_failed == 0:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS: All Phase 2 tests passed!")
        print("=" * 60)
        return True
    else:
        print(f"\n⚠️ WARNING: {total_failed} tests failed.")
        return False

if __name__ == "__main__":
    run_phase2_verification()
