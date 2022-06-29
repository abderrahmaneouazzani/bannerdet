import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import pymysql
import s3fs










icon=Image.open("icon.png")

st.set_page_config(page_title="Web Banners Stats",layout="wide",page_icon=icon,initial_sidebar_state="collapsed")

fs = s3fs.S3FileSystem()



st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


hide_menu_style="""
               <style>
               #MainMenu {visibility : hidden ;}
               footer {visibility : hidden ;}
               </style>
               """


st.markdown(hide_menu_style, unsafe_allow_html=True)












def occurence_page():
    r1, r2, r3 ,r4= st.columns((0.2,0.5,1,0.25))
    r1.image(icon)
    r3.title("Web Banners Stats")
    i1, i2, i3, i4 = st.columns(4)
    o1, o2 = st.columns(2)
    Start_day = i1.selectbox('select starting day ', options=sorted(df['day'].unique()),index=len(df['day'].unique())-1)
    End_day = i2.selectbox('select ending day', options=sorted(df['day'].unique()),index=len(df['day'].unique())-1)
    Start_hour = i3.selectbox('select starting hour ', options=sorted(df.loc[df.query('day<= @End_day & day>= @Start_day').index]['hour'].unique()),index=0)
    End_hour = i4.selectbox('select ending hour', options=sorted(df.loc[df.query('day<= @End_day & day>= @Start_day').index]['hour'].unique())
                            ,index=len(sorted(df.loc[df.query('day<= @End_day & day>= @Start_day').index]['hour'].unique()))-1)
    page = o1.multiselect('select banners page level', options=df['page'].unique(), default=df['page'].unique())
    type = o2.multiselect('select banners type', options=df['type'].unique(), default=df['type'].unique())
    s1,s2 =st.columns(2)
    df_advertiser = df.query(
        "page==@page & type==@type  & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour  "
    )
    advertiser= s1.multiselect('select advertiser', options=df_advertiser['advertiser'].unique(),
                default=df_advertiser['advertiser'].unique())
    Editor = s2.multiselect('select editor', options=df_advertiser['site'].unique(), default=df_advertiser['site'].unique())

    NumberOfAdvertisers = st.selectbox('select number of advertisers ', options=['5', '10', '15', '20'])
    df_selection = df.query(
        "page==@page & type==@type & advertiser ==@advertiser & day <= @End_day & day >= @Start_day & hour <= @End_hour & hour >= @Start_hour & site==@Editor "
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
        dfResume.loc[i] = [key, advertiserresults[key].astype(float)]
        i += 1
    i = 0
    for key in sitesoccurence:
        dfsites.loc[i] = [key, sitesoccurence[key]]
        i += 1
    st.markdown('#')
    if len(dfResume['advertiser'])>0:
        b = alt.Chart(dfResume.nlargest(int(NumberOfAdvertisers), 'occurence'), title="Occurence des top "+NumberOfAdvertisers+" annonceurs").mark_bar().encode(x=alt.X("occurence",
                                                                                axis=alt.Axis(title="Nb d'occurence")), y=alt.Y("advertiser",sort='-x'),
                                                                                  tooltip=["advertiser", "occurence"]).properties(height=300)
        p = alt.Chart(dfsites, title="Occurence des sites").mark_arc().encode(theta=alt.Theta(field="occurence", type="quantitative"),
        color=alt.Color(field="site", type="nominal"),tooltip=["site", "occurence"])

        f1,f2=st.columns((1,2))
        f1.altair_chart(p, use_container_width=True)
        f2.altair_chart(b, use_container_width=True)
        advertisers = df_selection["advertiser"].unique()
        response = st.text_input('insert advertiser name here for a sample of ads:')
        adsNumber=20
        advertisername=response
        if response in advertisers:
            A1, A2 , A3 = st.columns(3)
            B1, B2 , B3 = st.columns(3)
            C1, C2, C3 = st.columns(3)
            D1, D2, D3 = st.columns(3)
            E1, E2 ,E3 = st.columns(3)
            F1, F2, F3 = st.columns(3)
            alldays =[]
            for day in fs.ls("detectedads/" + advertisername+'/'):
                alldays.append(day.split('/')[2])
            days=[]
            for day in alldays:
                if day <=End_day and day >=Start_day:
                    days.append(day)
            adsnum=0
            for day in days :
                adsnum+=len(fs.ls("detectedads/" + advertisername+'/'+day+'/'))

            if adsNumber > adsnum:
                ADS=[]
                for day in days :
                    if len(fs.ls("detectedads/" + advertisername + '/' + day + '/')) > 0:
                        ads=fs.ls("detectedads/" + advertisername + '/' + day + '/')
                        for ad in ads:
                             ADS.append(ad)
                w = 0
                for ad in ADS:
                    k=0
                    with fs.open(ad) as f:

                        f = Image.open(f)

                        if w == 0:
                            A1.image(f)
                            k= 1
                        if w == 1:
                            A2.image(f)
                            k= 1
                        if w == 2:
                            A3.image(f)
                            k= 1
                        if w == 3:
                            B1.image(f)
                            k= 1
                        if w== 4:
                            B2.image(f)
                            k= 1
                        if w== 5:
                            B3.image(f)
                            k= 1
                        if w == 6:
                            C1.image(f)
                            k= 1
                        if w == 7:
                            C2.image(f)
                            k= 1
                        if w == 8:
                            C3.image(f)
                            k= 1
                        if w == 9:
                            D1.image(f)
                            k= 1
                        if w== 10:
                            D2.image(f)
                            k= 1
                        if w== 11:
                            D3.image(f)
                            k= 1
                        if w == 12:
                            E1.image(f)
                            k= 1
                        if w == 13:
                            E2.image(f)
                            k= 1
                        if w == 14:
                            E3.image(f)
                            k= 1
                        if w == 15:
                            F1.image(f)
                            k= 1
                        if w== 16:
                            F2.image(f)
                            k= 1
                        if w== 17:
                            F3.image(f)
                            k=1
                        if k==1:
                            w+=1
            else:
                ADS=[]

                for day in days:
                    if len(fs.ls("detectedads/" + advertisername + '/' + day + '/'))>0:
                        ads = fs.ls("detectedads/" + advertisername + '/' + day + '/')
                        for ad in ads:
                            ADS.append(ad)
                w = 0
                num = 0
                VAR=ADS[:adsNumber]
                for ad in VAR:
                    k=0
                    with fs.open(ad) as f:
                        f=Image.open(f)

                        if w == 0:
                            A1.image(f)
                            k= 1
                        if w == 1:
                            A2.image(f)
                            k= 1
                        if w == 2:
                            A3.image(f)
                            k= 1
                        if w == 3:
                            B1.image(f)
                            k= 1
                        if w == 4:
                            B2.image(f)
                            k= 1
                        if w == 5:
                            B3.image(f)
                            k= 1
                        if w == 6:
                            C1.image(f)
                            k= 1
                        if w == 7:
                            C2.image(f)
                            k= 1
                        if w == 8:
                            C3.image(f)
                            k= 1
                        if w == 9:
                            D1.image(f)
                            k= 1
                        if w== 10:
                            D2.image(f)
                            k= 1
                        if w== 11:
                            D3.image(f)
                            k= 1
                        if w == 12:
                            E1.image(f)
                            k= 1
                        if w == 13:
                            E2.image(f)
                            k= 1
                        if w == 14:
                            E3.image(f)
                            k= 1
                        if w == 15:
                            F1.image(f)
                            k= 1
                        if w== 16:
                            F2.image(f)
                            k= 1
                        if w== 17:
                            F3.image(f)
                            k= 1
                        if k==1:
                            w+=1
                        if k ==0 :
                            num+=1
                            VAR = ADS[num:adsNumber+num]

    values = ['<select>']
    b1, b2, b3 = st.columns(3)
    b2.subheader('Undetected ads')
    day = st.selectbox('select day ', options=values + sorted(df2['day'].unique()), index=0)
    if day != '<select>' and (response not in advertisers):
        nondetected_imgs = df2[df2['day'] == day]['adlink']
        def paginator(label, items, items_per_page=50, on_sidebar=False):
            if on_sidebar:
                location = st.sidebar.empty()
            else:
                location = st.empty()
            items = list(items)
            n_pages = len(items)
            n_pages = (len(items) - 1) // items_per_page + 1
            page_format_func = lambda i: "Page %s" % i
            if 'page_number' not in st.session_state:
                st.session_state['page_number'] = 0
            q1,q2=st.columns((1,0.000000000000000000001))
            a1, a2, a3,a4 = st.columns((1, 1, 1,1))
            if a4.button('Next'):
              st.session_state['page_number'] += 1
            if a1.button('Previous'):
                #if 'page_number' in st.session_state:
               st.session_state['page_number'] -= 1
            min_index = st.session_state['page_number'] * items_per_page
            max_index = min_index + items_per_page
            import itertools
            if min_index < len(items) and max_index < len(items):
                return itertools.islice(enumerate(items), min_index, max_index)
            else :
                return itertools.islice(enumerate(items), 0, items_per_page)
        image_iterator = paginator("Select page", nondetected_imgs)
        indices_on_page, images_on_page = map(list, zip(*image_iterator))
        idx = 0
        for _ in range(len(images_on_page) - 1):
            cols = st.columns(5)
            if idx < len(images_on_page):
                img = Image.open(fs.open(images_on_page[idx]))

                if img.size[1] > 500 and img.size[1] < 1500:
                    cols[0].image(img.resize((int(img.size[1] * img.size[0] / 500), 500)), use_column_width=True)
                    idx += 1
                elif img.size[1] > 1500:
                    idx += 1
                else:
                    cols[0].image(img, use_column_width=True)
                    idx += 1
            if idx < len(images_on_page):
                img = Image.open(fs.open(images_on_page[idx]))
                if img.size[1] > 500 and img.size[1] < 1500:
                    cols[1].image(img.resize((int(img.size[1] * img.size[0] / 500), 500)), use_column_width=True)
                    idx += 1
                elif img.size[1] > 1500:
                    idx += 1
                else:
                    cols[1].image(img, use_column_width=True)
                    idx += 1
            if idx < len(images_on_page):
                img = Image.open(fs.open(images_on_page[idx]))
                if img.size[1] > 500 and img.size[1] < 1500:
                    cols[2].image(img.resize((int(img.size[1] * img.size[0] / 500), 500)), use_column_width=True)
                    idx += 1
                elif img.size[1] > 1500:
                    idx += 1
                else:
                    cols[2].image(img, use_column_width=True)
                    idx += 1
            if idx < len(images_on_page):
                img = Image.open(fs.open(images_on_page[idx]))
                if img.size[1] > 500 and img.size[1] < 1500:
                    cols[3].image(img.resize((int(img.size[1] * img.size[0] / 500), 500)), use_column_width=True)
                    idx += 1
                elif img.size[1] > 1500:
                    idx += 1
                else:
                    cols[3].image(img, use_column_width=True)
                    idx += 1
            if idx < len(images_on_page):
                img = Image.open(fs.open(images_on_page[idx]))
                if img.size[1] > 500 and img.size[1] < 1500:
                    cols[4].image(img.resize((int(img.size[1] * img.size[0] / 500), 500)), use_column_width=True)
                    idx += 1
                elif img.size[1] > 1500:
                    idx += 1
                else:
                    cols[4].image(img, use_column_width=True)
                    idx += 1
            else:
                break


conn=pymysql.connect(host='bannersdet.cbai1qawgjuw.us-east-2.rds.amazonaws.com',port=int(33066),user='admin',passwd='s0nF8#v!1',db='bannersDetections')


cursor=conn.cursor()


sql="SELECT * FROM Detections1"
cursor.execute(sql)
df = cursor.fetchall()
df=pd.DataFrame(df,columns=['advertiser', 'type', 'page', 'site', 'day','hour','adlink'])

sql="SELECT * FROM undetectedads"
cursor.execute(sql)
df2 = cursor.fetchall()
df2=pd.DataFrame(df2,columns=['adlink', 'day'])







occurence_page()



