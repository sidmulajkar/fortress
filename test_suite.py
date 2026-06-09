#!/usr/bin/env python3
"""
FORTRESS ZERO — Automated Test Suite
Tests every format, locale, entity detection, and edge case.
Validates output correctness for AI tool usage.
"""

import json
import re
import sys
from typing import List, Dict, Any, Tuple

# ============================================================
# TEST RESULTS TRACKER
# ============================================================

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def record(self, name: str, passed: bool, message: str = ""):
        if passed:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            self.errors.append(f"FAIL: {name} - {message}")
            print(f"  ✗ {name}: {message}")

    def summary(self):
        print("\n" + "=" * 60)
        print(f"RESULTS: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print("\nFailures:")
            for e in self.errors:
                print(f"  - {e}")
        return self.failed == 0


# ============================================================
# VALIDATORS (Match JS implementation)
# ============================================================

def validate_aadhaar(digits: str) -> bool:
    """Verhoeff algorithm for Aadhaar validation"""
    if len(digits) != 12 or not digits.isdigit():
        return False

    V = {
        'd': [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],
              [3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],
              [6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],
              [9,8,7,6,5,4,3,2,1,0]],
        'p': [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[2,7,6,0,4,9,3,1,8,5],
              [3,4,0,7,6,5,9,2,1,8],[4,2,8,6,7,0,9,3,5,1],[5,8,3,9,0,4,6,7,2,1],
              [6,3,9,5,8,1,0,4,7,2],[7,0,1,2,3,4,5,6,8,9],[8,9,2,1,5,7,4,6,0,3],
              [9,6,5,4,1,2,7,8,3,0]]
    }

    c = 0
    for i, ch in enumerate(digits):
        c = V['d'][c][V['p'][i % 8][int(ch)]]
    return c == 0

def validate_luhn(num: str) -> bool:
    """Luhn algorithm for credit cards"""
    d = re.sub(r'\D', '', num)
    if len(d) < 13 or len(d) > 19:
        return False
    total = 0
    is_even = False
    for c in reversed(d):
        n = int(c)
        if is_even:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        is_even = not is_even
    return total % 10 == 0

def validate_iban(iban: str) -> bool:
    """IBAN validation (mod 97)"""
    clean = iban.replace(' ', '').upper()
    if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$', clean):
        return False
    rearranged = clean[4:] + clean[:4]
    numeric = ''
    for c in rearranged:
        if 'A' <= c <= 'Z':
            numeric += str(ord(c) - 55)
        else:
            numeric += c
    mod = 0
    for d in numeric:
        mod = (mod * 10 + int(d)) % 97
    return mod == 1

# ============================================================
# PATTERNS (Match JS implementation)
# ============================================================

PATTERNS = {
    'in': {
        'aadhaar': r'\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b',
        'pan': r'\b([A-Z]{3}[PCJHFATBLG][A-Z]\d{4}[A-Z])\b',
        'email': r'\b([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\b',
        'apiKey': r'\b(sk-[A-Za-z0-9_\-]{10,})\b',
        'jwt': r'\b(eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\b'
    },
    'eu': {
        'email': r'\b([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\b',
        'iban': r'\b([A-Z]{2}\d{2}[\s]?[A-Z0-9]{4}[\s]?[A-Z0-9]{4}[\s]?[A-Z0-9]{4}[\s]?[A-Z0-9]{4}[\s]?[A-Z0-9]{2,4})\b',
        'vat': r'\b([A-Z]{2}[\s]?\d{2}[\s]?[A-Z0-9]{1,9})\b',
        'ip': r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b',
        'phone': r'(\+\d[\s\-\d]{7,})',  # Fixed: + followed by 7+ chars
        'passport': r'\b([A-Z]{1,2}[0-9]{6,9})\b',
        'ssn': r'\b(\d{3}[\s\-]?\d{2}[\s\-]?\d{4})\b',
        'uuid': r'\b([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\b',
        'jwt': r'\b(eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\b',
        'creditcard': r'\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b'
    },
    'us': {
        'email': r'\b([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})\b',
        'ssn': r'\b(\d{3}[\s\-]?\d{2}[\s\-]?\d{4})\b',
        'ip': r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b',
        'phone': r'\b(\+1[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{4})\b',
        'creditcard': r'\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b',
        'uuid': r'\b([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\b',
        'zip': r'\b(\d{5}([\-]\d{4})?)\b'
    }
}

