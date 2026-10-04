# Solutions — Steps, Payloads & Code

Detailed walkthrough of all 13 exploited challenges. **Everything here was done through
the web browser** (address bar + DevTools F12). No Burp Suite, no Python. The only code
used is the payloads below and one JavaScript Console command (challenge 11).

Format per challenge: **Vulnerability → Steps → Payload/Command → Impact → Fix.**

---

## Member A — Nayanika Khote (16014124026)
### Injection, Cross-Site Scripting & Authentication

### 1. Score Board (Recon)
- **Vulnerability:** A hidden progress page is reachable by anyone; it is not protected.
- **Steps:** Navigate directly to the Score Board route in the address bar.
- **Payload/URL:** `http://localhost:3000/#/score-board`
- **Impact:** Hiding a page in the UI is not a security control; it stays accessible.
- **Fix:** Protect sensitive routes with server-side authorization, not by hiding links.

### 2. DOM XSS (A05 Injection)
- **Vulnerability:** The search field writes user input into the page (DOM) without
  sanitisation, so injected HTML/JS executes.
- **Steps:** Type the payload into the search box (top-right magnifier) and press Enter.
- **Payload:**
  ```
  <iframe src="javascript:alert(`xss`)">
  ```
- **Impact:** Arbitrary JavaScript runs in a victim's browser (token theft, impersonation).
- **Fix:** Sanitise/encode output; use Angular sanitisation + a strict Content Security Policy.

### 3. Login Admin — SQL Injection (A05 Injection)
- **Vulnerability:** The login query concatenates input directly into SQL.
- **Steps:** On the Login page, put the payload in the **Email** field with any password.
- **Payload:** Email `' OR 1=1--`  |  Password `12345`
- **Impact:** Full authentication bypass — logs in as the administrator.
- **Fix:** Use parameterised queries / prepared statements; never concatenate SQL.

### 4. Reflected XSS (A05 Injection)
- **Vulnerability:** The order-tracking page reflects the URL `id` parameter without encoding.
- **Steps:** Log in, open order tracking, and put the payload in the `id` value in the URL.
- **Payload/URL:**
  ```
  http://localhost:3000/#/track-result?id=<iframe src="javascript:alert(`xss`)">
  ```
- **Impact:** A crafted link runs attacker JS in a victim's session.
- **Fix:** Context-aware output encoding of reflected parameters; CSP as defence in depth.

### 5. Password Strength (A07 Authentication Failures)
- **Vulnerability:** The admin account uses a weak, unchanged, well-known password.
- **Steps:** Log in with the real admin credentials (no injection).
- **Payload:** Email `admin@juice-sh.op`  |  Password `admin123`
- **Impact:** Trivial takeover of the highest-privilege account.
- **Fix:** Strong password policy, block common passwords, force changing defaults, add MFA.

### 6. Bonus Payload (A05 Injection)
- **Vulnerability:** Same unsanitised search sink, exploited with embedded media.
- **Steps:** Paste the payload into the search box and press Enter; a media player renders.
- **Payload:**
  ```
  <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>
  ```
- **Impact:** Confirms arbitrary active/embedded content can be injected via XSS.
- **Fix:** Same as DOM XSS — sanitise output; restrict embedded content via CSP.

### 7. Privacy Policy (Transparency / awareness)
- **Vulnerability:** Awareness task — confirms a privacy policy exists describing data use.
- **Steps:** Open the Privacy Policy page from the account menu.
- **Payload/URL:** `http://localhost:3000/#/privacy-security/privacy-policy`
- **Impact:** Not an exploit; relevant to data-protection transparency completeness.
- **Fix:** Keep privacy/data-handling disclosures accurate and current.

---

## Member B — Gayatri Markale (16014124036)
### Broken Access Control, Security Misconfiguration & Data Handling

### 8. Confidential Document (A01 Broken Access Control)
- **Vulnerability:** Sensitive files are served from a public directory with no access control.
- **Steps:** Browse the public `/ftp/` directory listing and open the confidential file.
- **Payload/URL:** `http://localhost:3000/ftp/`  then  `http://localhost:3000/ftp/acquisitions.md`
- **Impact:** Leakage of confidential internal documents to any anonymous user.
- **Fix:** Remove public access to internal dirs; disable directory listing; authorize every file.

### 9. Error Handling (A10 Mishandling of Exceptional Conditions)
- **Vulnerability:** An invalid request returns a raw error/stack trace instead of a clean message.
- **Steps:** Request an invalid API route.
- **Payload/URL:** `http://localhost:3000/rest/qwertz`
- **Impact:** Information disclosure — internal paths/versions aid further attacks.
- **Fix:** Generic user errors; log details server-side only; global error handler.

### 10. Admin Section (A01 Broken Access Control)
- **Vulnerability:** The admin area is reachable directly by URL; the route is not properly protected.
- **Steps:** While logged in, navigate directly to the administration route.
- **Payload/URL:** `http://localhost:3000/#/administration`
- **Impact:** Exposure of the admin dashboard (users, all feedback) and privileged actions.
- **Fix:** Enforce server-side role checks on every admin route and API.

### 11. View Basket — IDOR (A01 Broken Access Control)
- **Vulnerability:** The basket API returns any basket by id without checking ownership.
- **Steps:** Logged in, open DevTools (F12) -> Console, type `allow pasting` if prompted, run the command.
- **Command (JavaScript, run in the browser Console):**
  ```javascript
  fetch('/rest/basket/2', {
    headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
  })
    .then(r => r.json())
    .then(console.log);
  // change the number (1, 2, 3, ...) to read other users' baskets
  ```
- **Impact:** One user can read another user's cart/order data (IDOR generalises to any object).
- **Fix:** Enforce object-level authorization — verify resource owner == authenticated user.

### 12. Deprecated Interface (A02 Security Misconfiguration)
- **Vulnerability:** An old B2B file interface is still enabled; the backend accepts a file
  type the UI claims to reject.
- **Steps:** Create `test.xml` (content `<test>hello</test>`). On the complaint form, type a
  message and upload the XML file, then submit.
- **Payload/URL:** Upload `test.xml` at `http://localhost:3000/#/complain`
- **Impact:** Deprecated interfaces widen the attack surface (e.g. XML-based attacks).
- **Fix:** Decommission unused interfaces; enforce server-side file-type allow-lists.

### 13. Five-Star Feedback (A01 Broken Access Control)
- **Vulnerability:** The admin capability can silently delete all top-rated feedback,
  manipulating data integrity.
- **Steps:** Using admin access from #10, open the admin panel and delete every 5-star row
  in the Customer Feedback table.
- **Payload/URL:** `http://localhost:3000/#/administration` -> Customer Feedback -> delete 5-star rows
- **Impact:** Reviews can be censored/manipulated by whoever reaches the admin function.
- **Fix:** Restrict, log and audit destructive admin actions; apply least privilege.
