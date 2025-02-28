## Team Member Names
- Colin Crippen
- CJ Faircloth
- Ryan Fitzgerald

## Tools/Resources Used
- NewsAPI
- Google's reCAPTCHA v2

## Build and Run Instructions
1. Clone the repository:
```bash
git clone https://github.com/colincrippen/Boko-Hacks-2025.git
cd Boko-Hacks-2025
```

2. Creating and activating a virtual environment using VSCode:
- CTRL+SHIFT+P to view Command Palette
- Enter "Python: Create Environment"
- Select "Venv"
- Select "Delete and Recreate"
- Select "Python 3.12.2" or a similar up-to-date Python interpreter path
- Check off requirements.txt and select "OK"

3. Open "RENAME_TO_DOT_ENV" file

4. For the judges' convenience, copy and paste the following into the "RENAME_TO_DOT_ENV" file
```bash
NEWS_API_KEY='49a12ef1b1e54d89bfbb0b0e9519eca6'
RECAPTCHA_SECRET_KEY='6Lc_2uUqAAAAAEfO4VcZ00trkCmI_jXITRBAAfix'
```

5. Rename "RENAME_TO_DOT_ENV" to ".env"

6. Start the application: 
```bash
python app.py
```