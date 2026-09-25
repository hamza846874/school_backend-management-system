import streamlit as st
import requests
from datetime import date

# ---------------- Page Config ----------------
st.set_page_config(page_title="School Management System", page_icon="🏫", layout="wide")

# ---------------- Session State ----------------
if "token" not in st.session_state:
    st.session_state.token = None
if "admin_email" not in st.session_state:
    st.session_state.admin_email = None
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://127.0.0.1:8000"


# ---------------- Helper Functions ----------------
def api_url(path: str) -> str:
    return st.session_state.backend_url.rstrip("/") + path


def auth_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def api_get(path):
    try:
        r = requests.get(api_url(path), timeout=10)
        if r.status_code == 200:
            return r.json(), None
        return None, f"Error {r.status_code}: {r.text}"
    except requests.exceptions.ConnectionError:
        return None, "Backend se connect nahi ho saka. Backend URL check karein aur server chala hua hai ya nahi."
    except Exception as e:
        return None, str(e)


def api_post(path, payload, auth=True):
    try:
        r = requests.post(api_url(path), json=payload, headers=auth_headers() if auth else {}, timeout=10)
        if r.status_code in (200, 201):
            return r.json(), None
        return None, f"Error {r.status_code}: {r.text}"
    except requests.exceptions.ConnectionError:
        return None, "Backend se connect nahi ho saka."
    except Exception as e:
        return None, str(e)


def api_put(path, payload):
    try:
        r = requests.put(api_url(path), json=payload, headers=auth_headers(), timeout=10)
        if r.status_code == 200:
            return r.json(), None
        return None, f"Error {r.status_code}: {r.text}"
    except requests.exceptions.ConnectionError:
        return None, "Backend se connect nahi ho saka."
    except Exception as e:
        return None, str(e)


def api_delete(path):
    try:
        r = requests.delete(api_url(path), headers=auth_headers(), timeout=10)
        if r.status_code == 200:
            return True, None
        return False, f"Error {r.status_code}: {r.text}"
    except requests.exceptions.ConnectionError:
        return False, "Backend se connect nahi ho saka."
    except Exception as e:
        return False, str(e)


def is_logged_in():
    return st.session_state.token is not None


# ---------------- Sidebar ----------------
st.sidebar.title("🏫 School System")

st.session_state.backend_url = st.sidebar.text_input(
    "Backend URL", value=st.session_state.backend_url
)

st.sidebar.markdown("---")

# Login / Logout Box
if is_logged_in():
    st.sidebar.success(f"Logged in: {st.session_state.admin_email}")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.admin_email = None
        st.rerun()
else:
    st.sidebar.subheader("Admin Login")
    login_email = st.sidebar.text_input("Email", value="admin@school.com")
    login_password = st.sidebar.text_input("Password", type="password", value="admin123")
    if st.sidebar.button("Login"):
        try:
            r = requests.post(
                api_url("/auth/login"),
                data={"username": login_email, "password": login_password},
                timeout=10,
            )
            if r.status_code == 200:
                st.session_state.token = r.json()["access_token"]
                st.session_state.admin_email = login_email
                st.sidebar.success("Login successful!")
                st.rerun()
            else:
                st.sidebar.error("Email ya password galat hai")
        except requests.exceptions.ConnectionError:
            st.sidebar.error("Backend se connect nahi ho saka")

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Classes", "Teachers", "Students", "Attendance"],
)

# ---------------- Main Title ----------------
st.title("🏫 School Management System")

if not is_logged_in():
    st.info("ℹ️ Aap bina login ke bhi records dekh sakte hain. Add / Edit / Delete ke liye sidebar se **Admin Login** karein.")

st.markdown("---")

# ================= DASHBOARD =================
if page == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)

    classes, _ = api_get("/classes/")
    teachers, _ = api_get("/teachers/")
    students, _ = api_get("/students/")

    with col1:
        st.metric("Total Classes", len(classes) if classes else 0)
    with col2:
        st.metric("Total Teachers", len(teachers) if teachers else 0)
    with col3:
        st.metric("Total Students", len(students) if students else 0)
    with col4:
        st.metric("Status", "🟢 Connected" if classes is not None or teachers is not None else "🔴 Offline")

    st.markdown("### Welcome")
    st.write(
        "Sidebar se menu chun kar Classes, Teachers, Students ya Attendance manage karein. "
        "Records dekhna sab ke liye khula hai, magar Add/Edit/Delete ke liye admin login zaroori hai."
    )

