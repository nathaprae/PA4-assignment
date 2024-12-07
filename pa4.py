import openai
import streamlit as st
import pandas as pd


st.sidebar.title('API Key')
api_key = st.sidebar.text_input('กรุณากรอก API Key ของท่าน:', type='password')

st.title('แปลภาษาถิ่น เป็นภาษาไทยกลาง')
st.write('เว็บไซต์นี้จะเปลี่ยนคำภาษาถิ่นของประเทศไทย ได้แก่ ภาษาถิ่นเหนือ ภาษาถิ่นอีสาน และภาษาถิ่นใต้ให้เป็นภาษาไทยภาคกลาง พร้อมบอกคำศัพท์ที่น่าสนใจในภาษาถิ่นนั้น ๆ และความหมาย')
input_text = st.text_area('กรุณากรอกข้อความที่ต้องการแปล:')


if st.button('แปล'):
    if api_key and input_text:
        openai.api_key = api_key
        try:
            response_text = openai.chat.completions.create(
            model= 'gpt-4o',
            messages=[
                {'role': 'system', 'content':'คุณคือนักจำแนกภาษาถิ่น 4 ภาคของประเทศไทยและนักแปลคำภาษาถิ่นให้เป็นภาษาไทยภาคกลาง'},
                {'role': 'user', 'content': f"{input_text} เป็นภาษาถิ่นภาคอะไร ให้ตอบขึ้นต้นด้วย ภาษาถิ่น ถ้ามีหลายภาคให้คั่นด้วย และ"
                 "และแปลเป็นภาษาไทยภาคกลางทุกคำ ไม่ต้องอธิบายและใช้รูปแบบการตอบ ชื่อภาษาถิ่น, คำแปลไทย เท่านั้น ห้ามมีคำอื่น ๆ"}
            ],
            )

            result_text = response_text.choices[0].message.content.strip()
            text = result_text.split(',')
            dialect = text[0].strip()
            trans_text = text[1].strip()


            st.subheader('ภาษาถิ่นที่พบ:')
            st.write(dialect)
            st.subheader('คำแปลภาษาไทยกลาง:')
            st.write(trans_text)


            response_words = openai.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {"role": "system", "content": "คุณคือนักแยกคำศัพท์ในภาษาถิ่นไทยที่ต่างจากภาษาไทยกลาง"},
                    {"role": "user", "content": f"กรุณาแยกคำศัพท์ภาษาถิ่นที่พบจากข้อความใน {input_text} ทีละคำ และให้คำแปลไทยภาคกลาง และให้คำอธิบายว่าคำศัพท์จะใช้งานในสถานการณ์ไหนบริบทอะไรโดยไม่ต้องบอกว่าใช้ในภาคไหน"
                    "ไม่ต้องอธิบาย รูปแบบการตอบคือ คำศัพท์ภาษาถิ่น:คำแปล:คำอธิบาย มีหลายคำให้คั่นด้วย ,"}
                ],
            )

            interesting_words = response_words.choices[0].message.content.strip()
            word_by_word = interesting_words.split(',')
            words_list = []
            for word in word_by_word:
                parts = word.split(':')
                if len(parts) == 3:
                    words_list.append({
                    "คำศัพท์ภาษาถิ่น": parts[0].strip(),
                    "คำแปลไทยภาคกลาง": parts[1].strip(),
                    "วิธีการใช้": parts[2].strip()})

            df = pd.DataFrame(words_list)
            df.index = range(1, len(df)+1)
            df.index.names = ["คำที่"]
            
            styled_df = df.style.set_table_styles([
                {"selector": "thead th", "props": [("text-align", "center"),("border", "1px white !important"),
                ("background-color", "#3d3d3d"), ("color", "white")]},
            ]
            )

            if not df.empty:
                st.subheader('คำศัพท์ในภาษาถิ่นและความหมาย:')
                st.write(styled_df.to_html(), unsafe_allow_html=True)
            else:
                st.subheader('คำศัพท์ในภาษาถิ่นและความหมาย:')
                st.write("ไม่พบคำศัพท์ที่น่าสนใจ")

            csv = df.to_csv()
            st.download_button(
            label= "ดาวน์โหลดไฟล์ CSV",
            data = csv,
            file_name = "vocab.csv",
            mime = "text/csv",)
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด {e}")
        
    else:
        st.warning('กรุณาใส่ API Key และข้อความ')