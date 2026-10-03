# VAPT Remediation Case Study: Broken Access Control in ASP.NET

## Disclaimer
This case study is sanitized and based on a representative enterprise web-application scenario.
No client data, source code, endpoints, credentials, screenshots, or confidential information is included.

## Objective
Assess and remediate a broken access-control scenario where a low-privilege user could attempt to access functionality intended for a higher-privilege user.

## Environment
- Application type: Enterprise employee self-service web application
- Technology: ASP.NET Framework 4.8, C#, SQL Server, IIS
- Testing tool: Burp Suite Community/Professional
- Test account types: Low-privilege and high-privilege authorized test accounts

## Risk
Broken access control can allow unauthorized viewing, modification, or submission of another user's data.
Potential business impact includes exposure of employee records, payroll-related information, or unauthorized workflow actions.

## Testing Method
1. Logged in with an authorized low-privilege test account.
2. Captured a valid request using Burp Suite Proxy.
3. Sent the request to Burp Repeater.
4. Modified only the object identifier or role-related request value in the authorized test environment.
5. Observed whether the server enforced authorization independently of the client request.

## Root Cause
Authorization depended partially on client-controlled values or UI-level restrictions.
The server did not consistently validate whether the authenticated user was permitted to access the requested resource.

## Remediation
- Enforced server-side authorization for every sensitive action.
- Derived user identity and role from the authenticated server-side session or claims, not client input.
- Validated ownership or permitted scope before read, insert, update, or delete operations.
- Applied least-privilege role checks at controller, service, and data-access layers where appropriate.
- Added negative test cases for cross-user and cross-role access.

## Secure Design Example
Do not trust a user ID or role supplied by the browser.
Obtain the authenticated identity from the server-side security context and verify authorization before executing the operation.

## Validation
1. Retested the same request after deployment in the approved test environment.
2. Confirmed that unauthorized requests returned an appropriate access-denied response.
3. Tested multiple low-privilege and high-privilege account combinations.
4. Verified that valid authorized functionality continued to work.

## Key Lesson
UI restrictions are not authorization controls. Sensitive actions must be authorized on the server for every request.
