import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
#sym_df
@st.cache
def get_sym_df(url1):
  sym_df = pd.read_csv(url1)
  sym_df = sym_df.loc[:,('eng','viet')]
  return sym_df

#dis_df
@st.cache
def get_dis_df(url1):
  dis_df = pd.read_csv(url1)
  dis_df = dis_df.loc[:,('id_diseases', 'eng', 'viet', 'bv_tuong_ung')]
  return dis_df

#train_df
@st.cache(allow_output_mutation=True)
def get_train_df(url1):
  train_df = pd.read_csv(url1)
  train_df['vector'] = train_df.iloc[:,-133:-1].apply(lambda x: list(x), axis=1) ## sau nay nen tong quat hoa cac con so 133, 1, ...
  return train_df

#load data_chan doan benh
url_train_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/train_df.csv'
url_dis_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/diseases_df.csv'
url_sym_df = 'https://raw.githubusercontent.com/Ha-Huynh-Anh/Timbenhvien_test/main/data/sym_df.csv'

sym_df = get_sym_df(url_sym_df)
dis_df = get_dis_df(url_dis_df)
train_df = get_train_df(url_train_df)
# function to translate sym vie - eng:
def trans_sym(list_sym):
    """
    translate sym from list vie to list eng
    input: ['Yếu mệt','Da nổi mẩn']
    output: ['lethargy', 'nodal_skin_eruptions']
    """
    list_eng = []
    for i in list_sym:
        if i in list(sym_df.viet):
            index = list(sym_df.viet).index(i)
            list_eng.append(list(sym_df.eng)[index])
    return list_eng

# sym_to_vector(sym_input_eng)
# convert to array format
def sym_to_vector(list_input_sym):
    #  to convert sym to vector
    sym_input_vector = []    
    for i in list(sym_df.eng): 
        if i in list_input_sym:
            sym_input_vector.append(1)
        else:
            sym_input_vector.append(0)
    return sym_input_vector

# convert all into list
def get_disease(train_df, input_array):
    
    # cal similarity
    train_df['similar'] = train_df.vector.apply(lambda x: cosine_similarity(input_array,np.array([x]))[0][0])

    # disease result
    dis_result = train_df[train_df['similar'] > 0]
    return dis_result.groupby('prognosis').max('similar').iloc[:,-1].sort_values(ascending=False)    

list_disease_eng = dis_df.eng.to_list()
list_disease_vie = dis_df.viet.to_list()
list_disease_id = dis_df.id_diseases.to_list()

# convert disease to vie
def disease_to_vie(dis_eng):
    if dis_eng in list_disease_eng:
        index = list_disease_eng.index(dis_eng)
        return list_disease_vie[index]
def disease_to_id(dis_eng):
    if dis_eng in list_disease_eng:
        index = list_disease_eng.index(dis_eng)
        return list_disease_id[index]
#Lay ID benh vien tuong ung voi ID benh
def get_hopital_list(dis_id):
    bv_id = dis_df[dis_df.id_diseases == dis_id].bv_tuong_ung
    bv_id = list(bv_id)[0]
    bv_id = bv_id.split(sep = ';')
    return bv_id

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
elif option1 == 'Cần tư vấn bệnh viện theo triệu chứng':
    sym_input_vie = st.multiselect('Các triệu chứng của bạn', sym_df.viet.values)
    # translate vie into eng
    sym_input_eng = trans_sym(sym_input_vie)
    #convert to vector
    input_array = np.array([sym_to_vector(sym_input_eng)])
    output_disease_eng =  get_disease(train_df,input_array)
    output_disease_eng = output_disease_eng.reset_index()
    # create table
    output_disease_eng['viet'] = output_disease_eng.prognosis.apply(lambda x: disease_to_vie(x))
    output_disease_eng['id'] = output_disease_eng.prognosis.apply(lambda x: disease_to_id(x))
    st.markdown(':hospital: Bạn có thể cần được khám về ')
    for i in output_disease_eng.index:
        see_hospital = st.checkbox(output_disease_eng.iloc[i,2])
        if see_hospital:
            id_bv = get_hopital_list(output_disease_eng.iloc[i,3])

if option1 not in ['Vui lòng lựa chọn ở các ô bên dưới','Cần tư vấn bệnh viện theo triệu chứng'] :
    st.dataframe(df_result)

check_box = st.sidebar.checkbox("Tìm các bệnh viện gần nhất")
if check_box:
    with st.sidebar.form('bv_gan'):
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
