# Writing Against AI Slop: classroom app (Streamlit)

Classroom version of the Writing Against AI Slop site. The HTML site stays live on GitHub Pages; this app is for in-class use.

## What's in this folder

| File or folder | What it does |
|---|---|
| `streamlit_app.py` | The file Streamlit runs. Sets up the sidebar and the list of pages. |
| `app_pages/` | One file per page. Pages that haven't been ported yet show a "coming soon" note. |
| `content/` | The text of quizzes and exercises. **Edit wording here**, not in the page files. |
| `utils/` | Shared helpers: styling, exercise widgets, and the Word download. |
| `.streamlit/config.toml` | Colors and fonts. See the note in step 3 below. |
| `requirements.txt` | Tells Streamlit Cloud which Python packages to install. |

## Putting it online (no terminal needed)

### Step 1: Make a repository on GitHub

Sign in at github.com, click **New** (or the **+** menu, then **New repository**), name it `anti-slop-app`, and click **Create repository**.

### Step 2: Upload the files

On the new repository's page, click **uploading an existing file** (or **Add file → Upload files**). Open the unzipped `anti-slop-app` folder on your computer, select everything inside it, and drag it into the browser window. Click **Commit changes**.

### Step 3: Check for the settings folder

Look at the list of files on your repository page. You should see a folder called `.streamlit`.

**Why it might be missing:** names that start with a dot are hidden files. Mac and Windows don't show them in a normal folder window, so when you select everything and drag it, the `.streamlit` folder usually gets left behind. The app still runs without it, but it uses Streamlit's default colors and fonts, and it shows a yellow setup note on every page until the file is added.

**If `.streamlit` is missing, add it by hand:**

1. On the repository page, click **Add file → Create new file**.
2. In the file name box, type `.streamlit/config.toml` exactly. When you type the slash, GitHub turns `.streamlit` into a folder automatically.
3. Copy the block below and paste it into the large text box.
4. Click **Commit changes**.

```toml
[theme]
base = "light"
primaryColor = "#6b5030"
backgroundColor = "#f5f0e8"
secondaryBackgroundColor = "#ede8de"
textColor = "#1a1410"
borderColor = "#d5ccc0"
font = "Source Serif 4:https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&display=swap"
headingFont = "Playfair Display:https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap"

[theme.sidebar]
backgroundColor = "#ede8de"

[client]
toolbarMode = "minimal"
```

### Step 4: Turn it into an app

Go to share.streamlit.io, sign in with your GitHub account, and click **Create app**. Choose your `anti-slop-app` repository, leave the branch as `main`, and set the main file path to `streamlit_app.py`. Click **Deploy**. After a few minutes you'll get a web address, and that's the link to put in Canvas.

When you change a file on GitHub later, the app updates itself within a minute or so.

## Notes

- Nothing students type is stored. Each page has a download button that gives them a Word file of their answers.
- Community Cloud apps go to sleep after a period with no visitors, and the first person to open a sleeping app may wait a minute while it wakes up. Opening it yourself a few minutes before class avoids this.
- To run it on your own computer instead: `pip install -r requirements.txt`, then `streamlit run streamlit_app.py`.
