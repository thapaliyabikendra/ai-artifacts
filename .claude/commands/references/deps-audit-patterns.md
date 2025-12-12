# Dependency Audit Patterns Reference

Patterns and code for the `/refactor:deps-audit` command.

## Dependency Discovery

```python
from pathlib import Path
import json
import toml

class DependencyDiscovery:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dependency_files = {
            'npm': ['package.json', 'package-lock.json', 'yarn.lock'],
            'python': ['requirements.txt', 'Pipfile', 'pyproject.toml', 'poetry.lock'],
            'ruby': ['Gemfile', 'Gemfile.lock'],
            'java': ['pom.xml', 'build.gradle'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'dotnet': ['*.csproj', 'packages.config']
        }

    def discover_all_dependencies(self):
        """Discover all dependencies across different package managers"""
        dependencies = {}

        if (self.project_path / 'package.json').exists():
            dependencies['npm'] = self._parse_npm_dependencies()
        if (self.project_path / 'requirements.txt').exists():
            dependencies['python'] = self._parse_requirements_txt()
        if (self.project_path / 'go.mod').exists():
            dependencies['go'] = self._parse_go_mod()

        return dependencies

    def _parse_npm_dependencies(self):
        """Parse NPM package.json and lock files"""
        with open(self.project_path / 'package.json', 'r') as f:
            package_json = json.load(f)

        deps = {}
        for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
            if dep_type in package_json:
                for name, version in package_json[dep_type].items():
                    deps[name] = {
                        'version': version,
                        'type': dep_type,
                        'direct': True
                    }
        return deps
```

## Vulnerability Scanning

```python
import requests

class VulnerabilityScanner:
    def __init__(self):
        self.vulnerability_apis = {
            'npm': 'https://registry.npmjs.org/-/npm/v1/security/advisories/bulk',
            'pypi': 'https://pypi.org/pypi/{package}/json',
            'maven': 'https://ossindex.sonatype.org/api/v3/component-report'
        }

    def scan_vulnerabilities(self, dependencies):
        """Scan dependencies for known vulnerabilities"""
        vulnerabilities = []

        for package_name, package_info in dependencies.items():
            vulns = self._check_package_vulnerabilities(
                package_name,
                package_info['version'],
                package_info.get('ecosystem', 'npm')
            )
            if vulns:
                vulnerabilities.extend(vulns)

        return self._analyze_vulnerabilities(vulnerabilities)

    def _check_npm_vulnerabilities(self, name, version):
        """Check NPM package vulnerabilities"""
        response = requests.post(
            'https://registry.npmjs.org/-/npm/v1/security/advisories/bulk',
            json={name: [version]}
        )

        vulnerabilities = []
        if response.status_code == 200:
            data = response.json()
            if name in data:
                for advisory in data[name]:
                    vulnerabilities.append({
                        'package': name,
                        'version': version,
                        'severity': advisory['severity'],
                        'title': advisory['title'],
                        'cve': advisory.get('cves', []),
                        'patched_versions': advisory['patched_versions']
                    })
        return vulnerabilities
```

## Severity Analysis

```python
def analyze_vulnerability_severity(vulnerabilities):
    """Analyze and prioritize vulnerabilities by severity"""
    severity_scores = {
        'critical': 9.0,
        'high': 7.0,
        'moderate': 4.0,
        'low': 1.0
    }

    analysis = {
        'total': len(vulnerabilities),
        'by_severity': {'critical': [], 'high': [], 'moderate': [], 'low': []},
        'risk_score': 0,
        'immediate_action_required': []
    }

    for vuln in vulnerabilities:
        severity = vuln['severity'].lower()
        analysis['by_severity'][severity].append(vuln)

        base_score = severity_scores.get(severity, 0)

        if vuln.get('exploit_available', False):
            base_score *= 1.5
        if 'remote_code_execution' in vuln.get('description', '').lower():
            base_score *= 2.0

        vuln['risk_score'] = base_score
        analysis['risk_score'] += base_score

        if severity in ['critical', 'high'] or base_score > 8.0:
            analysis['immediate_action_required'].append({
                'package': vuln['package'],
                'severity': severity,
                'action': f"Update to {vuln['patched_versions']}"
            })

    return analysis
```

## License Compliance

