# School Management — Streamlit Frontend

Ye sirf **Streamlit** mein bana hua frontend hai jo aap ke pichle FastAPI backend se connect hota hai. Koi aur framework nahi — bas ek `app.py` file hai.

## Zaroori Baat

Ye frontend chalane se pehle **backend (school_backend) alag terminal mein chala hua hona chahiye**, warna records nahi milenge.

## Zip Extract Karna

```bash
unzip school_frontend.zip
cd school_frontend
```

## Step 1: Requirements Install Karein

```bash
pip install -r requirements.txt
```

## Step 2: Backend Pehle Chalayein (agar nahi chala)

Doosri terminal window mein pehle wala backend project chalayein:

```bash
cd school_backend
uvicorn app.main:app --reload
```

Backend `http://127.0.0.1:8000` par chalta rahega.

## Step 3: Streamlit App Run Karein

Is (frontend) folder ki terminal mein:

```bash
streamlit run app.py
```

Browser khud khul jayega — agar na khule to link kholein:

```
http://localhost:8501
```

## Kaise Use Karein

1. Sidebar mein **Backend URL** check karein (default `http://127.0.0.1:8000` hai — agar backend kahin aur chal raha ho to yahan change karein)
2. **View** karna ho (Classes/Teachers/Students/Attendance dekhna) to bina login ke kar sakte hain
3. **Add/Edit/Delete** karna ho to sidebar mein **Admin Login** karein:
   - Email: `admin@school.com`
   - Password: `admin123`
   (Ye backend ki `.env` file mein set hain)
4. Menu se Dashboard, Classes, Teachers, Students, Attendance mein se koi bhi section chun lein

## Features

- 📊 Dashboard — total classes/teachers/students ka overview
- 📚 Classes — add, view, delete
- 👩‍🏫 Teachers — add, view, delete
- 🎓 Students — add, view, edit, delete (class assign karne ke sath)
- 📝 Attendance — mark karna aur student-wise dekhna
- 🔐 Admin login/logout sidebar se
