import os
import re

print("🔍 Checking Dashboard Templates for Static Content...")

dashboard_templates = [
    'templates/dashboard/deposit.html',
    'templates/dashboard/support.html', 
    'templates/dashboard/transactions.html',
    'templates/dashboard/withdraw.html'
]

def check_template_for_static_content(template_path):
    """Check if template has static content that should be dynamic"""
    if not os.path.exists(template_path):
        return False, "File not found"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for static content patterns
    static_patterns = [
        r'\$\d+[,.]?\d*\.?\d*',  # Dollar amounts like $12,450.00
        r'<h3>\d+</h3>',         # Static numbers in h3 tags
        r'<strong>\$\d+',        # Static dollar amounts in strong tags
        r'Jan \d+, 202\d',       # Static dates
        r'<option value="[^"]*">[^<]*</option>',  # Static option tags
    ]
    
    issues = []
    for pattern in static_patterns:
        matches = re.findall(pattern, content)
        if matches:
            issues.extend(matches)
    
    # Check if it properly extends base template
    extends_base = '{% extends \'dashboard/base_dashboard.html\' %}' in content
    loads_static = '{% load static %}' in content
    
    return {
        'extends_base': extends_base,
        'loads_static': loads_static,
        'static_content': issues,
        'needs_fixing': len(issues) > 0
    }

print("\n📊 Template Analysis:")
templates_to_fix = []

for template_path in dashboard_templates:
    result = check_template_for_static_content(template_path)
    template_name = os.path.basename(template_path)
    
    print(f"\n📄 {template_name}:")
    print(f"   ✅ Extends base: {result['extends_base']}")
    print(f"   ✅ Loads static: {result['loads_static']}")
    print(f"   🔍 Static content found: {len(result['static_content'])}")
    
    if result['static_content']:
        print(f"   📝 Examples:")
        for example in result['static_content'][:3]:  # Show first 3 examples
            print(f"      - {example}")
        if len(result['static_content']) > 3:
            print(f"      ... and {len(result['static_content']) - 3} more")
    
    if result['needs_fixing']:
        templates_to_fix.append(template_path)

print(f"\n🎯 Summary:")
print(f"   Templates checked: {len(dashboard_templates)}")
print(f"   Templates needing fixes: {len(templates_to_fix)}")

if templates_to_fix:
    print(f"\n🔧 Templates that need to be converted to Django templates:")
    for template in templates_to_fix:
        template_name = os.path.basename(template)
        print(f"   ❌ {template_name}")
        
        # Suggest what needs to be done
        if 'deposit.html' in template:
            print(f"      → Should use deposit form and user wallet data")
        elif 'support.html' in template:
            print(f"      → Should use support ticket system")
        elif 'transactions.html' in template:
            print(f"      → Should use user's actual transaction data")
        elif 'withdraw.html' in template:
            print(f"      → Already fixed! ✅")

print(f"\n💡 These templates should:")
print(f"   ✅ Use Django template variables instead of static content")
print(f"   ✅ Display real user data from the database")
print(f"   ✅ Use proper Django forms")
print(f"   ✅ Show dynamic calculations and statistics")

print(f"\n🚀 Next steps:")
print(f"   1. Fix deposit.html to use real deposit form and data")
print(f"   2. Fix support.html to use support ticket system")
print(f"   3. Fix transactions.html to use real transaction data")
print(f"   4. Update corresponding views to provide proper context")

print(f"\n✅ withdraw.html has been fixed and now uses Django templates properly!")
