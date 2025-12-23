# Finding #1: WORKFLOW_IDOR - Insecure Direct Object Reference

## 📊 Summary

**Severity**: CRITICAL  
**CVSS Score**: 9.1  
**Component**: Workflow Endpoints  
**Domain**: workflow.aixblock.io (CRITICAL - highest value target)

## 📁 Contents

- `report.md` - Complete vulnerability report with technical details, impact assessment, and proof of concept
- `fixes/` - Proposed code fixes (views.py, serializers.py)
- `screenshots/` - Visual evidence of the vulnerability

## 🔗 Related

- **GitHub Issue**: #TBD
- **Pull Request**: #TBD
- **Branch**: `bugfix/issue-1-workflow-idor`

## 🔧 Fix Location

The fixes in `fixes/` should be applied to:
- `workflow/views.py` (or equivalent ViewSet file)
- `workflow/serializers.py` (if applicable)

## 📸 Evidence

Screenshots demonstrate unauthorized access to other users' workflows by manipulating the workflow ID parameter.

---

**Status**: Reported | Awaiting Acknowledgment | Validated | Fixed

