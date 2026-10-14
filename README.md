# Institution Intelligence Platform (IIP) — Streamlit starter

A browser-deployable prototype for a college/institution intelligence dashboard.

## Important data note
All institutions and numerical records in this starter are fictional demonstration data. Do not represent them as official or verified college records. The app deliberately labels source and verification limitations.

## Fastest browser-only workflow

1. Create or sign in to a GitHub account.
2. Create a new **public** repository named `iip-streamlit` (public is the simplest route for Streamlit Community Cloud).
3. Upload `app.py` and `requirements.txt` to the repository using GitHub's web interface:
   - Open the repository.
   - Choose **Add file → Upload files**.
   - Drag both files into the page and commit the changes.
4. Open https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select the `iip-streamlit` repository, branch `main`, and main file path `app.py`.
6. Deploy. Streamlit installs packages from `requirements.txt` and publishes a URL.
7. Open the app URL and test each sidebar page.

## Local run (optional)
If you later use a computer with Python installed:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Included
- Executive overview
- Admission intelligence
- Placement intelligence
- Rankings and accreditation
- Promoter due-diligence entry form (temporary session only)
- Campus performance
- Commercial scenario calculator
- Risk register
- Sources and verification register
- CSV downloads
- Fictional demonstration data for three institutions

## Prototype limitations
- No live government/university integrations.
- No persistent database; form entries are session-only and may disappear when the app restarts.
- No authentication or access controls.
- No legal-record search.
- CSV reports are provided; a branded PDF export can be added later.