# ============================================================
# FORMAT DETECTION
# ============================================================

def detect_format(text: str) -> str:
    """Match JS detectFormat function"""
    trimmed = text.strip()

    if (trimmed.startswith('{') and trimmed.endswith('}')) or \
       (trimmed.startswith('[') and trimmed.endswith(']')):
        try:
            json.loads(trimmed)
            return 'json'
        except:
            pass

    if re.search(r'INSERT\s+INTO', trimmed, re.I) and re.search(r'VALUES', trimmed, re.I):
        return 'sql'

    lines = [l for l in trimmed.split('\n') if l.strip()]
    if len(lines) >= 2:
        first_count = len(lines[0].split(','))
        if all(len(l.split(',')) == first_count for l in lines[1:]):
            return 'csv'

    if re.match(r'\d{4}-\d{2}-\d{2}', trimmed):
        return 'log'

    return 'prose'

# ============================================================
# FORMAT CONVERSION
# ============================================================

def convert_to_json(text: str, format: str) -> str:
    """Convert various formats to JSON (match JS convertToJSON)"""
    trimmed = text.strip()

    if format == 'json':
        try:
            return json.dumps(json.loads(trimmed), indent=2)
        except:
            return trimmed

    if format == 'csv':
        lines = [l for l in trimmed.split('\n') if l.strip()]
        if len(lines) < 2:
            return json.dumps({'raw': trimmed})
        headers = [h.strip().replace('"', '').replace("'", '') for h in lines[0].split(',')]
        records = []
        for line in lines[1:]:
            vals = [v.strip().replace('"', '').replace("'", '') for v in line.split(',')]
            records.append(dict(zip(headers, vals)))
        return json.dumps({'records': records}, indent=2)

    if format == 'sql':
        records = []
        for match in re.finditer(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)', trimmed, re.I):
            table, cols, vals = match.groups()
            cols = [c.strip() for c in cols.split(',')]
            vals = [v.strip().strip("'").strip('"') for v in vals.split(',')]
            record = {'_table': table}
            record.update(dict(zip(cols, vals)))
            records.append(record)
        if records:
            return json.dumps({'records': records}, indent=2)
        return json.dumps({'raw': trimmed})

    if format == 'log':
        lines = [l for l in trimmed.split('\n') if l.strip()]
        logs = [{'raw': line, 'message': line} for line in lines]
        return json.dumps({'logs': logs}, indent=2)

    return json.dumps({'text': trimmed}, indent=2)

# ============================================================
# SANITIZE (Python simulation of JS sanitize)
# ============================================================

def sanitize(text: str, locale: str) -> Dict[str, Any]:
    """Python simulation of JS sanitize function"""
    if not text or not text.strip():
        return {'text': '', 'changes': [], 'format': 'prose', 'typesFound': []}

    patterns = PATTERNS.get(locale, PATTERNS['in'])
    detected_format = detect_format(text)

    # Convert to JSON
    json_text = convert_to_json(text, detected_format)
    changes = []

    # First pass: find all matches in ORIGINAL text and check code context
    matches_to_skip = set()
    for entity_type, pattern in patterns.items():
        regex = re.compile(pattern)
        for match in regex.finditer(text):
            orig = match.group(1) if match.group(1) else match.group(0)
            window = text[max(0, match.start() - 5):match.start()]
            if re.search(r'=\s*["\']', window):
                matches_to_skip.add((orig, match.start()))

    # Second pass: process JSON, skipping code context matches
    for entity_type, pattern in patterns.items():
        regex = re.compile(pattern)
        for match in regex.finditer(json_text):
            orig = match.group(1) if match.group(1) else match.group(0)
            if (orig, match.start()) in matches_to_skip:
                continue

            # Skip localhost/dev ports
            if re.search(r'localhost|127\.0\.0\.1|:\d{3,5}', orig):
                continue

            # Validate specific types
            if entity_type == 'aadhaar':
                digits = re.sub(r'\D', '', orig)
                if not validate_aadhaar(digits):
                    continue

            if entity_type == 'creditcard':
                if not validate_luhn(orig):
                    continue

            if entity_type == 'iban':
                if not validate_iban(orig):
                    continue

            # Generate synthetic (simplified - just mark as replaced)
            synthetic = f'[{entity_type.upper()}_REPLACED]'

            if synthetic != orig:
                changes.append({
                    'type': entity_type,
                    'orig': orig,
                    'synthetic': synthetic,
                    'index': match.start()
                })

    # Apply changes in descending index order
    changes.sort(key=lambda x: x['index'], reverse=True)
    result = json_text
    for c in changes:
        result = result[:c['index']] + c['synthetic'] + result[c['index'] + len(c['orig']):]

    types_found = list(set(c['type'] for c in changes))

    return {
        'text': result,
        'changes': changes,
        'format': detected_format,
        'typesFound': types_found
    }

