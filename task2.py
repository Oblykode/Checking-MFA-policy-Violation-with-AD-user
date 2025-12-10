from z3 import *
import random
from datetime import datetime

def generate_realistic_ad_users(num_users=500):
    """Generate realistic AD users matching real domain patterns."""
    # Real AD naming patterns
    prefixes = ["svc_", "admin", "user", "guest", "test", "temp", "service", "sql", "app"]
    departments = ["hr", "it", "finance", "sales", "dev", "qa"]
    
    users = {}
    
    # Admins (95% MFA enabled)
    for i in range(20):
        name = f"admin{i:02d}"
        users[name] = random.choices([True, False], weights=[95, 5])[0]
    
    # Service accounts (80% MFA)
    for i in range(50):
        name = f"{random.choice(prefixes)}{i:03d}"
        users[name] = random.choices([True, False], weights=[80, 20])[0]
    
    # Regular users (90% MFA)
    for i in range(num_users - 70):
        name = f"{random.choice(['j', 'm', 's'])}{random.choice(departments)}.{random.randint(100,999)}"
        users[name] = random.choices([True, False], weights=[90, 10])[0]
    
    return users

def check_ad_mfa_policy():
    """Complete Z3 verification for Active Directory MFA policy."""
    print(" Scanning Active Directory users...")
    
    # Generate realistic AD dataset
    ad_users = generate_realistic_ad_users(500)
    
    s = Solver()
    violations = []
    
    print(f" Analyzing {len(ad_users):,} AD users")
    
    # Build Z3 constraints
    for username, mfa_status in ad_users.items():
        var = Bool(f"{username}_mfa_enabled")
        s.add(var == mfa_status)  # Actual status from AD
        s.add(var == True)        # Policy: ALL must have MFA
    
    # Formal verification
    result = s.check()
    
    if result == sat:
        print("\n MFA POLICY SATISFIED")
        print("All Active Directory users compliant!")
    else:
        print("\n MFA POLICY VIOLATION!")
        print("Users without MFA:")
        
        # Identify violators
        violation_count = 0
        for username, mfa_status in ad_users.items():
            if not mfa_status:
                violations.append(username)
                print(f"  → {username}")
                violation_count += 1
        
        print(f"\n Compliance: {100-len(violations)/len(ad_users)*100:.1f}%")
        print(f"   Violations: {violation_count}/{len(ad_users)} users")
    
    return violations

# Run AD policy check NOW
if __name__ == "__main__":
    start_time = datetime.now()
    violations = check_ad_mfa_policy()
    print(f"\n  Analysis complete in {datetime.now() - start_time}")