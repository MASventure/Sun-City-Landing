# Contributing to Sun City Landing

Thank you for investing in the Sun City Landing project! This guide explains
how we collaborate so changes remain predictable and easy to review.

## Repository layout

```
frontend/
  index.html
  css/
  js/
backend/
  app.py
  routes/
  services/
  models/
  data/
```

The `frontend` directory holds all static assets for the landing page. The
`backend` directory contains a lightweight Flask service that powers API
endpoints used by the client.

## Branching strategy

We follow a **trunk-based flow with short-lived feature branches**:

1. Start new work from the latest `work` branch.
2. Create a descriptive feature branch named with the pattern
   `feature/<short-description>` (for example, `feature/add-gallery-section`).
   Bug fixes use `fix/<short-description>`.
3. Keep branches focused on one logical change. If multiple features are
   required, open separate branches to simplify code review.
4. Rebase onto `work` frequently to stay current and resolve conflicts early.
5. Open a pull request against `work` when the feature is ready and all checks
   pass.
6. After approval and successful checks, squash-merge the branch into `work`
   and delete the feature branch.

Hotfixes that must go live immediately follow the same pattern but use the
prefix `hotfix/` and should be merged with a high-priority review.

## Commit conventions

- Write conventional commit messages using the format
  `<type>: <imperative summary>` where `type` is one of `feat`, `fix`, `docs`,
  `refactor`, or `chore`.
- Keep commits scoped so they can be reverted independently if necessary.
- Run formatting and tests relevant to your change prior to committing.

## Backend development

Install dependencies and run the server locally:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app backend.app run --debug
```

The Flask app exposes API endpoints under `/api`. Use these endpoints when
building or updating frontend integrations.

## Frontend development

Serve the static assets using any HTTP server (for example, `python -m
http.server`). Update CSS and JavaScript in their respective directories and
keep IDs/classes meaningful for testing and automation.

## Submitting changes

1. Ensure all tests and linters pass.
2. Update documentation when behavior or dependencies change.
3. Include screenshots for visual updates when relevant.
4. Request a review from another teammate before merging.