# ============================================================
# TESTS
# ============================================================

def test_validators(results: TestResults):
    """Test validation functions"""
    print("\n--- VALIDATORS ---")

    # Aadhaar validation
    # Generate a valid Aadhaar
    test_aadhaars = [
        ('987610014325', True, 'Generated valid Aadhaar'),
        ('123456789012', False, 'Invalid Aadhaar (bad checksum)'),
        ('1234', False, 'Too short'),
        ('12345678901234', False, 'Too long'),
        ('abc123def456', False, 'Contains letters'),
    ]

    for aadhaar, expected, desc in test_aadhaars:
        result = validate_aadhaar(aadhaar)
        results.record(f"Aadhaar {desc}", result == expected)

    # Luhn validation
    luhn_tests = [
        ('4111111111111111', True, 'Valid Visa'),
        ('5500000000000004', True, 'Valid MC'),
        ('4111111111111112', False, 'Invalid checksum'),
        ('1234567890123456', False, 'Random number'),
    ]

    for num, expected, desc in luhn_tests:
        result = validate_luhn(num)
        results.record(f"Luhn {desc}", result == expected)

    # IBAN validation
    iban_tests = [
        ('DE89370400440532013000', True, 'Valid German IBAN'),
        ('GB82WEST12345698765432', True, 'Valid UK IBAN'),
        ('FR7630006000011234567890189', True, 'Valid French IBAN'),
        ('DE89370400440532013001', False, 'Invalid checksum'),
        ('1234567890', False, 'Too short'),
    ]

    for iban, expected, desc in iban_tests:
        result = validate_iban(iban)
        results.record(f"IBAN {desc}", result == expected)

def test_format_detection(results: TestResults):
    """Test format detection"""
    print("\n--- FORMAT DETECTION ---")

    tests = [
        ('{"name": "test"}', 'json', 'Simple JSON object'),
        ('[1, 2, 3]', 'json', 'JSON array'),
        ('name,aadhaar,email\nRajesh,987610014325,test@test.com', 'csv', 'CSV with headers'),
        ("INSERT INTO users (name) VALUES ('test')", 'sql', 'SQL INSERT'),
        ('2024-11-15T10:30:45 ERROR: test message', 'log', 'Log line with timestamp'),
        ('Plain text without structure', 'prose', 'Plain text'),
        ('  { "key": "value" }  ', 'json', 'JSON with whitespace'),
    ]

    for text, expected, desc in tests:
        result = detect_format(text)
        results.record(f"Format {desc}", result == expected, f"got {result}, expected {expected}")

