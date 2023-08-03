from datetime import datetime
from pytz import timezone
from supabase import create_client
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

## 온라인 게시용 수파 접속
@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

@st.cache_data
def user_data_load():
    response1= supabase.table('medimedi_user').select('*').execute()
    df = pd.DataFrame(response1.data)
    name = df.name.to_list()
    user_id = df.user_id.to_list()
    user_pass = df.password.to_list()
    return name, user_id,user_pass

name, user_id,user_pass = user_data_load()

names = []
for i in range(len(name)):
    names.append(f"{user_id[i]}({name[i]})")

authenticator = stauth.Authenticate(names,user_id,user_pass,
                                    'Test1','abcdef',cookie_expiry_days=30)


name1, authentication_status, username = authenticator.login('로그인','main')

if authentication_status == False:
    st.error('아이디/비밀번호가 일치하지 않습니다.')
    
if authentication_status == None:
    st.warning('아이디와 비밀번호를 입력하세요')



def auto_insert(pillname,pillcount):
    eee = (datetime.now()).astimezone(timezone('Asia/Seoul'))
    fff = eee.timestamp()
    data_dict = {'복용시간':fff,'복용자':username,'약이름':pillname,'수량':pillcount,'비고':'auto'}
    supabase.table('medimedi').insert(data_dict).execute()
        



if authentication_status:
    
    def pill_data_load():
        response2= supabase.table('medimedi').select('*').eq('복용자',username).execute()
        df2 = pd.DataFrame(response2.data)
        return df2
    df2 = pill_data_load()
    title00 = f"<h1 style='text-align: center;color:green'>{username}님, 안녕하세요!</h1>"
    title0 = f"<h1 style='text-align: center;color:orange;'>MEDIMEDI+</h1>"
    st.markdown(title0,unsafe_allow_html=True)
    st.markdown(title00,unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.subheader(f"가장 최근에 복용한 약: {(df2.약이름.to_list())[-1]}")
    with st.expander('세부입력'):
        pillname = st.selectbox('약 이름을 선택하세요',options=sorted(set(df2.약이름.to_list())))
        pillnew = st.checkbox('원하는 약 이름이 없나요?')
        if pillnew:
            pillname = st.text_input('약 이름을 입력하세요')
        pillcount = st.slider('복용량을 입력하세요',1,10,1)
        pilldate = st.date_input('복용일을 선택하세요')
        pilltime = st.time_input('복용시간을 입력하세요')
        pilletc = st.text_input('복용관련 특이사항을 입력하세요')
        eee = (datetime.now()).astimezone(timezone('Asia/Seoul'))
        fff = eee.timestamp()
        col1,col2,col3 = st.columns(3)
        with col2:
            submit = st.button('등록',use_container_width=True)
        if submit:
            data_dict = {'복용시간':fff,'복용자':username,'약이름':pillname,'수량':pillcount,'비고':pilletc}
            supabase.table('medimedi').insert(data_dict).execute()
            st.experimental_rerun()
    title1 = f"<h3 style='text-align: center;'>필수복용</h3>"
    title2 = f"<h3 style='text-align: center;'>건기식</h3>"
    with st.expander('자주 먹는 약'):
        col1,col2 = st.columns(2)
        with col1:
            st.markdown(title1,unsafe_allow_html=True)
            st.button(':blue[씬지] 1알',on_click=auto_insert,args=('씬지',1),use_container_width=True)
            st.button(':green[칼슘] 3알',on_click=auto_insert,args=('칼슘',3),use_container_width=True)
            st.button(':orange[본키] 2알',on_click=auto_insert,args=('본키',2),use_container_width=True)
        with col2:
            st.markdown(title2,unsafe_allow_html=True)
            st.button('비타민C 1알',on_click=auto_insert,args=('비타민C',1),use_container_width=True)
        
        
        
    
    with st.expander('복약 기록'):
        df2 = df2.loc[:,['약이름','복용시간','수량','비고']]
        for i in range(len(df2.복용시간.to_list())):
            aabb = datetime.fromtimestamp(float(df2.iat[i,1]))
            aabb = aabb.astimezone(timezone('Asia/Seoul'))
            df2.iat[i,1] = aabb.strftime('%Y-%m-%d %H:%M:%S')
        df2 = df2.sort_index(ascending=False)
        df2
    st.divider()
    st.success(f'{username}님 접속중')
    authenticator.logout('로그아웃')
    
    
    
    
    
    
    