# ================= CLASSES =================
elif page == "Classes":
    st.header("📚 Classes")

    tab1, tab2 = st.tabs(["View Classes", "Add / Delete Class"])

    with tab1:
        classes, err = api_get("/classes/")
        if err:
            st.error(err)
        elif classes:
            st.table(classes)
        else:
            st.info("Abhi tak koi class add nahi hui.")

    with tab2:
        if not is_logged_in():
            st.warning("Class add/delete karne ke liye pehle Admin Login karein.")
        else:
            st.subheader("Nayi Class Add Karein")
            with st.form("add_class_form"):
                name = st.text_input("Class Name (e.g. Class 9-A)")
                section = st.text_input("Section (optional)")
                submitted = st.form_submit_button("Add Class")
                if submitted:
                    if not name:
                        st.error("Class name zaroori hai")
                    else:
                        result, err = api_post("/classes/", {"name": name, "section": section or None})
                        if err:
                            st.error(err)
                        else:
                            st.success(f"Class '{result['name']}' add ho gayi!")
                            st.rerun()

            st.markdown("---")
            st.subheader("Class Delete Karein")
            classes, _ = api_get("/classes/")
            if classes:
                options = {f"{c['name']} (ID: {c['id']})": c["id"] for c in classes}
                choice = st.selectbox("Class chunein", list(options.keys()))
                if st.button("Delete Class"):
                    ok, err = api_delete(f"/classes/{options[choice]}")
                    if err:
                        st.error(err)
                    else:
                        st.success("Class delete ho gayi!")
                        st.rerun()
            else:
                st.info("Delete karne ke liye koi class maujood nahi.")

# ================= TEACHERS =================
elif page == "Teachers":
    st.header("👩‍🏫 Teachers")

    tab1, tab2 = st.tabs(["View Teachers", "Add / Delete Teacher"])

    with tab1:
        teachers, err = api_get("/teachers/")
        if err:
            st.error(err)
        elif teachers:
            st.table(teachers)
        else:
            st.info("Abhi tak koi teacher add nahi hua.")

    with tab2:
        if not is_logged_in():
            st.warning("Teacher add/delete karne ke liye pehle Admin Login karein.")
        else:
            st.subheader("Naya Teacher Add Karein")
            with st.form("add_teacher_form"):
                name = st.text_input("Teacher Name")
                subject = st.text_input("Subject")
                email = st.text_input("Email")
                phone = st.text_input("Phone (optional)")
                submitted = st.form_submit_button("Add Teacher")
                if submitted:
                    if not name or not email:
                        st.error("Naam aur email zaroori hain")
                    else:
                        result, err = api_post(
                            "/teachers/",
                            {"name": name, "subject": subject or None, "email": email, "phone": phone or None},
                        )
                        if err:
                            st.error(err)
                        else:
                            st.success(f"Teacher '{result['name']}' add ho gaya!")
                            st.rerun()

            st.markdown("---")
            st.subheader("Teacher Delete Karein")
            teachers, _ = api_get("/teachers/")
            if teachers:
                options = {f"{t['name']} (ID: {t['id']})": t["id"] for t in teachers}
                choice = st.selectbox("Teacher chunein", list(options.keys()))
                if st.button("Delete Teacher"):
                    ok, err = api_delete(f"/teachers/{options[choice]}")
                    if err:
                        st.error(err)
                    else:
                        st.success("Teacher delete ho gaya!")
                        st.rerun()
            else:
                st.info("Delete karne ke liye koi teacher maujood nahi.")

