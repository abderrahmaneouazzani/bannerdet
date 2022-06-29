import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import pymysql
import s3fs






icon=Image.open("download.png")
st.set_page_config(page_title="Web Banners Stats",layout="wide",page_icon=icon,initial_sidebar_state="collapsed")

fs = s3fs.S3FileSystem()

hide_menu_style="""
               <style>
               #MainMenu {visibility : hidden ;}
               footer {visibility : hidden ;}
               </style>
               """

z1,z2,z3=st.columns((1,1,1))
st.session_state.pages=["home","Advertisers' Occurence","Web advertisers' insights"]


st.session_state.current_page = z2.radio(
    '',
    st.session_state.pages,
)
st.markdown(hide_menu_style, unsafe_allow_html=True)



#nav=st.radio("Navigations",["home","Web advertiser's insights","Advertiser's Occurence"])





st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)




def occurence_page():
    r1, r2, r3 = st.columns((0.75, 1, 0.75))
    r2.title("Occurences' Statistques")


    i1, i2, i3, i4 = st.columns(4)
    o1, o2 = st.columns(2)
    st.sidebar.header("Additional filters")
    Start_day = i1.selectbox('select starting day ', options=df['day'].unique())
    End_day = i2.selectbox('select ending day', options=df['day'].unique())
    Start_hour = i3.selectbox('select starting hour ', options=df['hour'].unique())
    End_hour = i4.selectbox('select ending hour', options=df['hour'].unique())
    advertiser = st.sidebar.multiselect('select advertiser', options=df['advertiser'].unique(),
                                        default=df['advertiser'].unique())
    page = o1.multiselect('select banners page level', options=df['page'].unique(), default=df['page'].unique())
    type = o2.multiselect('select banners type', options=df['type'].unique(), default=df['type'].unique())

    df_selection = df.query(
        "page==@page & type==@type & advertiser ==@advertiser & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour "
    )

    dfResume = pd.DataFrame(columns=['advertiser', 'occurence'])
    dfsites = pd.DataFrame(columns=['site', 'occurence'])

    count1 = pd.Series(df_selection['advertiser']).value_counts()
    count2 = pd.Series(df_selection['site']).value_counts()
    advertiserresults = {}
    sitesoccurence = {}
    for item in df_selection['advertiser']:
        advertiserresults[item] = count1[item]
    for item in df_selection['site']:
        sitesoccurence[item] = count2[item]
    i = 0
    for key in advertiserresults:
        dfResume.loc[i] = [key, advertiserresults[key]]
        i += 1
    i = 0
    for key in sitesoccurence:
        dfsites.loc[i] = [key, sitesoccurence[key]]
        i += 1
    b = alt.Chart(dfResume, title="Advertisers' Occurence").mark_bar().encode(x="advertiser", y="occurence",
                                                                              tooltip=["advertiser", "occurence"])
    p = alt.Chart(dfsites, title="sites' Occurence").mark_bar().encode(x="site", y="occurence",
                                                                 tooltip=["site", "occurence"])
    f1,f2=st.columns((1,2))
    f1.dataframe(dfResume)
    f2.altair_chart(b, use_container_width=True)
    st.write('#')
    h1, h2 = st.columns((1,2))
    h1.dataframe(dfsites)
    h2.altair_chart(p, use_container_width=True)

def adsDisplay(advertisername,adsNumber):
    df_selection = df.query(
        "page==@page & type==@type & advertiser ==@advertiser & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour "
    )


    dfResume = pd.DataFrame(columns=['advertiser', 'occurence'])

    count1 = pd.Series(df_selection['advertiser']).value_counts()

    advertiserresults = {}
    for item in df_selection['advertiser']:
        advertiserresults[item] = count1[item]
    i = 0
    for key in advertiserresults:
        dfResume.loc[i] = [key, advertiserresults[key]]
        i += 1
    A1,A2 = st.columns(2)
    B1,B2=st.columns(2)


    if adsNumber >= int(dfResume.loc[dfResume['advertiser']==advertisername]['occurence']):

        ads=df_selection.loc[df['advertiser']==advertisername]['adlink']
        w=0
        for ad in ads :


            with fs.open(ad) as f:

                f=Image.open(f)
                if w == 0:
                    A1.image(f)
                if w == 1:
                    A2.image(f)
                if w == 2:
                    B1.image(f)
                if w == 3:
                    B2.image(f)
                w += 1
    else:

        ads=df_selection.loc[df_selection['advertiser']==advertisername]['adlink'][:adsNumber]
        w=0
        for ad in ads :

            with fs.open(ad) as f:
                f=Image.open(f)
                if w==0:
                    A1.image(f)
                if w==1:
                    A2.image(f)
                if w==2:
                    B1.image(f)
                if w==3:
                    B2.image(f)
                w+=1
                if w==4:
                    st.image(f)





a1,a2=st.columns(2)



conn=pymysql.connect(host='localhost',port=int(3306),user='root',passwd='P@ssw0rd123',db='bannersdetection')

cursor=conn.cursor()


sql="SELECT * FROM detections"
cursor.execute(sql)
df = cursor.fetchall()
df=pd.DataFrame(df,columns=['advertiser', 'type', 'page', 'site', 'day','hour','adlink'])














if st.session_state.current_page=="Web advertisers' insights" :

    r1, r2, r3 = st.columns((0.75, 1, 0.75))
    i1, i2, i3, i4 = st.columns(4)
    o1, o2 = st.columns(2)
    q1, q2, q3 = st.columns((1, 3, 1))

    r2.title("Advertisers' Detailed Insights")
    st.sidebar.header("Additional filters")
    Start_day = i1.selectbox('select starting day ', options=df['day'].unique())
    End_day = i2.selectbox('select ending day', options=df['day'].unique())
    Start_hour = i3.selectbox('select starting hour ', options=df['hour'].unique())
    End_hour = i4.selectbox('select ending hour', options=df['hour'].unique())
    advertiser = st.sidebar.multiselect('select advertiser', options=df['advertiser'].unique(),
                                        default=df['advertiser'].unique())
    page = o1.multiselect('select banners page level', options=df['page'].unique(), default=df['page'].unique())
    type = o2.multiselect('select banners type', options=df['type'].unique(), default=df['type'].unique())

    df_selection = df.query(
        "page==@page & type==@type & advertiser ==@advertiser & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour "
    )

    advertisers = df_selection["advertiser"].unique()

    st.write('#')
    q2.dataframe(df_selection.iloc[:, :-1])
    response = st.text_input('insert advertiser here for a sample of ads:')
    if response in advertisers:
        adsDisplay(response, 5)







elif st.session_state.current_page=="Advertisers' Occurence" :
    occurence_page()



elif st.session_state.current_page=="home":
    st.markdown('#')
    st.markdown('#')
    w1,w2,w3=st.columns((1.6,1,1))
    t1, t2, t3 = st.columns((1,1,1))
    u1, u2, u3 = st.columns((1.1,1,1))
    p1, p2, p3 = st.columns((1.5,1,1))
    m1, m2, m3 = st.columns((1, 1, 1))

    w2.subheader("Welcome to")
    t2.title("Web banners Statistiques")
    u2.write("This is a site for web banners statistiques and detailed insights ")
    st.markdown('#')
    f = Image.open("download.png")
    p2.image(f)





