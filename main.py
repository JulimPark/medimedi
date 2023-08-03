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
    st.title(f"{username}님을 위한 Fill Pill")
    with st.expander('세부입력'):
        pillname = st.selectbox('약이름을 선택하세요',options=['씬지','칼슘','본키','비타민C','오메가3','콜린','B6'])
        pillcount = st.slider('복용량을 입력하세요',1,10,1)
        pilldate = st.date_input('복용일을 선택하세요')
        pilltime = st.time_input('복용시간을 입력하세요')
        pilletc = st.text_input('복용관련 특이사항을 입력하세요')
        eee = (datetime.now()).astimezone(timezone('Asia/Seoul'))
        fff = eee.timestamp()
        
        submit = st.button('등록')
        if submit:
            data_dict = {'복용시간':fff,'복용자':username,'약이름':pillname,'수량':pillcount,'비고':pilletc}
            supabase.table('medimedi').insert(data_dict).execute()
        
    with st.expander('자주 먹는 약'):
        st.button('씬지 1알',on_click=auto_insert,args=('씬지',1))
        st.button('칼슘 3알',on_click=auto_insert,args=('칼슘',3))
        st.button('본키 1알',on_click=auto_insert,args=('본키',1))
        st.button('비타민C 1알',on_click=auto_insert,args=('비타민C',1))
        
        
        
    
    with st.expander('복약 기록'):
        df2 = pill_data_load()
        df2 = df2.loc[:,['약이름','복용시간','수량','비고']]
        for i in range(len(df2.복용시간.to_list())):
            aabb = datetime.fromtimestamp(float(df2.iat[i,1]))
            aabb = aabb.astimezone(timezone('Asia/Seoul'))
            df2.iat[i,1] = aabb.strftime('%Y-%m-%d %H:%M:%S')
        df2
    st.divider()
    st.success(f'{username}님 접속중')
    authenticator.logout('로그아웃')
    
    
    
    
    
    
    
