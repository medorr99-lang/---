import streamlit as st
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة اختبارات عبد الحميد", layout="wide")

st.title("📝 منصة الاختبارات التفاعلية")
st.sidebar.header("لوحة تحكم المعلم")

# 1. رفع ملف الأسئلة من قبلك أو عرض ملف موجود
uploaded_file = st.sidebar.file_uploader("ارفع ملف الأسئلة (PDF)", type="pdf")

# 2. إدخال الإجابات الصحيحة (نموذج الإجابة)
st.sidebar.subheader("نموذج الإجابة الصحيحة")
num_questions = st.sidebar.number_input("عدد الأسئلة", min_value=1, max_value=50, value=5)
correct_answers = {}
for i in range(1, num_questions + 1):
    correct_answers[str(i)] = st.sidebar.selectbox(f"إجابة س{i}", ["أ", "ب", "ج", "د"], key=f"ans_{i}")

# تقسيم الشاشة لجزئين
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📄 ورقة الأسئلة")
    if uploaded_file:
        # عرض ملف PDF داخل الموقع
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info("الرجاء رفع ملف PDF من القائمة الجانبية ليظهر هنا.")

with col2:
    st.subheader("✍️ خانة الإجابة")
    student_name = st.text_input("اسم الطالب")
    student_answers = {}
    
    for i in range(1, num_questions + 1):
        student_answers[str(i)] = st.radio(f"إجابة السؤال رقم ({i}):", ["أ", "ب", "ج", "د"], horizontal=True, key=f"q_{i}")

    if st.button("إرسال الإجابة والحصول على النتيجة"):
        if not student_name:
            st.error("يرجى كتابة اسمك أولاً")
        else:
            score = 0
            for i in range(1, num_questions + 1):
                if student_answers[str(i)] == correct_answers[str(i)]:
                    score += 1
            
            st.success(f"أحسنت يا {student_name}!")
            st.metric("درجتك النهائية هي:", f"{score} من {num_questions}")
            if score == num_questions:
                st.balloons()