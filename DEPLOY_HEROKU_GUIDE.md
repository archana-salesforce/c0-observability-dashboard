# Heroku Deployment Guide for `ASR_Dash_C0`

This folder now contains a minimal Flask app that serves your static dashboard shell:

- `app.py`: serves `c0-observability.html` at `/` and also serves the local SVG and HTML files in this folder
- `Procfile`: tells Heroku how to start the web process
- `requirements.txt`: Python dependencies for Heroku
- `.python-version`: pins the Python version the current Heroku Python buildpack expects
- `runtime.txt`: legacy Python version pin kept for compatibility
- `.gitignore`: keeps local Python environment files out of Git

## What this app does

- Hosts `c0-observability.html` as the home page
- Serves local assets like `sf logo.svg`, `ds logo.svg`, `det logo.svg`, `slack.svg`, and `updates-icon.svg`
- Leaves all Tableau embed logic in the browser exactly as it works today

Heroku is only serving the page shell. Tableau still handles the embedded dashboards and their connection to Snowflake.

## Files to include in the Git repo

Include everything in this folder:

- `c0-observability.html`
- `email_coach_v34.html`
- `sf logo.svg`
- `ds logo.svg`
- `det logo.svg`
- `slack.svg`
- `updates-icon.svg`
- `app.py`
- `Procfile`
- `requirements.txt`
- `.python-version`
- `runtime.txt`
- `.gitignore`
- `DEPLOY_HEROKU_GUIDE.md`

## Step 1: Install the tools you need

On the machine you will use to deploy:

1. Install Git: [https://git-scm.com/downloads/win](https://git-scm.com/downloads/win)
2. Install the Heroku CLI: [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. Confirm both are installed:

```powershell
git --version
heroku --version
```

## Step 2: Open a terminal in this folder

Use PowerShell and change into the project folder:

```powershell
cd "C:\Users\archana.parihar\Documents\decision-science-sandbox\archana\codex\ASR_Dash_C0"
```

## Step 3: Test locally before deploying

Create a local virtual environment, install dependencies, and run the app:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open:

- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/c0-observability.html`

Check that:

- the page loads
- the local logos render
- the Tableau embeds load for users who have access

## Step 4: Create a new GitHub repo for these files

From the GitHub page in your screenshot:

1. Click the green `New` button
2. Repository name: `c0-observability-dashboard`
3. Visibility: `Private`
4. Do not initialize with a README, `.gitignore`, or license
5. Click `Create repository`

After GitHub shows you the new repo URL, copy it. It will look like one of these:

```text
https://github.com/archana-salesforce/c0-observability-dashboard.git
git@github.com:archana-salesforce/c0-observability-dashboard.git
```

## Step 5: Create a local Git repo and connect it to GitHub

If you want this folder to become its own repo:

```powershell
git init
git branch -M main
git add .
git commit -m "Initial Heroku app for C0 observability dashboard"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

Example:

```powershell
git remote add origin https://github.com/<your-org>/<your-repo>.git
git push -u origin main
```

## Step 6: Log in to Heroku

```powershell
heroku login
```

This opens a browser so you can authenticate.

## Step 7: Create the Heroku app

Pick a unique app name. Example:

```powershell
heroku create c0-observability-dashboard
```

If the name is taken, Heroku will tell you. Try a variation until it succeeds.

Optional: if you already know the app should live in a Heroku team or enterprise space, create it there instead:

```powershell
heroku create c0-observability-dashboard --team <HEROKU_TEAM_NAME>
```

## Step 8: Connect Heroku to GitHub

In the Heroku Dashboard:

1. Open your new app
2. Go to the `Deploy` tab
3. Under `Deployment method`, choose `GitHub`
4. Connect your GitHub account if Heroku prompts you
5. Search for `c0-observability-dashboard`
6. Click `Connect`
7. Under `Manual deploy`, choose branch `main`
8. Click `Deploy Branch`

If you want every push to GitHub to redeploy automatically, enable `Automatic Deploys` for the `main` branch.

Important: once you use GitHub integration, GitHub should be your source of truth. Heroku’s docs recommend not mixing that with regular `git push heroku main` deploys unless you have a specific reason.

## Step 9: Alternative deploy path with Heroku Git

If you do not want to use the Heroku Dashboard GitHub integration, you can deploy straight from your machine:

```powershell
git push heroku main
```

This works, but for your use case GitHub integration is usually cleaner because the repo becomes the canonical source.

## Step 10: Confirm the app is serving the right page
When the deploy completes, open the app from the Heroku Dashboard or run:

```powershell
heroku open
```

You can inspect logs with:

```powershell
heroku logs --tail
```

## Step 11: Update the app later

Any time you update the HTML or SVG files:

```powershell
git add .
git commit -m "Update dashboard content"
git push origin main
```

If `Automatic Deploys` are enabled in Heroku, pushing to GitHub is enough. If not, go to the app’s `Deploy` tab and click `Deploy Branch`.

After deployment:

1. Open the Heroku URL
2. Confirm `c0-observability.html` loads at the home page
3. Confirm the SVG assets render
4. Confirm the Tableau embeds load
5. Confirm the page works with hash fragments like:

```text
https://<your-heroku-app>.herokuapp.com/#agent-rubric
```

## Important notes

- Hash routing is safe on Heroku because URL fragments such as `#agent-rubric` never hit the server
- Tableau access is still controlled by Tableau authentication and permissions
- If Tableau embedding is restricted by domain, you may need to allowlist your Heroku app domain or custom domain in Tableau
- Heroku is hosting the page shell only; Snowflake connectivity stays behind the Tableau layer

## Minimal deployment checklist

1. Install `git` and `heroku`
2. Run the app locally
3. Create an empty private GitHub repo
4. `git init`
5. `git remote add origin <repo-url>`
6. `git push -u origin main`
7. `heroku login`
8. `heroku create <app-name>`
9. Connect the app to GitHub in the Heroku `Deploy` tab
10. Deploy branch `main`
11. Open the Heroku URL and validate the Tableau embeds
