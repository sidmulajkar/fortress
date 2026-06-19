# 🛡️ Fortress Zero — Stop PII Leaks to AI Tools Before They Happen

**Stop pasting real customer data into ChatGPT.** Fortress Zero sanitizes Aadhaar, PAN, emails, API keys, and 15+ PII types locally—before they hit your clipboard.

[![Phase 0 Live](https://img.shields.io/badge/Status-Phase%200%20Live-brightgreen)](https://github.com/sidmulajkar/fortress)
[![Client-Side Only](https://img.shields.io/badge/Data-100%25%20Client%20Side-blue)](https://github.com/sidmulajkar/fortress)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange)](https://github.com/sidmulajkar/fortress)

---

## 🚨 The Problem No One's Talking About

Your dev team pastes production data into AI tools **every day**.

- `curl` response with real Aadhaar numbers → ChatGPT
- SQL export with customer emails → Claude
- Log file with PAN cards → Cursor

**One paste = cross-border data transfer = potential DPDP/GDPR violation.**

The clipboard doesn't warn you. Your IDE doesn't stop you. But now Fortress Zero does.

Beyond PII, production logs carry **system fingerprints** that can uniquely identify infrastructure:
- AWS EC2 instance IDs, GPU UUIDs, and IAM roles from log metadata
- Kernel memory addresses and function offsets from crash dumps (`ffffffffa12bc3d0`, `nvidia_uvm+0x1a2f`)
- K8s pod names, container IDs, and cgroup paths
- MAC addresses and internal IP addresses

**A single log paste can reveal your entire infrastructure topology to an AI provider.**

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

**System Logs / DevOps**
- ✅ EC2 Instance IDs (`i-0a91bcf34d2e8a1c7`)
- ✅ GPU UUIDs (`GPU-3c2f1a9b-7d8e-4f12-9c44-0a91bcf34d2e`)
- ✅ IAM Role names (from ARN context)
- ✅ AWS Account IDs (from ARN context)
- ✅ Kernel memory addresses (`ffffffffa12bc3d0`)
- ✅ Kernel function offsets (`nvidia_uvm+0x1a2f`)
- ✅ Kernel taint flags (`Tainted: P O W E`)
- ✅ Container IDs, K8s Pod names, Hostnames
- ✅ MAC addresses, File paths, UUIDs

---

## ⚡ Try It Now

**[Live Playground →](https://sidmulajkar.com/fortress/playground.html)**

Or open `playground.html` directly in your browser.

```
1. Paste your data (JSON, CSV, SQL, logs, plain text)
2. Click Sanitize
3. Copy clean output
4. Paste into any AI tool — with reduced PII risk
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
| PII Patterns | ✅ 15+ types (India/EU/US) |
| System Log Patterns | ✅ AWS, GPU, Kernel, K8s, Container |
| Line-by-line Fallback | ✅ Unstructured log support |
| Waitlist | 🔄 Open |
| CLI (Phase 1) | 🔜 Planned |

---

## 🔮 What's Next (Phase 1)

- **CLI** — `fz clip`, `fz check`, `fz file`
- **VS Code Extension** — Inline diff panel
- **Attestation Log** — `~/.fortress/events.ndjson` for audits
- **Team Tiers** — ₹1,500/dev/month

**[Join Waitlist →](https://sidmulajkar.com/fortress/index.html)**

---

## 💡 Common Questions

**Q: Does this send my data anywhere?**
A: No. Zero network calls. Everything runs in your browser.

**Q: What's the difference between sanitization and anonymization?**
A: Sanitization (pseudonymization) replaces PII with synthetic tokens that can be reversed with the original mapping. Anonymization removes PII permanently. Synthetic ≠ anonymous under GDPR.

**Q: Can I use this for production logs?**
A: Yes. It's designed for exactly this use case—cleaning logs, exports, and data dumps before AI processing. Supports kernel panics, GPU crash traces, AWS/K8s infrastructure logs, nginx access logs, and raw terminal output (line-by-line fallback handles unstructured content).

**Q: What system fingerprints does it catch beyond PII?**
A: AWS EC2 instance IDs, GPU UUIDs, IAM role ARNs, kernel memory addresses (`0xffffffff*`), kernel function offsets (`+0x1a2f`), taint flags, K8s pod names, container IDs, and MAC addresses. These can uniquely identify infrastructure when combined—see the kernel panic section above.

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

---

**Legal Disclaimer:** Fortress Zero is a Technical and Organisational Measure (TOM) designed to support data protection workflows under DPDP, GDPR, and similar frameworks. It does not constitute legal advice, guarantee compliance, or replace the guidance of your appointed Data Protection Officer (DPO). Synthetic replacement is a form of pseudonymisation, not anonymisation — pseudonymised data remains personal data under DPDP Section 2(t) and GDPR Recital 26. Final legal interpretation of whether your processing is compliant rests with your organisation's DPO and legal counsel.