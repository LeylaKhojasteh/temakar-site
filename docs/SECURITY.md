# SECURITY.md — Security Baseline

Security is a boundary discipline. The UI hiding a button is never authorization.

---

## 1. Secrets and environment

- All secrets live in environment variables, never in the repository or client bundle.
- Validate required variables at boot; fail fast with a clear message.
- `.env.example` lists every key with safe placeholder values.
- `.env*`, `.vercel`, local databases and credentials are git-ignored.
- Rotate secrets after accidental exposure; removing the commit is not enough.
- Never print tokens, passwords, database URLs or reset links in production logs.

---

## 2. Authentication

- Passwords hashed with bcrypt (cost ≥ 12) or argon2id.
- Minimum password policy enforced server-side; no maximum that blocks passphrases.
- Session cookie: `httpOnly`, `Secure` in production, `SameSite=Lax`, bounded lifetime.
- JWT/session signing secret ≥ 32 random bytes.
- Logout clears the cookie; server-side revocation where the design supports it.
- Password reset:
  - random, hashed at rest, single-use, expiring;
  - generic response to avoid account enumeration;
  - rate-limited;
  - email provider failure is surfaced honestly.
- Login/registration rate-limited by IP and account.
- No public demo credentials in production.
- Consider optional MFA for admin accounts on high-risk products.

---

## 3. Authorization

- Role checks happen in every protected page, action and route handler.
- Customers can only read/write their own orders and addresses.
- Admin mutations require an explicit `ADMIN` check, not a hidden link.
- Object-level authorization: verify ownership, not only login.
- Never trust an ID from the client without checking that it belongs to the caller.

---

## 4. Input and output

- Zod validation at every server boundary.
- Whitelist enums and formats; reject unknown fields where practical.
- Parameterized queries via Prisma; no string-concatenated SQL.
- Escape/encode user content in HTML; avoid `dangerouslySetInnerHTML` unless sanitized.
- Validate URL redirects (`next`, return URLs) to same-origin paths.
- File uploads: MIME whitelist, size limit, safe storage key, ownership check.
- Rate-limit public forms; honeypot/time trap as a secondary layer.

---

## 5. Headers and transport

In production, set at minimum:

- `Strict-Transport-Security`
- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `X-Frame-Options` / `frame-ancestors`
- `Cross-Origin-Opener-Policy`
- `Cross-Origin-Resource-Policy`
- `Permissions-Policy`

CSP should avoid `unsafe-inline` for scripts where feasible. If a framework requires it,
document why and keep the policy narrow. Do not enable `unsafe-eval` for convenience.

---

## 6. Cookies and sessions

- `httpOnly` always; `Secure` in production; `SameSite=Lax` unless a cross-site flow requires otherwise.
- Session lifetime bounded; refresh policy documented.
- CSRF: Server Actions provide protection in Next.js, but verify your framework version and
  any custom Route Handler. Do not expose state-changing GET endpoints.

---

## 7. Database

- Least-privilege database user for the app; migrations use a separate/direct connection.
- Backups enabled and restore tested.
- No production database in local development.
- No secrets in seed scripts.
- Destructive migrations reviewed and backed up.
- Connection pooling configured for serverless; avoid connection exhaustion.

---

## 8. Dependencies and supply chain

- Lockfile committed.
- `npm audit` reviewed regularly; critical issues fixed promptly.
- Avoid packages with unknown maintenance for auth/crypto/payment.
- Pin major versions; read release notes before upgrades.
- Never run arbitrary install scripts without reviewing them.
- Review generated code and AI-generated dependencies before shipping.

---

## 9. Logging and monitoring

- Log server errors with route/action context and request id; no secrets.
- Do not log full request bodies for auth/payment.
- Alert on repeated auth failures, 5xx spikes and checkout failures.
- Keep an audit trail for admin actions on orders/products where the product needs it.
- Do not expose internal errors or stack traces to users.

---

## 10. Deployment

- Preview and production separated.
- Production secrets only in production environment.
- No local `.env` uploaded.
- Security headers verified on the live URL.
- Domain/canonical URL correct; no mixed content.
- Demo accounts removed or rotated before launch.
- Rollback and restore plan documented.

---

## 11. Security review gate

- [ ] no secret in client/repo/logs
- [ ] auth cookie flags correct
- [ ] server-side RBAC and ownership checks
- [ ] input validated and output escaped
- [ ] rate limits on auth/contact/checkout
- [ ] upload validation
- [ ] headers/HSTS/CSP live
- [ ] dependency audit clean or documented
- [ ] production demo credentials removed
- [ ] backup/restore tested
- [ ] error messages do not leak internals
