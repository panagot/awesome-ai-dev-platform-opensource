# [CRITICAL] Bug Report: SSRF in Multiple Parameters

## 🔍 Vulnerability Description

Multiple Server-Side Request Forgery (SSRF) vulnerabilities exist across various parameters in the AIxBlock platform. The application accepts user-controlled URLs in 19+ different parameters without proper validation, allowing attackers to force the server to make HTTP requests to arbitrary URLs, including internal resources, cloud metadata endpoints, and private network addresses.

**Location**:
- Domains: `api.aixblock.io`, `app.aixblock.io`, `webhook.aixblock.io` (CRITICAL domains)
- Component: Multiple endpoints accepting URL parameters
- Affected Parameters: 19+ parameters identified (see detailed report)

**Root Cause**: The application processes user-controlled URLs without:
1. Validating target hostname/IP address
2. Blocking access to internal/private IP ranges
3. Whitelisting allowed domains
4. Proper URL parsing and validation

## 🧠 Impact Assessment

**Technical Impact**:
- Internal network access and service enumeration
- Cloud metadata endpoint access (AWS, GCP, Azure) - potential for complete account compromise
- Data exfiltration from internal services
- Port scanning of internal infrastructure
- Bypass of firewall protections

**Business Impact**:
- Affects **webhook integrations** (new feature) - critical third-party integration ecosystem
- Potential cloud account compromise if metadata endpoints accessible
- Data breach of sensitive internal resources
- Compliance violations (GDPR, CCPA)
- Significant financial and reputation impact

**CVSS v3.1 Score**: 8.6 (High, treated as Critical due to widespread impact across 19+ parameters)

## 📸 Screenshots or Video Evidence

Representative screenshots demonstrating SSRF exploitation across different parameters are attached below.

## 🔄 Steps to Reproduce

1. Identify an endpoint that accepts URL parameters (e.g., `url`, `webhook`, `image`, etc.)
2. Craft a malicious request with parameter set to internal address:
   ```bash
   curl -X POST "https://app.aixblock.io/api/endpoint" \
     -H "Authorization: Token [YOUR_TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{"url": "http://127.0.0.1:8080/internal-service"}'
   ```
3. Observe the response - if server makes request to internal address, vulnerability confirmed
4. Test access to cloud metadata endpoints (e.g., `http://169.254.169.254/latest/meta-data/`)

## 🔧 Suggested Fix

Complete fix implementation is available in the PR. The fix implements:
- Comprehensive URL validation function
- Blocking of internal/private IP ranges
- Domain whitelisting where applicable
- Proper URL parsing and normalization

See detailed report: https://github.com/panagot/awesome-ai-dev-platform-opensource/tree/main/bug-bounty-findings/CRITICAL/002-ssrf-comprehensive

