# =====================================================
# IMPORTS
# =====================================================

import streamlit as st
import face_recognition
import cv2
import numpy as np
import os
import pickle
import pandas as pd
from datetime import datetime
import time
from PIL import Image

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Smart Attendance",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main{
    background: linear-gradient(to right,#141e30,#243b55);
    color:white;
}

/* SIDEBAR */

[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#7c3aed,#4c1d95);
    color:white;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

/* SELECT BOX */

div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] input {
    color: white !important;
}

div[data-baseweb="popover"] {
    background-color: #111827 !important;
    color: white !important;
}

/* CARDS */

.metric-card{
    background:linear-gradient(135deg,#06b6d4,#2563eb);
    padding:25px;
    border-radius:20px;
    text-align:center;
    color:white;
    box-shadow:0px 5px 15px rgba(0,0,0,0.3);
}

.feature-card{
    background:#111827;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    box-shadow:0px 5px 15px rgba(0,0,0,0.3);
}

.present-box{
    background:linear-gradient(135deg,#11998e,#38ef7d);
    padding:20px;
    border-radius:20px;
    color:white;
}

.absent-box{
    background:linear-gradient(135deg,#ff416c,#ff4b2b);
    padding:20px;
    border-radius:20px;
    color:white;
}

.footer-box{
    background:#111827;
    padding:25px;
    border-radius:20px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(135deg,#7c3aed,#c026d3);
padding:30px;
border-radius:25px;
text-align:center;
box-shadow:0px 5px 25px rgba(0,0,0,0.4);
">

<h1 style='
font-size:60px;
color:white;
margin-bottom:10px;
'>
🚀 AI SMART ATTENDANCE SYSTEM
</h1>

<h2 style='color:#f3e8ff;'>
🎓 Deogiri Institute of Engineering and Management Studies
</h2>

<h3 style='color:#e9d5ff;'>
💻 Department : AIML
</h3>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# LOAD ENCODINGS
# =====================================================

if os.path.exists("encodings.pkl"):

    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)

    known_encodings = data["encodings"]
    known_names = data["names"]

else:

    st.error("❌ encodings.pkl file not found")
    st.stop()

# =====================================================
# ATTENDANCE FILE
# =====================================================

if not os.path.exists("attendance.csv"):

    df = pd.DataFrame(
        columns=["Name","Date","Time","Lecture","Status"]
    )

    df.to_csv("attendance.csv", index=False)

attendance_df = pd.read_csv("attendance.csv")

# =====================================================
# FIX OLD CSV
# =====================================================

if "Lecture" not in attendance_df.columns:
    attendance_df["Lecture"] = "Lecture 1"

# =====================================================
# STUDENTS
# =====================================================

students = os.listdir("dataset")

total_students = len(students)

today = datetime.now().strftime("%Y-%m-%d")
# =====================================================
# SIDEBAR + LECTURE PANEL CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
SIDEBAR FULL DESIGN
===================================================== */

[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#0f172a,#1e1b4b,#312e81,#7c3aed);
    border-right:3px solid #c084fc;
}

/* SIDEBAR TEXT */

[data-testid="stSidebar"] *{
    color:white !important;
}

/* SIDEBAR TITLE */

.sidebar-title{
    text-align:center;
    font-size:32px;
    font-weight:bold;
    color:white;
    margin-bottom:20px;
    text-shadow:0px 0px 20px #f472b6;
}

/* CURRENT LECTURE BOX */

.lecture-box{
    background: linear-gradient(135deg,#ec4899,#7c3aed,#2563eb);
    padding:20px;
    border-radius:20px;
    margin-top:15px;
    margin-bottom:20px;
    text-align:center;
    color:white;
    box-shadow:0px 0px 25px rgba(236,72,153,0.7);
    animation: lectureGlow 2s infinite alternate;
}

@keyframes lectureGlow{

    from{
        box-shadow:0px 0px 15px rgba(168,85,247,0.5);
    }

    to{
        box-shadow:0px 0px 35px rgba(236,72,153,1);
    }
}

/* CURRENT TIME BOX */

.time-box{
    background: rgba(255,255,255,0.08);
    padding:15px;
    border-radius:15px;
    margin-top:10px;
    border:1px solid rgba(255,255,255,0.2);
    text-align:center;
    font-size:18px;
}

/* CAMERA CHECKBOX */

.stCheckbox{
    background: rgba(255,255,255,0.08);
    padding:15px;
    border-radius:15px;
    margin-top:10px;
}

/* SELECT BOX */

div[data-baseweb="select"] > div{
    background:#111827 !important;
    border:2px solid #c084fc !important;
    border-radius:15px !important;
    color:white !important;
    box-shadow:0px 0px 15px rgba(168,85,247,0.5);
}

div[data-baseweb="select"] input{
    color:white !important;
}

div[data-baseweb="popover"]{
    background:#111827 !important;
    color:white !important;
}

/* RESET BUTTON */

.stButton>button{
    width:100%;
    border-radius:15px;
    background: linear-gradient(135deg,#ef4444,#ec4899);
    color:white;
    font-size:18px;
    font-weight:bold;
    border:none;
    padding:12px;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.03);
    box-shadow:0px 0px 20px rgba(236,72,153,0.9);
}

/* SUCCESS / INFO BOX */

.stAlert{
    border-radius:15px !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TIMETABLE LOGIC
# =====================================================

now = datetime.now()

current_hour = now.hour
current_minute = now.minute

current_total = current_hour * 60 + current_minute

lecture_name = "No Lecture"

# 10:15 to 11:15
if 615 <= current_total <= 675:
    lecture_name = "Lecture 1"

# 11:15 to 12:15
elif 675 <= current_total <= 735:
    lecture_name = "Lecture 2"

# 1:15 PM to 2:15 PM
elif 795 <= current_total <= 855:
    lecture_name = "Lecture 3"

# 2:15 PM to 3:15 PM
elif 855 <= current_total <= 915:
    lecture_name = "Lecture 4"

# 3:30 PM to 4:30 PM
elif 930 <= current_total <= 990:
    lecture_name = "Lecture 5"

# =====================================================
# TODAY DATA
# =====================================================

today_df = attendance_df[
    attendance_df["Date"] == today
]

present_students = today_df["Name"].unique().tolist()

present_count = len(present_students)

attendance_percent = 0

if total_students > 0:

    attendance_percent = (
        present_count / total_students
    ) * 100

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("""
<div class="sidebar-title">
⚙ SMART CONTROL PANEL
</div>
""", unsafe_allow_html=True)

camera_on = st.sidebar.checkbox("📷 Start Camera")

selected_student = st.sidebar.selectbox(
    "👩 Select Student",
    students
)

st.sidebar.markdown(f"""
<div class="lecture-box">

<h2>📚 CURRENT LECTURE</h2>

<h1>{lecture_name}</h1>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="time-box">

📅 <b>{today}</b>

<br><br>

⏰ <b>{datetime.now().strftime('%H:%M:%S')}</b>

</div>
""", unsafe_allow_html=True)

st.sidebar.success("✅ AI Attendance System Active")

if st.sidebar.button("🗑 Reset Attendance"):

    attendance_df = pd.DataFrame(
        columns=["Name","Date","Time","Lecture","Status"]
    )

    attendance_df.to_csv(
        "attendance.csv",
        index=False
    )

    st.sidebar.success("✅ Attendance Reset")

# =====================================================
# DASHBOARD
# =====================================================

st.markdown("## 📊 Attendance Dashboard")

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class='metric-card'>
    <h2>Total Students</h2>
    <h1>{total_students}</h1>
    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class='metric-card'>
    <h2>Present</h2>
    <h1>{present_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with c3:

    absent_count = total_students - present_count

    st.markdown(f"""
    <div class='metric-card'>
    <h2>Absent</h2>
    <h1>{absent_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class='metric-card'>
    <h2>Attendance %</h2>
    <h1>{attendance_percent:.1f}%</h1>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FEATURES
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

f1,f2,f3,f4 = st.columns(4)

with f1:

    st.markdown("""
    <div class='feature-card'>
    🔥
    <h3>AI Recognition</h3>
    <p>Smart Face Detection</p>
    </div>
    """, unsafe_allow_html=True)

with f2:

    st.markdown("""
    <div class='feature-card'>
    📈
    <h3>Analytics</h3>
    <p>Live Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

with f3:

    st.markdown("""
    <div class='feature-card'>
    🛡
    <h3>Security</h3>
    <p>Unknown Face Alert</p>
    </div>
    """, unsafe_allow_html=True)

with f4:

    st.markdown("""
    <div class='feature-card'>
    ☁
    <h3>Cloud Ready</h3>
    <p>Future Deployment</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# COLORFUL ATTRACTIVE TIMETABLE IMAGE DESIGN
# =====================================================

st.markdown("""
<style>

/* MAIN TIMETABLE BOX */

.super-timetable{
    background: linear-gradient(135deg,#0f172a,#1e3a8a,#6d28d9,#db2777);
    padding:30px;
    border-radius:35px;
    margin-top:30px;
    margin-bottom:30px;
    border:4px solid #c084fc;
    box-shadow:0px 0px 40px rgba(168,85,247,0.8);
    animation: glowbox 3s infinite alternate;
}

@keyframes glowbox{
    from{
        box-shadow:0px 0px 20px rgba(168,85,247,0.5);
    }

    to{
        box-shadow:0px 0px 50px rgba(236,72,153,0.9);
    }
}

/* TITLE */

.super-title{
    text-align:center;
    color:white;
    font-size:55px;
    font-weight:bold;
    margin-bottom:10px;
    letter-spacing:2px;
    text-shadow:0px 0px 20px #f472b6;
}

/* SUBTITLE */

.super-subtitle{
    text-align:center;
    color:#fbcfe8;
    font-size:26px;
    margin-bottom:25px;
    font-weight:bold;
}

/* IMAGE FRAME */

.image-frame{
    padding:18px;
    border-radius:30px;
    background: linear-gradient(135deg,#06b6d4,#9333ea,#ec4899,#f59e0b);
    box-shadow:0px 0px 35px rgba(255,255,255,0.3);
}

/* IMAGE EFFECT */

.image-frame img{
    border-radius:25px !important;
    border:6px solid white;
    filter: contrast(115%) brightness(108%) saturate(135%);
    transition:0.5s;
    box-shadow:0px 0px 30px rgba(255,255,255,0.4);
}

/* HOVER EFFECT */

.image-frame img:hover{
    transform:scale(1.03);
    filter: contrast(125%) brightness(115%) saturate(160%);
    box-shadow:0px 0px 60px rgba(236,72,153,1);
}

/* GLOW TEXT */

.glow-text{
    text-align:center;
    margin-top:20px;
    font-size:28px;
    color:#ffffff;
    font-weight:bold;
    animation: glowtext 1.5s infinite alternate;
}

@keyframes glowtext{
    from{
        text-shadow:0px 0px 10px #22d3ee;
    }

    to{
        text-shadow:0px 0px 30px #f472b6;
    }
}

/* FOOTER */

.timetable-bottom{
    margin-top:20px;
    background:rgba(255,255,255,0.12);
    padding:18px;
    border-radius:18px;
    text-align:center;
    color:white;
    font-size:20px;
    border:2px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TIMETABLE UI
# =====================================================

from PIL import Image
import os

image_path = r"c:\Users\morer\Downloads\ChatGPT Image May 12, 2026, 12_51_25 PM.png"

if os.path.exists(image_path):

    image = Image.open(image_path)

    st.markdown("""
    <div class="super-timetable">

    <div class="super-title">
    📚 SMART CLASS TIMETABLE
    </div>

    <div class="super-subtitle">
    🎓 Deogiri Institute of Engineering and Management Studies
    <br>
    💻 Department of CSE (AIML)
    </div>

    </div>
    """, unsafe_allow_html=True)

    left,center,right = st.columns([1,8,1])

    with center:

        st.markdown("""
        <div class="image-frame">
        """, unsafe_allow_html=True)

        st.image(
            image,
            use_container_width=True
        )

        st.markdown("""
        <div class="glow-text">
        ✨ AI Powered Smart Lecture System ✨
        </div>

        <div class="timetable-bottom">
        ⏰ Attendance works only during lecture timings
        <br><br>
        🚀 Live Face Recognition &nbsp;&nbsp;|&nbsp;&nbsp;
        📊 Smart Attendance Tracking &nbsp;&nbsp;|&nbsp;&nbsp;
        🔥 AI Monitoring Dashboard
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

else:

    st.error("❌ Timetable image not found")
# =====================================================
# CAMERA
# =====================================================

st.markdown("---")

st.markdown("## 🎥 Live Camera")

camera_placeholder = st.empty()

if camera_on:

    if lecture_name == "No Lecture":

        st.error("❌ No Lecture Running")

    else:

        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

        if not cap.isOpened():

            st.error("❌ Camera not detected")

        else:

            st.success(
                f"✅ Attendance Active For {lecture_name}"
            )

            stop_btn = st.button("🛑 Stop Camera")

            while True:

                if stop_btn:
                    break

                ret, frame = cap.read()

                if not ret:
                    st.error("❌ Camera Error")
                    break

                frame = cv2.flip(frame,1)

                small_frame = cv2.resize(
                    frame,
                    (0,0),
                    fx=0.5,
                    fy=0.5
                )

                rgb_small = cv2.cvtColor(
                    small_frame,
                    cv2.COLOR_BGR2RGB
                )

                face_locations = face_recognition.face_locations(
                    rgb_small,
                    model="hog"
                )

                face_encodings = face_recognition.face_encodings(
                    rgb_small,
                    face_locations
                )

                for face_encoding, face_location in zip(
                    face_encodings,
                    face_locations
                ):

                    matches = face_recognition.compare_faces(
                        known_encodings,
                        face_encoding,
                        tolerance=0.50
                    )

                    face_distances = face_recognition.face_distance(
                        known_encodings,
                        face_encoding
                    )

                    best_match_index = np.argmin(face_distances)

                    name = "Unknown"

                    if matches[best_match_index]:

                        name = known_names[best_match_index]

                        already_exists = (
                            (attendance_df["Name"] == name)
                            &
                            (attendance_df["Date"] == today)
                            &
                            (attendance_df["Lecture"] == lecture_name)
                        ).any()

                        if not already_exists:

                            now = datetime.now()

                            new_row = pd.DataFrame([{
                                "Name": name,
                                "Date": now.strftime("%Y-%m-%d"),
                                "Time": now.strftime("%H:%M:%S"),
                                "Lecture": lecture_name,
                                "Status": "Present"
                            }])

                            attendance_df = pd.concat(
                                [attendance_df,new_row],
                                ignore_index=True
                            )

                            attendance_df.to_csv(
                                "attendance.csv",
                                index=False
                            )

                            st.toast(
                                f"✅ Attendance Marked : {name}"
                            )

                    top,right,bottom,left = face_location

                    top *= 2
                    right *= 2
                    bottom *= 2
                    left *= 2

                    color = (0,255,0)

                    if name == "Unknown":
                        color = (0,0,255)

                    cv2.rectangle(
                        frame,
                        (left,top),
                        (right,bottom),
                        color,
                        3
                    )

                    cv2.rectangle(
                        frame,
                        (left,bottom-35),
                        (right,bottom),
                        color,
                        cv2.FILLED
                    )

                    cv2.putText(
                        frame,
                        name,
                        (left+6,bottom-6),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255,255,255),
                        2
                    )

                camera_placeholder.image(
                    frame,
                    channels="BGR",
                    use_container_width=True
                )

                time.sleep(0.03)

            cap.release()

# =====================================================
# PRESENT / ABSENT
# =====================================================

st.markdown("---")

p1,p2 = st.columns(2)

with p1:

    st.markdown("""
    <div class='present-box'>
    <h2>✅ Present Students</h2>
    </div>
    """, unsafe_allow_html=True)

    if len(present_students) > 0:

        for student in present_students:
            st.success(f"✅ {student}")

    else:
        st.warning("No Present Students")

with p2:

    st.markdown("""
    <div class='absent-box'>
    <h2>❌ Absent Students</h2>
    </div>
    """, unsafe_allow_html=True)

    real_absent = []

    for student in students:

        if student not in present_students:
            real_absent.append(student)

    if len(real_absent) > 0:

        for student in real_absent:
            st.error(f"❌ {student}")

    else:

        st.success("✅ No Absent Students")

# =====================================================
# RECORDS
# =====================================================

st.markdown("---")

st.markdown("## 📝 Attendance Records")

latest_df = attendance_df.drop_duplicates(
    subset=["Name","Date","Lecture"],
    keep="last"
)

st.dataframe(
    latest_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = attendance_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Attendance CSV",
    csv,
    "attendance.csv",
    "text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class='footer-box'>

<h2>🚀 Advanced Features Included</h2>

✔ Real-time Face Recognition<br>
✔ Timetable Based Attendance<br>
✔ Lecture-wise Attendance<br>
✔ AI Smart Dashboard<br>
✔ Present / Absent Detection<br>
✔ Unknown Face Detection<br>
✔ Download Attendance CSV<br>
✔ Attractive Modern UI<br>
✔ Duplicate Entry Prevention<br>

</div>
""", unsafe_allow_html=True)