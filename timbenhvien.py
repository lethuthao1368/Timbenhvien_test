import streamlit as st
import pandas as pd
import numpy as np
# from gsheetsdb import connect
import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
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
    #       # Các lựa chọn


# Dùng gspread load danh sách bệnh viện + địa chỉ + các yếu tố đặc biệt
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes= scope)
@st.cache(hash_funcs={service_account.Credentials: lambda _: None})
def get_data():
# credentials = ServiceAccountCredentials.from_json_keyfile_name('timbenhvien-830ed70dcaeb.json', scope)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key('1ysTWh2T1rJXOuYWC7KB9g0cOgyLgFESnK0PbqPMNlsU')
    worksheet1 = sh.get_worksheet(0)
    df_1 = pd.DataFrame(worksheet1.get_all_records())
    return df_1

df_1 = get_data()
st.sidebar.subheader('Bạn đang tìm bệnh viện theo tiêu chí:')
option1 = st.sidebar.radio("", ('Vui lòng lựa chọn ở các ô bên dưới',
    'Khám sức khỏe thông thường/ tổng quát', 'Khám sức khỏe cho người lái xe', 
    'Khám sức khỏe cho người nước ngoài', 'Khám sức khỏe để xuất ngoại', 'Tìm bệnh viện theo chuyên khoa','Cần tư vấn bệnh viện theo triệu chứng'))
if option1 == 'Khám sức khỏe thông thường/ tổng quát':
    df_result = df_1[df_1.iloc[:,5] == 'x'].iloc[:,[1,3,4,8]]
elif option1 == 'Khám sức khỏe cho người lái xe':
    df_result = df_1[df_1.iloc[:,7] == 'x'].iloc[:,[1,3,4,8]]
elif option1 == 'Khám sức khỏe cho người nước ngoài':
    df_result = df_1[df_1.iloc[:,8].str.contains('Thực hiện')].iloc[:,[1,3,4,8]]
elif option1 == 'Khám sức khỏe để xuất ngoại':
    df_result = df_1[df_1.iloc[:,6] == 'x'].iloc[:,[1,3,4,8]]

if option1 != 'Vui lòng lựa chọn ở các ô bên dưới':
    st.dataframe(df_result)

check_box = st.checkbox("Tìm các bệnh viện gần nhất")
if check_box:
    with st.form('bv_gan'):
        diachi_user = st.text_input("Địa chỉ của bạn", 'ví dụ: Lê Hồng Phong, Hồ Chí Minh hoặc Lottemart Cộng Hòa')
        submitted = st.form_submit_button("Tìm")

# options1 = st.sidebar.multiselect('Bạn muốn tìm bệnh viện theo tiêu chí nào?',
# ["Khám sức khỏe thông thường", "Khám sức khỏe cho người nước ngoài", "Khám sức khỏe lái xe"])
# df1 = 'Vui lòng chọn tiêu chí'
# if options1 == ["Khám sức khỏe thông thường"]:
#     df1 = df[df['KSKTT'] == 'x']
# elif options1 == ["Khám sức khỏe cho người nước ngoài"]:
#     df1 = df[df['KSKCYTNN'] == 'x']
# elif options1 == ["Khám sức khỏe lái xe"]:
#     df1 = df[df['KSKLX'] == 'x']

# Update các lựa chọn 