def test_format_conversion(results: TestResults):
    """Test format to JSON conversion"""
    print("\n--- FORMAT CONVERSION ---")

    # JSON
    json_input = '{"name": "Rajesh", "aadhaar": "987610014325"}'
    converted = convert_to_json(json_input, 'json')
    try:
        parsed = json.loads(converted)
        results.record("JSON conversion", parsed['name'] == 'Rajesh')
    except:
        results.record("JSON conversion", False, "Failed to parse")

    # CSV
    csv_input = 'name,email\na@b.com,c@d.com'
    converted = convert_to_json(csv_input, 'csv')
    try:
        parsed = json.loads(converted)
        results.record("CSV conversion", 'records' in parsed and len(parsed['records']) == 1)
    except:
        results.record("CSV conversion", False, "Failed to parse")

    # SQL
    sql_input = "INSERT INTO users (name, email) VALUES ('Rajesh', 'rajesh@test.com')"
    converted = convert_to_json(sql_input, 'sql')
    try:
        parsed = json.loads(converted)
        results.record("SQL conversion", 'records' in parsed and parsed['records'][0]['_table'] == 'users')
    except:
        results.record("SQL conversion", False, "Failed to parse")

    # Log
    log_input = '2024-11-15 ERROR: test message\n2024-11-15 INFO: another'
    converted = convert_to_json(log_input, 'log')
    try:
        parsed = json.loads(converted)
        results.record("Log conversion", 'logs' in parsed and len(parsed['logs']) == 2)
    except:
        results.record("Log conversion", False, "Failed to parse")

