# OWASP Juice Shop — Web Application Security Assessment

**Course:** Cyber Security Fundamentals (CSF) — IA 2
**Institution:** K. J. Somaiya School of Engineering, Somaiya Vidyavihar University

## Team
| Member | Roll No | Focus area |
|--------|---------|------------|
| Nayanika Khote | 16014124026 | Injection, Cross-Site Scripting, Authentication |
| Gayatri Markale | 16014124036 | Broken Access Control, Security Misconfiguration, Data handling |

## What this repository contains
This is the **code / execution repository** for our security assessment of OWASP Juice
Shop. It documents the 13 vulnerabilities we exploited, the exact steps and payloads for
each, and how they map to the OWASP Top 10 (2025).

> **Note on methodology:** the assessment was performed **mainly through the web browser** —
> using the address bar and the browser Developer Tools (F12) Console, Network and Storage
> panels. No external proxy (such as Burp Suite) and no custom Python tooling were required.
> The only "code" involved is the attack payloads and a short JavaScript Console command,
> which are included inline in [`SOLUTIONS.md`](SOLUTIONS.md).

The detailed walkthrough of every challenge — steps, payloads and the Console snippet —
is in **[`SOLUTIONS.md`](SOLUTIONS.md)**.

(The written report and screenshots are submitted separately in the report document and
are not part of this repository.)

## Target environment
- OWASP Juice Shop **v20.2.0**, self-hosted via **npm** (Node.js v24.21.0) on `http://localhost:3000`
- Tools: web browser + DevTools (F12) only

### Run the target
```bash
git clone https://github.com/juice-shop/juice-shop.git --depth 1
cd juice-shop
npm install
npm run build:server   # if the server build was skipped during install
npm start              # open http://localhost:3000
```

## Challenges solved (13) and OWASP Top 10 (2025) mapping
| # | Challenge | OWASP 2025 | Owner |
|---|-----------|------------|:-----:|
| 1 | Score Board (discovery) | Recon / Miscellaneous | NK |
| 2 | DOM XSS | A05 Injection | NK |
| 3 | Login Admin (SQL Injection) | A05 Injection | NK |
| 4 | Reflected XSS | A05 Injection | NK |
| 5 | Password Strength | A07 Authentication Failures | NK |
| 6 | Bonus Payload (XSS) | A05 Injection | NK |
| 7 | Privacy Policy (awareness) | Transparency / Miscellaneous | NK |
| 8 | Confidential Document | A01 Broken Access Control | GM |
| 9 | Error Handling | A10 Mishandling of Exceptional Conditions | GM |
| 10 | Admin Section | A01 Broken Access Control | GM |
| 11 | View Basket (IDOR) | A01 Broken Access Control | GM |
| 12 | Deprecated Interface | A02 Security Misconfiguration | GM |
| 13 | Five-Star Feedback | A01 Broken Access Control | GM |

Coverage: 5 of the OWASP Top 10 (2025) categories, led by Broken Access Control and Injection.

## Disclaimer
All testing was performed on a **self-hosted, isolated instance** of OWASP Juice Shop for
educational purposes only, as part of a graded academic assignment. No live or third-party
system was targeted.
