# Take-Home Exercise — Equipment Rental

Thanks for taking the time to do this! You'll work with a **small app that already exists** — much like you would on the job. A few core functions are left unimplemented (they raise `NotImplementedError`) for you to fill in against the business rules described in `app.py`.

It should take around **2-3 hours**. We don't expect everything to be flawless — we mostly want to see how you read unfamiliar code, reason about a spec, and track down a problem in code that isn't yours. That said, we do expect the app you send back to **work end to end in accordance with the business rules**: a customer should be able to go through the whole booking flow and get the right outcome at every step.

---

## The app

A simple tool for renting out equipment (cameras, drills, etc.). It has:

- `app.py` — a small Python (Flask) backend with the booking logic and a JSON API
- `index.html` — a one-page frontend (plain JavaScript) for making a booking
- `bookings.json` — where bookings are stored
- `requirements.txt`

## Prerequisites

You'll need **Python 3.10 or newer** installed. Check your version with:

```bash
python3 --version    # macOS / Linux
python --version     # Windows
```

If it prints something lower than 3.10, or the command isn't found, install Python first:

- **macOS** — download the installer from [python.org/downloads](https://www.python.org/downloads/), or if you use Homebrew: `brew install python`.
- **Windows** — download the installer from [python.org/downloads](https://www.python.org/downloads/) and, on the first screen, **tick "Add python.exe to PATH"** before clicking Install. (Alternatively: `winget install Python.Python.3.12`.)

No database or other tools are needed — just Python and a web browser.

---

## Getting your own copy

Before anything else:

Click **"Use this template"** on this repository to create your own copy, then clone it to your local machine to work on it.

---

## Running the app

We recommend using a virtual environment so the dependencies stay isolated.

**On macOS / Linux:**

```bash
# from inside the project folder
python3 -m venv venv          # create a virtual environment
source venv/bin/activate      # activate it (your prompt should now show "(venv)")
pip install -r requirements.txt
python app.py
```

**On Windows (PowerShell):**

```powershell
# from inside the project folder
python -m venv venv           # create a virtual environment
venv\Scripts\Activate.ps1     # activate it (your prompt should now show "(venv)")
pip install -r requirements.txt
python app.py
```

> If PowerShell blocks the activate script with an execution-policy error, run
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once in that window, then activate again.
> If you use the classic Command Prompt (cmd.exe) instead of PowerShell, activate with `venv\Scripts\activate.bat`.

Then open **http://localhost:5000** in your browser. Have a click around first to get a feel for it. The business rules are described in a comment at the top of `app.py`.

When you're done working, you can leave the virtual environment with `deactivate`.

---

## Your tasks

### 1. Implement booking-conflict detection
`dates_overlap`, `find_conflicting_booking`, and `rental_days` in `app.py` are left unimplemented (they currently `raise NotImplementedError`). Implement them against the business rules described in the comment at the top of `app.py` — including the same-day-turnover exception. *(The seed data in `bookings.json` gives you fixtures to test against — for example, there's a booking for the Canon DSLR Camera from Jan 10–15. Work out for yourself which nearby date ranges should and shouldn't be allowed, and test them.)*

### 2. Implement pricing
`calculate_total` in `app.py` is also unimplemented. Rentals are billed per the business rules at the top of the file — inclusive day counting, plus the long-rental discount. *(Pay close attention to the exact boundary of the discount rule, and test both sides of it.)*

### 3. Add a rule: no booking equipment under maintenance
Equipment can have a status of `maintenance` (the HD Projector is one). Right now it can still be booked and still shows up as available. **Add the rule that maintenance equipment cannot be booked**, and make sure it no longer appears as available. Think about all the places this rule needs to apply.

### 4. A short recorded walkthrough (screen recording + your voice)
Record a **short screen recording with your voice** — around 5 minutes, no more than 10. No editing or production polish needed, and any tool works (Loom, OBS, Windows Game Bar, QuickTime, etc.). We're not grading your English or presentation skills (Taglish is fine!), but we do want to see how well you can communicate — how clearly you can explain your own code and the thinking behind it. Cover these four things:

- **Explain your whole Task 1 solution.** Walk us through `rental_days`, `dates_overlap`, and `find_conflicting_booking` — how each one works, and why your implementation matches the business rules, including the same-day-turnover exception.
- **Show your conflict logic working.** In the running app, against the existing Jan 10–15 booking, demonstrate two bookings that are correctly **blocked** and one legitimate same-day turnover that is correctly **allowed**.
- **Your maintenance-equipment choice.** A brief explanation on how you chose to handle maintenance equipment in the UI, and why (Task 3).
- **Anything else worth addressing?** By this point you've probably spent some time running the app and using it the way a customer would. If anything stood out to you as worth addressing, tell us what it was, how you noticed it, and what (if anything) you did about it.

---

## What to send back

- The fixed code, as a git repo with at least **one commit per task or per function touched (as appropriate)** (Tasks 1-3 above, plus anything else you find and fix along the way). We read the commit history as part of the review, not just the final diff, so please write descriptive commit messages; it's the fastest way for us to follow how you got from symptom to root cause.
- Your recorded walkthrough from Task 4 — either the video file itself or a link we can open without an account (e.g. Loom, unlisted YouTube, or a shared Drive link).

Passing the assessment leads to a follow-up call. In that call, **we extend your submitted code together, live, by adding a small feature**. Using whatever tools and resources you normally work with to build this is completely fine; submitting code you can't explain is not. If you understand every line of your submission well enough to work on top of it on the spot, the call will be easy.

Good luck, and thank you!