def test_entity_detection(results: TestResults):
    """Test entity detection per locale"""
    print("\n--- ENTITY DETECTION ---")

    # India locale
    india_tests = [
        ('in', '987610014325', 'aadhaar', 'Valid Aadhaar'),
        ('in', 'ABCPK1234F', 'pan', 'Valid PAN'),
        ('in', 'test@example.com', 'email', 'Valid Email'),
        ('in', 'sk-abcdefghij1234567890', 'apiKey', 'Valid API Key'),
        ('in', 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature', 'jwt', 'Valid JWT'),
    ]

    for locale, text, expected_type, desc in india_tests:
        result = sanitize(text, locale)
        types_found = result['typesFound']
        results.record(f"India {desc}", expected_type in types_found, f"found: {types_found}")

    # EU locale
    eu_tests = [
        ('eu', 'DE89370400440532013000', 'iban', 'Valid IBAN'),
        ('eu', 'DE123456789', 'vat', 'Valid VAT ID'),
        ('eu', '192.168.1.1', 'ip', 'Valid IP'),
        ('eu', '+49 89 12345678', 'phone', 'Valid Phone'),
        ('eu', 'C1234567', 'passport', 'Valid Passport'),
        ('eu', '240-52-1234', 'ssn', 'Valid SSN'),
        ('eu', '550e8400-e29b-41d4-a716-446655440000', 'uuid', 'Valid UUID'),
        ('eu', '4111111111111111', 'creditcard', 'Valid Credit Card'),
    ]

    for locale, text, expected_type, desc in eu_tests:
        result = sanitize(text, locale)
        types_found = result['typesFound']
        results.record(f"EU {desc}", expected_type in types_found, f"found: {types_found}")

def test_edge_cases(results: TestResults):
    """Test edge cases"""
    print("\n--- EDGE CASES ---")

    # Empty input
    result = sanitize('', 'in')
    results.record("Empty input", result['text'] == '' and len(result['changes']) == 0)

    # Whitespace only
    result = sanitize('   \n\t  ', 'in')
    results.record("Whitespace only", result['text'] == '')

    # No PII
    result = sanitize('Hello world, this is normal text', 'in')
    results.record("No PII text", len(result['changes']) == 0)

    # JSON with no PII
    result = sanitize('{"key": "value", "count": 123}', 'in')
    results.record("JSON with no PII", len(result['changes']) == 0)

    # Multiple PII of same type
    result = sanitize('a@b.com and c@d.com and e@f.com', 'in')
    results.record("Multiple emails", len(result['changes']) == 3)

    # JSON with nested PII
    json_nested = '{"user": {"email": "test@test.com"}, "admin": {"email": "admin@test.com"}}'
    result = sanitize(json_nested, 'in')
    results.record("Nested JSON PII", len(result['changes']) == 2)

    # SQL with multiple inserts
    sql_multi = "INSERT INTO t (a) VALUES ('x'); INSERT INTO t (a) VALUES ('y')"
    result = sanitize(sql_multi, 'in')
    results.record("Multiple SQL inserts", len(result['changes']) == 0)  # No actual PII

    # CSV with special chars in values
    csv_special = 'name,email\n"Rajesh, Kumar","test@test.com"'
    result = sanitize(csv_special, 'in')
    results.record("CSV with quoted values", 'email' in result['typesFound'])

    # Long random string (no false positives)
    long_random = 'a' * 1000 + 'b' * 1000
    result = sanitize(long_random, 'in')
    results.record("Long random string", len(result['changes']) == 0)

    # Code context (should skip after =)
    code_context = 'const apiKey = "sk-abcdefghij1234567890";'
    result = sanitize(code_context, 'in')
    results.record("Code context skip", 'apiKey' not in result['typesFound'])

    # Localhost skip
    localhost = 'localhost:3000 or 127.0.0.1:5432'
    result = sanitize(localhost, 'in')
    results.record("Localhost skip", len(result['changes']) == 0)

def test_output_format_for_ai(results: TestResults):
    """Test that output is clean and usable for AI tools"""
    print("\n--- OUTPUT FORMAT FOR AI ---")

    # Test that output is valid JSON
    test_cases = [
        ('in', '{"user": {"aadhaar": "987610014325", "email": "test@test.com"}}'),
        ('eu', '{"iban": "DE89370400440532013000", "email": "test@test.com"}'),
        ('us', '{"ssn": "123-45-6789", "email": "test@test.com"}'),
    ]

    for locale, json_input in test_cases:
        result = sanitize(json_input, locale)
        # Output should be valid JSON
        try:
            parsed = json.loads(result['text'])
            results.record(f"Output valid JSON ({locale})", True)
        except json.JSONDecodeError as e:
            results.record(f"Output valid JSON ({locale})", False, str(e))

        # Changes should be reflected
        results.record(f"Changes detected ({locale})", len(result['changes']) > 0)

    # Test that output preserves structure
    structured = '{"name": "test", "data": {"email": "a@b.com"}}'
    result = sanitize(structured, 'in')
    try:
        parsed = json.loads(result['text'])
        # Should have same structure
        has_name = 'name' in parsed and parsed['name'] == 'test'
        has_data = 'data' in parsed
        results.record("Preserves JSON structure", has_name and has_data)
    except:
        results.record("Preserves JSON structure", False, "Invalid output")

def test_deterministic_validation(results: TestResults):
    """Test that the same input produces consistent validation"""
    print("\n--- DETERMINISTIC VALIDATION ---")

    # Same Aadhaar should always be detected
    aadhaar = '987610014325'
    for _ in range(5):
        result = sanitize(aadhaar, 'in')
        results.record("Aadhaar consistent detection", 'aadhaar' in result['typesFound'])

    # Same IBAN should always be detected
    iban = 'DE89370400440532013000'
    for _ in range(5):
        result = sanitize(iban, 'eu')
        results.record("IBAN consistent detection", 'iban' in result['typesFound'])

def test_false_positive_prevention(results: TestResults):
    """Test that common false positives are not flagged"""
    print("\n--- FALSE POSITIVE PREVENTION ---")

    # These should NOT be detected as PII
    safe_texts = [
        ('in', 'localhost:3000', 'Localhost address'),
        ('in', '127.0.0.1', 'Loopback address'),
        ('in', ':5000', 'Dev port'),
        ('in', 'apiKey = "sk-123"', 'Variable assignment'),
        ('in', 'const email = "test@test.com"', 'Const variable'),
        ('in', 'https://example.com', 'URL'),
        ('in', 'name,email', 'CSV headers'),
        ('in', 'SELECT * FROM', 'SQL keyword'),
        ('in', 'ERROR: something failed', 'Log level'),
        ('in', '{"key": "value"}', 'Random JSON'),
    ]

    for locale, text, desc in safe_texts:
        result = sanitize(text, locale)
        # All these should have 0 changes
        results.record(f"No false positive: {desc}", len(result['changes']) == 0,
                      f"got {len(result['changes'])} changes: {result['typesFound']}")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("FORTRESS ZERO — Automated Test Suite")
    print("=" * 60)

    results = TestResults()

    test_validators(results)
    test_format_detection(results)
    test_format_conversion(results)
    test_entity_detection(results)
    test_edge_cases(results)
    test_output_format_for_ai(results)
    test_deterministic_validation(results)
    test_false_positive_prevention(results)

    success = results.summary()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED - Review above")
    print("=" * 60)

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())