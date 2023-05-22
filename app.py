import pandas as pd
from pandas import json_normalize
from api_module import *
import streamlit as st
import base64

st.title('Group Member Downlaod')

# 全ユーザー情報取得
users = show_users().json()['value']
#print('Nomber of users are '+ str(len(users)))
df_users = json_normalize(users)
#df_users.to_csv('users.csv')
st.text('User一覧')
st.dataframe(df_users)

#全グループ情報取得
res = get_ad_all_groups()
groups = res.json()['value']
df_groups =json_normalize(groups)
#print('Nomber of group are '+ str(len(groups)))
#df_groups.to_csv('group.csv')
st.text('Group一覧')
st.dataframe(df_groups)

#グループに所属するユーザー情報の取得
for i, row in df_groups.iterrows():
    #print('----------------------')
    res = get_ad_group_menbers(row['id'])
    res.json()
    members = res.json()['value']
    df_members = json_normalize(members)
    #df_members
    if df_members.empty:
        aaa = 'aaa'
        #print(1)
        #st.text('なし')
    else:
        #print(2)
        st.text(row['displayName'])
        #df_members['@odata.type']=row['displayName']
        #df_members['groupName'] = df_members['@odata.type']
        #df_members.to_csv('member' + '_' + row['displayName'] + '.csv')
        display_name = row['displayName']
        #pyprint(df_members)
        st.dataframe(df_members)

        csv = df_members.to_csv(index=False) 
        b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="member_{display_name}.csv" >Download Link</a>'
        st.markdown(f"CSVファイルのダウンロード(utf-8 BOM):  {href}", unsafe_allow_html=True)


