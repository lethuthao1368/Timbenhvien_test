import streamlit as st
import pandas as pd
import numpy as np
# from gsheetsdb import connect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
st.title("demo TÌM BỆNH VIỆN")
st.image('Picture\TIM BENH VIEN.png',width = 600)
#     # Đọc data từ sheet dùng gsheetsdb
# conn = connect()
# def run_query(query):
#     rows = conn.execute(query, headers=1)
#     return rows
# sheet_url = st.secrets["public_gsheets_url"]
# rows = run_query(f'SELECT * FROM "{sheet_url}"')
# #Đọc data từ dạng query sang dạng pandas
# df = pd.DataFrame(rows.fetchall())
# st.write(pd.DataFrame(df.values, columns = ['STT', 'Điền', 'KẾT QUẢ', 2,6,7,8,9,0,1]))
## Các lựa chọn
# st.sidebar.markdown("## Nhập thông tin")
# options1 = st.sidebar.multiselect('Bạn muốn tìm bệnh viện theo tiêu chí nào?',
# ["Khám sức khỏe thông thường", "Khám sức khỏe cho người nước ngoài", "Khám sức khỏe lái xe"])
# df1 = 'Vui lòng chọn tiêu chí'
# if options1 == ["Khám sức khỏe thông thường"]:
#     df1 = df[df['KSKTT'] == 'x']
# elif options1 == ["Khám sức khỏe cho người nước ngoài"]:
#     df1 = df[df['KSKCYTNN'] == 'x']
# elif options1 == ["Khám sức khỏe lái xe"]:
#     df1 = df[df['KSKLX'] == 'x']
# st.write(df1)

# Dùng gspread load danh sách bệnh viện + địa chỉ + các yếu tố đặc biệt
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'timbenhvien-830ed70dcaeb.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1ysTWh2T1rJXOuYWC7KB9g0cOgyLgFESnK0PbqPMNlsU')
worksheet1 = sh.get_worksheet(0)
df_1 = pd.DataFrame(worksheet1.get_all_records())
st.write(df_1)
# 