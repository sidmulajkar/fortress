# 🛡️ Fortress Zero — Stop PII Leaks to AI Tools Before They Happen

**Stop pasting real customer data into ChatGPT.** Fortress Zero sanitizes Aadhaar, PAN, emails, API keys, and 15+ PII types locally—before they hit your clipboard.

[![Phase 0 Live](https://img.shields.io/badge/Status-Phase%200%20Live-brightgreen)](https://github.com)
[![Client-Side Only](https://img.shields.io/badge/Data-100%25%20Client%20Side-blue)](https://github.com)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange)](https://github.com)

---

## 🚨 The Problem No One's Talking About

Your dev team pastes production data into AI tools **every day**.

- `curl` response with real Aadhaar numbers → ChatGPT
- SQL export with customer emails → Claude
- Log file with PAN cards → Cursor

**One paste = cross-border data transfer = potential DPDP/GDPR violation.**

The clipboard doesn't warn you. Your IDE doesn't stop you. But now Fortress Zero does.

---

## ✨ Why Fortress Zero?

| Without Fortress Zero | With Fortress Zero |
|----------------------|-------------------|
| ❌ Paste real PII into AI | ✅ Paste sanitized data |
| ❌ DPDP/GDPR violation risk | ✅ Pseudonymized tokens |
| ❌ Data leaves your machine | ✅ Zero server calls |
| ❌ No audit trail | ✅ Local attestation ready |
| ❌ Hope for the best | ✅ Verify before paste |

---

## 🎯 What It Detects & Sanitizes

**India (DPDP Act)**
- ✅ Aadhaar (Verhoeff validated)
- ✅ PAN Card
- ✅ Email addresses
- ✅ Phone numbers (+91, international)
- ✅ API Keys (sk-...)
- ✅ JWT tokens

**EU (GDPR)**
- ✅ IBAN (checksum validated)
- ✅ VAT IDs
- ✅ Passport numbers
- ✅ SSN
- ✅ IP addresses
- ✅ Credit cards (Luhn validated)
- ✅ UUIDs

**US (CCPA)**
- ✅ SSN, ZIP codes, enhanced phone

**Universal**
- All of the above combined.

---

## ⚡ Try It Now

**[Live Playground →](https://fortress-zero.pages.dev/playground.html)**

Or open `playground.html` directly in your browser.

```
1. Paste your data (JSON, CSV, SQL, logs, plain text)
2. Click Sanitize
3. Copy clean output
4. Paste into any AI tool — safely
```

---

## 🔒 How It Works

```
Your Data → Fortress Zero (browser) → Sanitized Output → AI Tool
              ↓
         Zero network calls
         Zero data leaves you
```

1. **Detect** — Regex patterns with absolute string offsets
2. **Validate** — Mathematical checks (Verhoeff, Luhn, IBAN checksum)
3. **Generate** — Format-preserving synthetic tokens
4. **Output** — Diff view + one-click copy

**Nothing leaves your browser.** Run `view-source:playground.html` to verify.

---

## 📋 Compliance Ready

**DPDP Act 2023 (India)**
- Section 8(5): "Appropriate security safeguards"
- Section 16: Cross-border transfer restrictions
- Penalties up to ₹250 crore

**GDPR (EU)**
- Article 25: Data protection by design
- Article 32: Security of processing
- Synthetic = pseudonymisation

**CCPA (US)**
- Reasonable security measures
- Due diligence demonstration

*Fortress Zero helps you demonstrate due diligence. Consult your DPO for compliance guidance.*

---

## 🏗️ Architecture

```
┌────────────────────────────────────────┐
│              BROWSER                   │
│                                        │
│   INPUT ──▶ SANITIZE ──▶ SANITIZED     │
│   (raw)      ENGINE        (diff view) │
│                   │                    │
│                   └──▶ CLIPBOARD       │
│                              │         │
└──────────────────────────────┼─────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
    ┌─────────┐          ┌─────────┐          ┌─────────┐
    │ ChatGPT │          │ Claude  │          │ Cursor  │
    │ (safe)  │          │ (safe)  │          │ (safe)  │
    └─────────┘          └─────────┘          └─────────┘
```

---

## 📊 Phase 0 Status

| Component | Status |
|-----------|--------|
| Playground | ✅ Live |
| Landing Page | ✅ Live |
| Waitlist | 🔄 Open |
| CLI (Phase 1) | 🔜 Planned |

---

## 🔮 What's Next (Phase 1)

- **CLI** — `fz clip`, `fz check`, `fz file`
- **VS Code Extension** — Inline diff panel
- **Attestation Log** — `~/.fortress/events.ndjson` for audits
- **Team Tiers** — ₹1,500/dev/month

**[Join Waitlist →](https://fortress-zero.pages.dev/index.html)**

---

## 💡 Common Questions

**Q: Does this send my data anywhere?**
A: No. Zero network calls. Everything runs in your browser.

**Q: What's the difference between sanitization and anonymization?**
A: Sanitization (pseudonymization) replaces PII with synthetic tokens that can be reversed with the original mapping. Anonymization removes PII permanently. Synthetic ≠ anonymous under GDPR.

**Q: Can I use this for production logs?**
A: Yes. It's designed for exactly this use case—cleaning logs, exports, and data dumps before AI processing.

**Q: Does it preserve data format?**
A: Yes. Aadhaar stays 12 digits. IBAN passes checksum validation. AI reasoning stays intact.

---

## 📚 References

- [DPDP Act 2023](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf)
- [GDPR 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679)

---

## 🛠️ Tech Stack

Phase 0: **Vanilla HTML/CSS/JS** — Zero dependencies, zero build step.

---

<p align="center">
<strong>Stop leaking. Start sanitizing. Ship faster.</strong><br>
🛡️ Fortress Zero — Clipboard-first PII protection.
</p>