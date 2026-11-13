# BACKEND.md — Data and Server Standard

The backend exists to make the product correct, safe and fast. It is not a CRUD demo.

---

## 1. Data model rules

- PostgreSQL + Prisma. No raw SQL unless a measured query requires it.
- Every model: stable primary key (`cuid()` or UUID), `createdAt`, `updatedAt` when mutable.
- Money: integer, never float. Document whether the unit is Toman or Rial.
- Dates: `DateTime` in UTC; format in the UI for the user's timezone.
- Finite states use enums (`OrderStatus`, `Role`, `VariantKind`), not free strings.
- Explicit relations and indexes for every filter/sort/join path.
- Catalogue/history rows are deactivated (`isActive`) rather than deleted when referenced by orders.
- Unique constraints for slugs, SKUs, emails and any natural key.
- Use `@@index` on foreign keys and common list filters (`categoryId`, `createdAt`, `status`).
- Do not store derived display strings (formatted price, Persian date) in the database.

Example naming:

```prisma
model Product {
  id          String   @id @default(cuid())
  slug        String   @unique
  name        String
  price       Int
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  categoryId  String
  category    Category @relation(fields: [categoryId], references: [id])

  @@index([categoryId, isActive])
}
```

---

## 2. Migrations and seed

- Every schema change has a committed migration; never edit production by hand.
- Apply with `prisma migrate deploy` using the direct/unpooled URL.
- Seed is **idempotent**:
  - upsert by natural keys;
  - do not overwrite real user passwords on every run;
  - guard destructive resets behind an explicit env flag;
  - print a summary of created/updated rows.
- Demo seed data is clearly separated from real content and never published with public credentials.
- Back up before a destructive migration; test restore.

---

## 3. Server Actions and Route Handlers

Preferred shape:

```ts
type ActionResult<T> =
  | { ok: true; data: T }
  | { ok: false; message: string; fieldErrors?: Record<string, string[]> };
```

Rules:

- Parse input with Zod first. Never trust types from the client.
- Check authentication and authorization before reading/writing protected data.
- Return typed, human-readable errors; log the technical details server-side.
- Do not leak stack traces, SQL, secrets or internal IDs unnecessarily.
- Use `revalidatePath`/`revalidateTag` deliberately after mutations.
- Use a transaction when more than one row/table must change together.
- Price, discount, stock and role are always read from the database, never from the client payload.
- Idempotency key or unique constraint for checkout/order creation and webhook handling.
- Route Handlers are for external callbacks, file streaming and APIs consumed by non-UI clients.
  Normal UI mutations should be Server Actions unless there is a reason.

---

## 4. Authentication and authorization

- Password hashing: bcrypt cost ≥ 12 or argon2id with a modern parameter set.
- Session: signed JWT (`jose`) in an `httpOnly`, `Secure` (production), `SameSite=Lax` cookie.
- Never store the raw session token in `localStorage`.
- Session payload contains the user id and role; authorization is re-checked server-side.
- Logout invalidates the cookie and, where supported, the server-side session.
- Password reset:
  - random token, hashed at rest;
  - single use;
  - 30-minute expiry;
  - generic response whether or not the email exists;
  - never log the token in production.
- RBAC:
  - `CUSTOMER` can access only their own orders/addresses;
  - `ADMIN` routes and actions require an explicit role check, not only a hidden link.
- Rate-limit login, registration, password reset, contact and checkout.
- Production demo/admin accounts: rotate passwords, remove public credentials, or disable.

---

## 5. Validation

- Zod schemas live in `src/lib/validation.ts` (or feature-specific modules).
- Validate:
  - strings: trim, length, format;
  - numbers: range and integer where required;
  - IDs: existence and ownership;
  - enums: whitelist;
  - files: MIME, size, extension, ownership.
- Normalize Persian/Arabic characters for search, but store the original display text.
- Never use `as` to bypass a validation failure.
- Client validation is UX; server validation is the boundary.

---

## 6. Checkout and money

- Server recomputes line totals, discounts, shipping and grand total.
- Stock is checked and decremented in the same transaction as order creation.
- Order status transitions are explicit; invalid transitions are rejected.
- Payment gateway integration:
  - create a payment intent/order server-side;
  - verify the callback signature;
  - make callback handling idempotent;
  - never mark paid based on a client redirect alone.
- A demo checkout is clearly labelled and never claims a payment was taken.

---

## 7. Uploads and media

- Accepted MIME whitelist; verify magic bytes where possible.
- Max size enforced server-side and in the action body limit.
- Generate a safe storage key; never use the client filename as a path.
- Strip metadata if privacy matters.
- Serve with correct `Content-Type`, `Content-Disposition` and cache headers.
- Object storage or Postgres `BYTEA` for small files; never write to the source tree at runtime.
- Delete orphaned uploads when the owning record is removed.

---

## 8. Email and external services

- Email is optional at build time; the UI must still explain what happens if it is unavailable.
- Provider keys stay server-side.
- Password-reset tokens are never logged in production.
- External calls have a timeout, a clear failure path and no secret in logs.
- Webhooks verify signatures and are idempotent.
- If a side effect fails, the core database transaction should not silently claim success.

---

## 9. Observability and failure handling

- Log server errors with enough context (route, action, request id) but no secrets.
- Distinguish expected validation errors (4xx) from real faults (5xx).
- Add a health endpoint only if the platform needs it; do not expose internals.
- Keep a documented backup/restore procedure for production.
- For a single-instance demo, in-memory rate limiting is acceptable **only if documented**;
  for production scale, use Redis/Upstash or a shared limiter.

---

## 10. Backend quality gate

- [ ] migration committed and applied
- [ ] seed idempotent and safe for existing users
- [ ] every mutation validates input and authorization
- [ ] price/stock/role never trusted from the client
- [ ] multi-row writes use a transaction
- [ ] checkout/webhook idempotent
- [ ] auth cookie flags correct
- [ ] rate limits on public/auth endpoints
- [ ] no secret in client/logs/repo
- [ ] error states return useful messages
- [ ] indexes cover list/filter queries
- [ ] tests cover happy path + denied + invalid input
