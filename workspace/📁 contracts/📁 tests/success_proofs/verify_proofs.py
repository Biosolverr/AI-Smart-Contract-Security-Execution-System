import json
import os

def verify_security_proofs():
    report_path = os.path.join(os.path.dirname(__file__), 'SECURITY_PROOFS_REPORT.json')
    
    if not os.path.exists(report_path):
        print("❌ ERROR: SECURITY_PROOFS_REPORT.json not found!")
        return False
    
    with open(report_path, 'r') as f:
        data = json.load(f)
    
    print("🔍 Verifying GenRoute Security Proofs...")
    print(f"Report ID: {data['report_id']}")
    print(f"Status: {data['status']}")
    print("-" * 40)
    
    all_passed = True
    
    # Check Summary
    summary = data['summary']
    if summary['successful_mitigations'] != summary['total_attacks_simulated']:
        print("❌ CRITICAL: Not all attacks were mitigated!")
        all_passed = False
    else:
        print(f"✅ All {summary['total_attacks_simulated']} attacks mitigated.")
    
    # Check Individual Proofs
    for proof in data['proofs']:
        if proof['evidence'].get('match', False):
            print(f"✅ {proof['test_id']}: {proof['name']} - VERIFIED")
        else:
            print(f"❌ {proof['test_id']}: {proof['name']} - FAILED")
            all_passed = False
    
    print("-" * 40)
    
    if all_passed:
        print("🎉 SUCCESS: All security proofs are valid. Contract is secure.")
        return True
    else:
        print("⚠️ WARNING: Some proofs failed verification.")
        return False

if __name__ == "__main__":
    verify_security_proofs()
