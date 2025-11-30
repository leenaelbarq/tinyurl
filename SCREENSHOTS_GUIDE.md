# Screenshots Guide for REPORT.md

You need to take 6 screenshots and add them to the Appendix section of REPORT.md.

## Required Screenshots:

### A. Coverage Report
**What to capture**: Terminal output showing pytest coverage

**How to get it**:
```bash
cd /Users/leenabarq/Downloads/tinyurl
source .venv/bin/activate
python -m pytest --cov=app --cov-report=term-missing
```

**What to screenshot**: The coverage table showing 89% coverage

**Where to add**: Replace `[INSERT SCREENSHOT: pytest coverage output showing 89%]` in REPORT.md

---

### B. CI Pipeline Success
**What to capture**: GitHub Actions CI workflow success page

**How to get it**:
1. Go to: https://github.com/leenaelbarq/tinyurl/actions
2. Click on "CI" in the left sidebar
3. Click on the most recent successful run (green checkmark)
4. Screenshot the entire page showing all green checkmarks

**Where to add**: Replace `[INSERT SCREENSHOT: GitHub Actions CI workflow success]` in REPORT.md

---

### C. CD Pipeline Success
**What to capture**: GitHub Actions CD workflow deploying to Azure

**How to get it**:
1. Go to: https://github.com/leenaelbarq/tinyurl/actions
2. Click on "CD" in the left sidebar
3. Click on the most recent successful run (green checkmark)
4. Screenshot showing the deployment steps completed

**Where to add**: Replace `[INSERT SCREENSHOT: GitHub Actions CD workflow deploying to Azure]` in REPORT.md

---

### D. Live Application
**What to capture**: Your working app in a browser

**How to get it**:
1. Open: https://leena-tinyurl-webapp.azurewebsites.net
2. Screenshot the homepage showing:
   - "TinyURL" title
   - Input field
   - "Shorten" button
   - "All Short Links" section

**Where to add**: Replace `[INSERT SCREENSHOT: Working app at https://leena-tinyurl-webapp.azurewebsites.net]` in REPORT.md

---

### E. Metrics Endpoint
**What to capture**: /metrics endpoint showing Prometheus metrics

**How to get it**:
Option 1 - Browser:
1. Open: https://leena-tinyurl-webapp.azurewebsites.net/metrics
2. Screenshot showing the metrics (scroll to show tinyurl_ metrics)

Option 2 - Terminal:
```bash
curl https://leena-tinyurl-webapp.azurewebsites.net/metrics | grep "tinyurl_" | head -20
```
Screenshot the terminal output

**Where to add**: Replace `[INSERT SCREENSHOT: /metrics endpoint showing Prometheus metrics]` in REPORT.md

---

### F. Azure Resources
**What to capture**: Azure portal showing your resources

**How to get it**:
1. Go to: https://portal.azure.com
2. Search for "leena-tinyurl-webapp" or navigate to your resource group
3. Screenshot showing:
   - Web App (leena-tinyurl-webapp)
   - Container Registry (leenatinyurlcr)
   - Or the resource group overview page

**Where to add**: Replace `[INSERT SCREENSHOT: Azure portal showing Web App and ACR]` in REPORT.md

---

## How to Add Screenshots to REPORT.md:

1. Save screenshots with clear names:
   - `coverage_report.png`
   - `ci_success.png`
   - `cd_success.png`
   - `live_app.png`
   - `metrics_endpoint.png`
   - `azure_resources.png`

2. Create an `images/` folder in your repo:
```bash
mkdir -p images
```

3. Move screenshots to images folder

4. Update REPORT.md:
Replace each `[INSERT SCREENSHOT: ...]` with:
```markdown
![Description](images/screenshot_name.png)
```

Example:
```markdown
### A. Coverage Report
![Coverage Report showing 89%](images/coverage_report.png)
```

5. Commit and push:
```bash
git add images/ REPORT.md
git commit -m "docs: add screenshots to REPORT"
git push origin main
```

---

## Quick Commands Reference:

```bash
# Take coverage screenshot
cd /Users/leenabarq/Downloads/tinyurl
source .venv/bin/activate
python -m pytest --cov=app --cov-report=term-missing

# View live app
open https://leena-tinyurl-webapp.azurewebsites.net

# View metrics
open https://leena-tinyurl-webapp.azurewebsites.net/metrics

# View GitHub Actions
open https://github.com/leenaelbarq/tinyurl/actions

# View Azure Portal
open https://portal.azure.com
```
