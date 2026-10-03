ASP.NET Secure Coding Examples
This repository contains original, simplified ASP.NET / C# examples showing common web-application security issues and secure alternatives.

Purpose: Demonstrate secure coding knowledge for Application Security (AppSec) roles.
Scope: Educational examples only. Do not use insecure patterns in production.

Included Examples

| # | Security Issue                | Insecure Pattern                  | Secure Pattern                                              |
| - | ----------------------------- | --------------------------------- | ----------------------------------------------------------- |
| 1 | SQL Injection                 | String-concatenated SQL query     | Parameterized SQL command                                   |
| 2 | Cross-Site Scripting (XSS)    | Direct HTML output of user input  | Context-aware output encoding                               |
| 3 | Broken Access Control / IDOR  | Trusting client-supplied user ID  | Server-side identity and ownership validation               |
| 4 | Sensitive Error Exposure      | Returning exception details       | Generic error response plus server-side logging             |
| 5 | Insecure Cookie Configuration | Default cookie settings           | Secure, HttpOnly, SameSite cookie configuration             |
| 6 | Missing Rate Limiting         | Unlimited authentication attempts | IIS IP/domain restrictions and application-level throttling |

1. SQL Injection
Insecure pattern
csharp
// DO NOT USE IN PRODUCTION
public DataTable GetEmployee(string employeeId)
{
    string query = "SELECT * FROM Employees WHERE EmployeeId = '" + employeeId + "'";

    using (SqlConnection connection = new SqlConnection(connectionString))
    using (SqlCommand command = new SqlCommand(query, connection))
    {
        SqlDataAdapter adapter = new SqlDataAdapter(command);
        DataTable result = new DataTable();
        adapter.Fill(result);
        return result;
    }
}
Why it is insecure
If employeeId contains SQL syntax, an attacker may change the meaning of the query.
For example, malicious input could terminate the expected condition and append another query or condition.

Secure pattern
csharp
public DataTable GetEmployee(int employeeId)
{
    const string query = "SELECT EmployeeId, FullName, Email FROM Employees WHERE EmployeeId = @EmployeeId";

    using (SqlConnection connection = new SqlConnection(connectionString))
    using (SqlCommand command = new SqlCommand(query, connection))
    {
        command.Parameters.Add("@EmployeeId", SqlDbType.Int).Value = employeeId;

        SqlDataAdapter adapter = new SqlDataAdapter(command);
        DataTable result = new DataTable();
        adapter.Fill(result);
        return result;
    }
}
Secure design notes
Use strongly typed parameters instead of concatenating user input into SQL.

Use stored procedures with parameters only if parameters are used correctly; a stored procedure that concatenates input internally is still vulnerable.

Give the application database account only the minimum required permissions.

Avoid exposing detailed database errors to users.

2. Cross-Site Scripting (XSS)
Insecure pattern
csharp
// DO NOT USE IN PRODUCTION
public string RenderComment(string userComment)
{
    return "<div>" + userComment + "</div>";
}
Why it is insecure
If userComment contains HTML or JavaScript, the browser may execute it in another user's session.

Secure pattern
csharp
using System.Web;
using System.Web.Security.AntiXss;

public string RenderComment(string userComment)
{
    string encodedComment = AntiXssEncoder.HtmlEncode(userComment, true);
    return "<div>" + encodedComment + "</div>";
}
Secure design notes
Encode output according to its destination: HTML body, attribute, JavaScript, URL, or CSS.

Treat all user-controlled data as untrusted, even if it came from your own database.

Use a strong Content Security Policy (CSP) as an additional defense-in-depth control.

Avoid using HttpUtility.HtmlEncode alone for all contexts; use context-appropriate encoding.

3. Broken Access Control / IDOR
Insecure pattern
csharp
// DO NOT USE IN PRODUCTION
public IHttpActionResult GetLeaveRequest(int requestId)
{
    // The server trusts the request ID without checking ownership.
    var leaveRequest = leaveRepository.GetLeaveRequestById(requestId);

    if (leaveRequest == null)
    {
        return NotFound();
    }

    return Ok(leaveRequest);
}
Why it is insecure
A low-privilege user may change requestId and access another employee's leave request.

Secure pattern
csharp
public IHttpActionResult GetLeaveRequest(int requestId)
{
    // Get identity from the authenticated server-side context, not from the request body.
    int currentEmployeeId = GetAuthenticatedEmployeeId();

    var leaveRequest = leaveRepository.GetLeaveRequestById(requestId);

    if (leaveRequest == null)
    {
        return NotFound();
    }

    // Enforce ownership or role-based authorization before returning data.
    bool isOwner = leaveRequest.EmployeeId == currentEmployeeId;
    bool isAuthorizedApprover = User.IsInRole("LeaveApprover");

    if (!isOwner && !isAuthorizedApprover)
    {
        return StatusCode(HttpStatusCode.Forbidden);
    }

    return Ok(leaveRequest);
}
Secure design notes
Never trust a user ID, role, or permission flag sent from the browser.

