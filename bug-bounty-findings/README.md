# 🛡️ Bug Bounty Findings - AIxBlock Security Reports

This folder contains professionally documented security vulnerabilities discovered during the AIxBlock Bug Bounty Program, along with complete code fixes ready for PR submission.

## 📋 Submission Status

- [x] Repository starred: https://github.com/AIxBlock-2023/awesome-ai-dev-platform-opensource
- [x] Repository forked: https://github.com/panagot/awesome-ai-dev-platform-opensource
- [ ] Issues created (pending)
- [ ] PRs submitted (pending)

## 🎯 Findings Overview

### CRITICAL Severity (2 findings)

1. **WORKFLOW_IDOR** - Insecure Direct Object Reference in Workflow Endpoints
   - CVSS Score: 9.1 (Critical)
   - Domain: `workflow.aixblock.io` (Critical - highest value target)
   - Status: Ready for submission
   - Fix: Complete code implementation ready

2. **SSRF_COMPREHENSIVE** - Server-Side Request Forgery in Multiple Parameters
   - CVSS Score: 8.6 (High, treated as Critical due to widespread impact)
   - Domains: `api.aixblock.io`, `app.aixblock.io`, `webhook.aixblock.io`
   - Affected Parameters: 19+ parameters identified
   - Status: Ready for submission
   - Fix: Complete code implementation ready

### HIGH Severity (1 finding)

3. **API_ENDPOINT_60** - IDOR in User Data Access
   - CVSS Score: 7.5 (High)
   - Domain: `api.aixblock.io`
   - Status: Ready for submission
   - Fix: Complete code implementation ready

## 📁 Structure

```
bug-bounty-findings/
├── README.md (this file)
├── CRITICAL/
│   ├── 001-workflow-idor/
│   │   ├── ISSUE.md (GitHub issue content)
│   │   ├── REPORT.md (Detailed technical report)
│   │   ├── FIX.md (Fix description and implementation guide)
│   │   ├── fixes/ (Code fixes ready for PR)
│   │   └── evidence/ (Screenshots)
│   └── 002-ssrf-comprehensive/
│       ├── ISSUE.md
│       ├── REPORT.md
│       ├── FIX.md
│       ├── fixes/
│       └── evidence/
└── HIGH/
    └── 003-api-endpoint-60/
        ├── ISSUE.md
        ├── REPORT.md
        ├── FIX.md
        └── fixes/ (Code fixes ready for PR)
```

## 🔗 Links

- **Original Repository**: https://github.com/AIxBlock-2023/awesome-ai-dev-platform-opensource
- **Fork**: https://github.com/panagot/awesome-ai-dev-platform-opensource
- **Issues**: https://github.com/AIxBlock-2023/awesome-ai-dev-platform-opensource/issues

## 📝 Notes

- All findings include detailed reports, proof of concept, and complete code fixes
- Fixes are ready for immediate PR submission
- Reports follow AIxBlock Bug Bounty Program guidelines
- All evidence (screenshots) is included

---

**Submitted by**: panagot  
**Submission Date**: 2025-12-23  
**Program**: AIxBlock Bug Bounty Program