```python
class LicenseAnalyzer:
    def __init__(self):
        self.license_compatibility = {
            'MIT': ['MIT', 'BSD', 'Apache-2.0', 'ISC'],
            'Apache-2.0': ['Apache-2.0', 'MIT', 'BSD'],
            'GPL-3.0': ['GPL-3.0', 'GPL-2.0'],
            'proprietary': []
        }

        self.license_restrictions = {
            'GPL-3.0': 'Copyleft - requires source code disclosure',
            'AGPL-3.0': 'Strong copyleft - network use requires source disclosure',
            'proprietary': 'Cannot be used without explicit license',
            'unknown': 'License unclear - legal review required'
        }

    def analyze_licenses(self, dependencies, project_license='MIT'):
        """Analyze license compatibility"""
        issues = []
        license_summary = {}

        for package_name, package_info in dependencies.items():
            license_type = package_info.get('license', 'unknown')

            if license_type not in license_summary:
                license_summary[license_type] = []
            license_summary[license_type].append(package_name)

            if not self._is_compatible(project_license, license_type):
                issues.append({
                    'package': package_name,
                    'license': license_type,
                    'issue': f'Incompatible with project license {project_license}',
                    'severity': 'high'
                })

        return {
            'summary': license_summary,
            'issues': issues,
            'compliance_status': 'FAIL' if issues else 'PASS'
        }
```

## License Report Template

```markdown
## License Compliance Report

### Summary
- **Project License**: MIT
- **Total Dependencies**: 245
- **License Issues**: 3
- **Compliance Status**: ⚠️ REVIEW REQUIRED

### License Distribution
| License | Count | Packages |
|---------|-------|----------|
| MIT | 180 | express, lodash, ... |
| Apache-2.0 | 45 | aws-sdk, ... |
| GPL-3.0 | 3 | [ISSUE] package1, package2, package3 |
| Unknown | 2 | [ISSUE] mystery-lib, old-package |

### Compliance Issues

#### High Severity
1. **GPL-3.0 Dependencies**
   - Packages: package1, package2, package3
   - Issue: GPL-3.0 is incompatible with MIT license
   - Risk: May require open-sourcing your entire project
   - Recommendation: Replace with MIT/Apache licensed alternatives
```

## Outdated Dependencies

```python
def analyze_outdated_dependencies(dependencies):
    """Check for outdated dependencies"""
    outdated = []

    for package_name, package_info in dependencies.items():
        current_version = package_info['version']
        latest_version = fetch_latest_version(package_name)

        if is_outdated(current_version, latest_version):
            version_diff = calculate_version_difference(current_version, latest_version)

            outdated.append({
                'package': package_name,
                'current': current_version,
                'latest': latest_version,
                'type': version_diff['type'],  # major, minor, patch
                'releases_behind': version_diff['count'],
                'age_days': get_version_age(package_name, current_version),
                'breaking_changes': version_diff['type'] == 'major'
            })

    return prioritize_updates(outdated)

def prioritize_updates(outdated_deps):
    """Prioritize updates based on multiple factors"""
    for dep in outdated_deps:
        score = 0

        if dep.get('has_security_fix', False):
            score += 100
        if dep['type'] == 'major':
            score += 20
        elif dep['type'] == 'minor':
            score += 10
        if dep['age_days'] > 365:
            score += 30

        dep['priority_score'] = score
        dep['priority'] = 'critical' if score > 80 else 'high' if score > 50 else 'medium'

    return sorted(outdated_deps, key=lambda x: x['priority_score'], reverse=True)
```

## Supply Chain Security

```python
def check_supply_chain_security(dependencies):
    """Perform supply chain security checks"""
    security_issues = []

    for package_name, package_info in dependencies.items():
        # Check for typosquatting
        typo_check = check_typosquatting(package_name)
        if typo_check['suspicious']:
            security_issues.append({
                'type': 'typosquatting',
                'package': package_name,
                'severity': 'high',
                'similar_to': typo_check['similar_packages']
            })

        # Check maintainer changes
        maintainer_check = check_maintainer_changes(package_name)
        if maintainer_check['recent_changes']:
            security_issues.append({
                'type': 'maintainer_change',
                'package': package_name,
                'severity': 'medium',
                'details': maintainer_check['changes']
            })

    return security_issues

def check_typosquatting(package_name):
    """Check if package name might be typosquatting"""
    common_packages = [
        'react', 'express', 'lodash', 'axios', 'webpack',
        'babel', 'jest', 'typescript', 'eslint', 'prettier'
    ]

    for legit_package in common_packages:
        distance = levenshtein_distance(package_name.lower(), legit_package)
        if 0 < distance <= 2:
            return {'suspicious': True, 'similar_packages': [legit_package]}

    return {'suspicious': False}
```

