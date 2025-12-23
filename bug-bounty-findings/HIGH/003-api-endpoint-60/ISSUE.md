# [HIGH] Bug Report: IDOR - Unauthorized User Data Access

## 🔍 Vulnerability Description

The API endpoint `/api/users/{id}` allows unauthorized access to user data through Insecure Direct Object Reference (IDOR). An authenticated user can access other users' personal information by manipulating the user ID parameter in the URL path.

**Location**:
- Endpoint: `/api/users/{id}` (where `{id}` is the user ID)
- Domain: `api.aixblock.io`
- Parameter: `user_id` (in URL path)
- HTTP Methods: GET, PUT, PATCH, DELETE

**Root Cause**: The endpoint does not verify that the authenticated user has permission to access the requested user's data. The authorization check is missing, allowing users to access other users' personal information.

## 🧠 Impact Assessment

**Technical Impact**:
- Unauthorized access to other users' email addresses, profile information, and sensitive data
- Potential for account enumeration
- Privacy violations and compliance issues (GDPR, CCPA)

**Business Impact**:
- Violates data protection regulations (GDPR, CCPA)
- Potential financial losses from data breaches
- Reputation damage and legal liability

**CVSS v3.1 Score**: 7.5 (High)

## 📸 Screenshots or Video Evidence

Screenshots demonstrating the IDOR vulnerability will be captured during manual verification. The vulnerability can be verified by accessing `/api/users/{id}` with another user's ID while authenticated.

**Note**: Evidence folder will be created upon manual verification.

## 🔄 Steps to Reproduce

1. Authenticate to the AIxBlock platform and obtain an authentication token
2. Identify a user ID that does not belong to your account (e.g., user ID 1)
3. Send a GET request to access another user's data:
   ```bash
   curl -X GET "https://api.aixblock.io/api/users/1" \
     -H "Authorization: Token [YOUR_TOKEN]"
   ```
4. Observe the response - if the request returns `200 OK` with user data, the vulnerability is confirmed
5. Verify unauthorized access - confirm that you can access other users' data without permission

## 🔧 Suggested Fix

The fix should implement:
- Authorization checks to verify user owns the resource
- Resource-level permissions filtering by authenticated user
- Input validation for user ID parameter

See detailed report: https://github.com/panagot/awesome-ai-dev-platform-opensource/tree/main/bug-bounty-findings/HIGH/003-api-endpoint-60