Obtain the authenticated identity from the server-side session, claims, or security context.

Validate authorization for every sensitive read, create, update, and delete operation.

Test both positive and negative cases: valid owner, non-owner, and different role combinations.

4. Sensitive Error Exposure
Insecure pattern
csharp
// DO NOT USE IN PRODUCTION
public IHttpActionResult ProcessPayment(PaymentRequest request)
{
    try
    {
        paymentService.Process(request);
        return Ok();
    }
    catch (Exception ex)
    {
        // Exposes internal details to the caller.
        return InternalServerError(ex);
    }
}
Why it is insecure
Stack traces, SQL errors, file paths, and internal exception details can help an attacker understand the application.

Secure pattern
csharp
private static readonly ILogger Logger = LogManager.GetCurrentClassLogger();

public IHttpActionResult ProcessPayment(PaymentRequest request)
{
    try
    {
        paymentService.Process(request);
        return Ok();
    }
    catch (Exception ex)
    {
        Logger.Error(ex, "Payment processing failed.");

        // Return a generic response to the client.
        return Content(
            HttpStatusCode.InternalServerError,
            new { message = "Unable to process the request. Please try again later." });
    }
}
Secure design notes
Log detailed errors on the server, but return only generic messages to users.

Avoid logging sensitive data such as passwords, tokens, card numbers, or full personal data.

Disable detailed ASP.NET error pages in production.

Monitor logs for repeated failures, unusual patterns, and suspicious activity.

5. Insecure Cookie Configuration
Insecure pattern
csharp
// DO NOT USE IN PRODUCTION
var cookie = new HttpCookie("SessionId", sessionId)
{
    Path = "/"
};

Response.Cookies.Add(cookie);
Why it is insecure
Without appropriate flags, the cookie may be exposed to JavaScript or sent over insecure connections, increasing session-hijacking risk.

Secure pattern
csharp
var cookie = new HttpCookie("SessionId", sessionId)
{
    HttpOnly = true,
    Secure = true,
    SameSite = SameSiteMode.Lax,
    Path = "/"
};

Response.Cookies.Add(cookie);
Secure design notes
Use Secure so the cookie is sent only over HTTPS.

Use HttpOnly to reduce JavaScript access to session cookies.

Use an appropriate SameSite policy based on your application's cross-site requirements.

Regenerate session identifiers after authentication and privilege changes where applicable.

Set short session timeouts and invalidate sessions on logout.

6. Missing Rate Limiting
Insecure pattern
csharp
// DO NOT USE IN PRODUCTION
public IHttpActionResult Login(LoginRequest request)
{
    bool isValid = authenticationService.ValidateCredentials(request.Username, request.Password);

    if (!isValid)
    {
        return Unauthorized();
    }

    return Ok();
}
Why it is insecure
An attacker may repeatedly attempt credentials, OTPs, password-reset requests, or expensive operations without restriction.

Secure pattern
csharp
public IHttpActionResult Login(LoginRequest request)
{
    string clientKey = GetClientIdentifier(); // IP, user, or combination based on your threat model.

    if (!rateLimitService.AllowRequest(clientKey, "login"))
    {
        return StatusCode(HttpStatusCode.TooManyRequests);
    }

    bool isValid = authenticationService.ValidateCredentials(request.Username, request.Password);

    if (!isValid)
    {
        rateLimitService.RecordFailure(clientKey, "login");
        return Unauthorized();
    }

    rateLimitService.ResetFailures(clientKey, "login");
    return Ok();
}
IIS-level control
For infrastructure-level restrictions, IIS supports IP Address and Domain Restrictions. This can be useful for limiting access from known ranges or blocking abusive sources.

Secure design notes
Apply limits to login, OTP, password reset, search, file upload, and expensive API operations.

Use a combination of application-level throttling and infrastructure-level controls where appropriate.

Return a generic rate-limit response; do not reveal internal implementation details.

Monitor blocked or throttled requests for signs of brute-force or abuse.

General Secure Coding Principles
Validate on the server. Client-side validation improves usability but is not a security control.

Use least privilege. Application identities, database accounts, and service accounts should have only required permissions.

Do not trust user input. Validate, encode, and authorize every request.

Fail securely. Return generic errors to users and log details securely on the server.

Use defense in depth. Combine secure coding, configuration hardening, monitoring, and testing.

Retest after fixing. Confirm that the vulnerability is fixed and that legitimate functionality still works.

Disclaimer
These examples are simplified for learning and portfolio purposes.
Real applications require threat modeling, code review, testing, and environment-specific security controls.
