# API Security Testing Checklist

## Scope and authorization
- Confirm written authorization and test scope before testing.
- Identify API base URLs, environments, auth method, and approved test accounts.
- Do not test production systems without explicit approval.

## Authentication testing
- Check whether unauthenticated requests can access protected endpoints.
- Test expired, malformed, revoked, and missing tokens.
- Check whether sensitive tokens are unnecessarily returned in response bodies.
- Verify logout and token revocation behavior where applicable.

## Authorization and BOLA/IDOR
- Test whether one user can access another user's object by modifying IDs.
- Test read, create, update, and delete operations separately.
- Confirm server-side ownership and role validation.
- Verify that object identifiers are not treated as authorization proof.

## Input validation
- Test query parameters, request bodies, headers, and path parameters.
- Check for SQL injection, reflected input, mass assignment, and unexpected field handling.
- Validate server-side input validation and error behavior.

## Data exposure
- Check responses for passwords, tokens, internal paths, stack traces, PII, and excessive fields.
- Verify that errors do not expose internal implementation details.
- Confirm sensitive fields are excluded by default.

## Rate limiting
- Identify authentication, OTP, password-reset, search, and high-cost endpoints.
- Test approved request volumes safely.
- Verify response behavior, lockout/throttling controls, monitoring, and recovery behavior.

## CORS
- Check whether allowed origins are specific and trusted.
- Verify that wildcard origins are not used with credentialed requests.
- Review allowed methods, headers, and preflight responses.

## Reporting format
For each issue document:
- Title
- Severity and business impact
- Preconditions
- Reproduction steps
- Evidence
- Root cause
- Recommended remediation
- Retest result