# ================= STUDENTS =================
elif page == "Students":
    st.header("🎓 Students")

    tab1, tab2, tab3 = st.tabs(["View Students", "Add Student", "Edit / Delete Student"])

    with tab1:
        students, err = api_get("/students/")
        if err:
            st.error(err)
        elif students:
            st.table(students)
        else:
            st.info("Abhi tak koi student add nahi hua.")

    with tab2:
        if not is_logged_in():
            st.warning("Student add karne ke liye pehle Admin Login karein.")
        else:
            classes, _ = api_get("/classes/")
            class_options = {"None": None}
            if classes:
                class_options.update({f"{c['name']} (ID: {c['id']})": c["id"] for c in classes})

            st.subheader("Naya Student Add Karein")
            with st.form("add_student_form"):
                name = st.text_input("Student Name")
                roll_number = st.text_input("Roll Number")
                dob = st.date_input("Date of Birth", value=None)
                email = st.text_input("Email (optional)")
                phone = st.text_input("Phone (optional)")
                class_choice = st.selectbox("Class", list(class_options.keys()))
                submitted = st.form_submit_button("Add Student")
                if submitted:
                    if not name or not roll_number:
                        st.error("Naam aur roll number zaroori hain")
                    else:
                        payload = {
                            "name": name,
                            "roll_number": roll_number,
                            "date_of_birth": str(dob) if dob else None,
                            "email": email or None,
                            "phone": phone or None,
                            "class_id": class_options[class_choice],
                        }
                        result, err = api_post("/students/", payload)
                        if err:
                            st.error(err)
                        else:
                            st.success(f"Student '{result['name']}' add ho gaya!")
                            st.rerun()

    with tab3:
        if not is_logged_in():
            st.warning("Edit/Delete karne ke liye pehle Admin Login karein.")
        else:
            students, _ = api_get("/students/")
            if students:
                options = {f"{s['name']} (Roll: {s['roll_number']})": s for s in students}
                choice = st.selectbox("Student chunein", list(options.keys()))
                student = options[choice]

                st.subheader("Student Update Karein")
                classes, _ = api_get("/classes/")
                class_options = {"None": None}
                if classes:
                    class_options.update({f"{c['name']} (ID: {c['id']})": c["id"] for c in classes})

                current_class_label = "None"
                for label, cid in class_options.items():
                    if cid == student.get("class_id"):
                        current_class_label = label

                with st.form("edit_student_form"):
                    name = st.text_input("Name", value=student["name"])
                    roll_number = st.text_input("Roll Number", value=student["roll_number"])
                    email = st.text_input("Email", value=student.get("email") or "")
                    phone = st.text_input("Phone", value=student.get("phone") or "")
                    class_choice = st.selectbox(
                        "Class", list(class_options.keys()),
                        index=list(class_options.keys()).index(current_class_label)
                    )
                    update_submitted = st.form_submit_button("Update Student")
                    if update_submitted:
                        payload = {
                            "name": name,
                            "roll_number": roll_number,
                            "date_of_birth": student.get("date_of_birth"),
                            "email": email or None,
                            "phone": phone or None,
                            "class_id": class_options[class_choice],
                        }
                        result, err = api_put(f"/students/{student['id']}", payload)
                        if err:
                            st.error(err)
                        else:
                            st.success("Student update ho gaya!")
                            st.rerun()

                st.markdown("---")
                if st.button("🗑️ Delete This Student"):
                    ok, err = api_delete(f"/students/{student['id']}")
                    if err:
                        st.error(err)
                    else:
                        st.success("Student delete ho gaya!")
                        st.rerun()
            else:
                st.info("Koi student maujood nahi.")

# ================= ATTENDANCE =================
elif page == "Attendance":
    st.header("📝 Attendance")

    tab1, tab2 = st.tabs(["Mark Attendance", "View Attendance"])

    with tab1:
        if not is_logged_in():
            st.warning("Attendance mark karne ke liye pehle Admin Login karein.")
        else:
            students, _ = api_get("/students/")
            if students:
                options = {f"{s['name']} (Roll: {s['roll_number']})": s["id"] for s in students}
                with st.form("attendance_form"):
                    choice = st.selectbox("Student chunein", list(options.keys()))
                    att_date = st.date_input("Date", value=date.today())
                    status = st.selectbox("Status", ["present", "absent", "leave"])
                    submitted = st.form_submit_button("Mark Attendance")
                    if submitted:
                        payload = {
                            "student_id": options[choice],
                            "date": str(att_date),
                            "status": status,
                        }
                        result, err = api_post("/attendance/", payload)
                        if err:
                            st.error(err)
                        else:
                            st.success("Attendance mark ho gayi!")
            else:
                st.info("Pehle students add karein.")

    with tab2:
        students, _ = api_get("/students/")
        if students:
            options = {f"{s['name']} (Roll: {s['roll_number']})": s["id"] for s in students}
            choice = st.selectbox("Student chunein (attendance dekhne ke liye)", list(options.keys()), key="view_att")
            records, err = api_get(f"/attendance/{options[choice]}")
            if err:
                st.error(err)
            elif records:
                st.table(records)
            else:
                st.info("Is student ki koi attendance record nahi mili.")
        else:
            st.info("Koi student maujood nahi.")
