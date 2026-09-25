# School Management Backend (Python + FastAPI)

Ye ek simple school backend hai jo FastAPI aur SQLite ka use karta hai.
Isme **Students, Teachers, Classes, aur Attendance** ke CRUD APIs hain.

Isme **login system (JWT)**, **.env configuration**, aur **Students, Teachers, Classes, Attendance** ke CRUD APIs hain.

- GET (list/view) APIs **public** hain — koi bhi dekh sakta hai
- POST / PUT / DELETE APIs **admin login** maangti hain

## Zip Extract Karna

Pehle zip file ko extract karein:

```bash
unzip school_backend.zip
cd school_backend
```

## Step 1: Python Install Check Karein

```bash
python3 --version
```

(Agar Python install nahi hai, to python.org se install kar lein — version 3.9+ hona chahiye)

## Step 2: Virtual Environment Banayein (recommended)

```bash
python3 -m venv venv
```

Activate karein:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

## Step 3: Requirements Install Karein

```bash
pip install -r requirements.txt
```

## Step 4: .env File Check Karein

Project mein `.env` file already maujood hai default settings ke sath. Aap chahein to apni marzi ki values daal sakte hain:

```env
APP_NAME=School Management Backend
DATABASE_URL=sqlite:///./school.db
SECRET_KEY=your-super-secret-key-change-this-in-production
ADMIN_EMAIL=admin@school.com
ADMIN_PASSWORD=admin123
```

⚠️ **Production mein `SECRET_KEY` aur `ADMIN_PASSWORD` zaroor change karein.**

Agar `.env` file delete ho jaye to `.env.example` ko copy kar ke naam `.env` rakh dein:

```bash
cp .env.example .env
```

## Step 5: Server Run Karein

```bash
uvicorn app.main:app --reload
```

Server chalne ke baad aap ko terminal mein ye milega:

```
Uvicorn running on http://127.0.0.1:8000
```

## Step 6: APIs Test Karein

Browser mein ye link kholein:

```
http://127.0.0.1:8000/docs
```

Yahan Swagger UI khulega jahan se aap seedhe tamam APIs test kar sakte hain.

### Pehle Login Karein (Admin APIs ke liye)

1. `/docs` page par upar right corner mein **"Authorize"** button dabayein
2. Username mein: `admin@school.com`
3. Password mein: `admin123`
4. **Authorize** dabayein — ab aap Add/Update/Delete APIs bhi use kar sakte hain

(Ye credentials `.env` file mein change kiye ja sakte hain)

## Available Endpoints

| Method | Endpoint | Kaam | Login Chahiye? |
|--------|----------|------|-----------------|
| POST | /auth/login | Admin login | Nahi |
| POST | /classes/ | Nayi class add karna | Haan |
| GET | /classes/ | Sari classes dekhna | Nahi |
| DELETE | /classes/{id} | Class delete karna | Haan |
| POST | /teachers/ | Naya teacher add karna | Haan |
| GET | /teachers/ | Sare teachers dekhna | Nahi |
| DELETE | /teachers/{id} | Teacher delete karna | Haan |
| POST | /students/ | Naya student add karna | Haan |
| GET | /students/ | Sare students dekhna | Nahi |
| GET | /students/{id} | Ek student dekhna | Nahi |
| PUT | /students/{id} | Student update karna | Haan |
| DELETE | /students/{id} | Student delete karna | Haan |
| POST | /attendance/ | Attendance mark karna | Haan |
| GET | /attendance/{student_id} | Student ki attendance dekhna | Nahi |

## Database

Database automatically `school.db` (SQLite file) ke naam se project folder mein ban jaayegi — koi alag se setup nahi chahiye.

## Agla Qadam (Optional)

- Login/Authentication add karna (JWT)
- PostgreSQL ya MySQL par switch karna production ke liye
- Frontend (React/Vue) connect karna