## Automated Remediation

### Update Script

```bash
#!/bin/bash
# Auto-update dependencies with security fixes

echo "🔒 Security Update Script"

# NPM/Yarn updates
if [ -f "package.json" ]; then
    echo "📦 Updating NPM dependencies..."
    npm audit fix --force
    npm test

    if [ $? -eq 0 ]; then
        echo "✅ NPM updates successful"
    else
        echo "❌ Tests failed, reverting..."
        git checkout package-lock.json
    fi
fi

# Python updates
if [ -f "requirements.txt" ]; then
    echo "🐍 Updating Python dependencies..."
    cp requirements.txt requirements.txt.backup
    pip-compile --upgrade-package package1 --upgrade-package package2
    pip install -r requirements.txt --dry-run

    if [ $? -eq 0 ]; then
        echo "✅ Python updates successful"
    else
        mv requirements.txt.backup requirements.txt
    fi
fi
```

### PR Generation

```python
def generate_dependency_update_pr(updates):
    """Generate PR with dependency updates"""
    pr_body = f"""
## 🔒 Dependency Security Update

This PR updates {len(updates)} dependencies to address security vulnerabilities.

### Security Fixes ({sum(1 for u in updates if u['has_security'])})

| Package | Current | Updated | Severity | CVE |
|---------|---------|---------|----------|-----|
"""

    for update in updates:
        if update['has_security']:
            pr_body += f"| {update['package']} | {update['current']} | {update['target']} | {update['severity']} | {', '.join(update['cves'])} |\n"

    pr_body += """

### Testing
- [ ] All tests pass
- [ ] No breaking changes identified

### Review Checklist
- [ ] Security vulnerabilities addressed
- [ ] License compliance maintained
"""

    return {
        'title': f'chore(deps): Security update for {len(updates)} dependencies',
        'body': pr_body,
        'labels': ['dependencies', 'security']
    }
```

## GitHub Actions Workflow

```yaml
name: Dependency Audit

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  push:
    paths:
      - 'package*.json'
      - 'requirements.txt'
  workflow_dispatch:

jobs:
  security-audit:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Run NPM Audit
      if: hashFiles('package.json')
      run: |
        npm audit --json > npm-audit.json
        if [ $(jq '.vulnerabilities.total' npm-audit.json) -gt 0 ]; then
          echo "::error::Found vulnerabilities"
          exit 1
        fi

    - name: Run Python Safety Check
      if: hashFiles('requirements.txt')
      run: |
        pip install safety
        safety check --json > safety-report.json

    - name: Check Licenses
      run: |
        npx license-checker --json > licenses.json
        python scripts/check_license_compliance.py

    - name: Create Issue for Critical Vulnerabilities
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          const audit = require('./npm-audit.json');
          const critical = audit.vulnerabilities.critical;

          if (critical > 0) {
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `🚨 ${critical} critical vulnerabilities found`,
              body: 'Dependency audit found critical vulnerabilities.',
              labels: ['security', 'dependencies', 'critical']
            });
          }
```

## Output Report Template

```markdown
## Dependency Audit Report

### Executive Summary
- **Total Dependencies**: {count}
- **Direct**: {direct_count} | **Transitive**: {transitive_count}
- **Security Risk**: {HIGH|MEDIUM|LOW}
- **License Compliance**: {PASS|FAIL}

### Security Vulnerabilities

| Severity | Count | Action Required |
|----------|-------|-----------------|
| Critical | {n} | Immediate update |
| High | {n} | Update this sprint |
| Moderate | {n} | Schedule update |
| Low | {n} | Backlog |

### Top Priority Updates

1. **{package}** - {current} → {latest}
   - CVE: {cve_id}
   - Severity: Critical
   - Fix: `npm update {package}`

### License Issues

| Package | License | Issue | Recommendation |
|---------|---------|-------|----------------|
| {pkg} | GPL-3.0 | Incompatible | Replace with alternative |

### Outdated Dependencies

| Package | Current | Latest | Age | Priority |
|---------|---------|--------|-----|----------|
| {pkg} | 1.0.0 | 3.0.0 | 2 years | High |

### Recommendations

1. **Immediate**: Update {n} packages with critical vulnerabilities
2. **This Sprint**: Review {n} license issues
3. **Backlog**: Plan major version updates for {n} packages
```
