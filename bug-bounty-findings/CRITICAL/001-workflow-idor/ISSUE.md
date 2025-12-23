# [CRITICAL] Bug Report: IDOR in Workflow Endpoints

## 🔍 Vulnerability Description

Insecure Direct Object Reference (IDOR) vulnerability in workflow endpoints allows unauthorized access to other users' workflows by manipulating the workflow ID parameter in the URL.

**Location**:
- Endpoint: `https://app.aixblock.io/api/workflows/{id}`
- Domain: `workflow.aixblock.io` (CRITICAL - highest value target per BugBounty.md)
- Parameter: `workflow_id` (in URL path)
- HTTP Methods: GET, PUT, PATCH, DELETE

**Root Cause**: The `WorkflowViewSet` does not verify that the authenticated user owns the requested workflow before allowing access. The endpoint accepts any workflow ID without authorization checks.

## 🧠 Impact Assessment

**Technical Impact**:
- Unauthorized access to other users' workflows
- Exposure of sensitive automation logic and business processes
- Data breach of workflow configurations
- Privacy violations

**Business Impact**:
- Affects **automation workflows feature** (workflow.aixblock.io) - a critical new feature
- Violates data protection regulations (GDPR, CCPA)
- Potential financial losses from data breaches
- Reputation damage and legal liability

**CVSS v3.1 Score**: 9.1 (Critical)
- Attack Vector: Network
- Attack Complexity: Low
- Privileges Required: Low (authenticated user)
- Confidentiality Impact: High
- Integrity Impact: High

## 📸 Screenshots or Video Evidence

Screenshots demonstrating unauthorized access to other users' workflows are attached below.

## 🔄 Steps to Reproduce

1. Authenticate to the AIxBlock platform and obtain an authentication token
2. Identify a workflow ID that belongs to another user
3. Send a GET request to the workflow endpoint:
   ```bash
   curl -X GET "https://app.aixblock.io/api/workflows/603804808873652" \
     -H "Authorization: Token [YOUR_TOKEN]"
   ```
4. Observe the response - returns `200 OK` with workflow data (should return `403 Forbidden`)
5. Verify unauthorized access - confirm you can access workflows that do not belong to your account

## 🔧 Suggested Fix

Complete fix code is available in the PR. The fix implements:
- `IsAuthenticated` permission requirement
- Ownership checks in `get_queryset()` to filter by authenticated user
- Explicit authorization checks in `retrieve()`, `update()`, and `destroy()` methods

See detailed report and fix implementation: https://github.com/panagot/awesome-ai-dev-platform-opensource/tree/main/bug-bounty-findings/CRITICAL/001-workflow-idor

