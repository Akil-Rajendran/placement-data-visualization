import streamlit as st
import pandas as pd
from plotly import express as px
import numpy as np
from plotly import graph_objects as go
from matplotlib import pyplot as plt
from numerize import numerize
import base64
from IPython.display import HTML
from decimal import Decimal

header = st.container()
overview = st.container()
visuals = st.container()

with header:
    st.markdown('<p style="font-family: Showcard Gothic, monospace; color:#9a44db; font-size: 72px;text-align: center"><b>PLACEMENT DATA VISUALIZATION OF BATCH 2018-2022</b></p>', unsafe_allow_html=True)

with overview:
    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>a deep down analysis of the placements</b></p>', unsafe_allow_html=True)
    st.markdown("""<hr style="height:5px;border:none;color:#000000;background-color:black;" /> """, unsafe_allow_html=True)
    data = pd.read_csv(r'data.csv', index_col=[0])
    placement = pd.read_csv(r'placement.csv', index_col=[0])
    higher = pd.read_csv(r'higher.csv', index_col=[0])
    company_group = placement.groupby(['Company Name'])
    CGPA_group = placement.groupby(['CGPA_round'])

    st.subheader("Students who got placed")
    st.table(pd.DataFrame(placement).iloc[:,:5])
    st.subheader("Students who did not opt for placements")
    st.table(pd.DataFrame(higher)[['Name', 'Package (Intern)']])
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

with visuals:
    st.metric("Maximum Package", numerize.numerize(int(placement['Package (FTE)'].max()), 2))
    st.metric("Average Package", numerize.numerize(int(placement['Package (FTE)'].mean()), 2))
    st.metric("Minimum Package", numerize.numerize(int(placement['Package (FTE)'].min()), 2))
    
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.metric("Maximum CGPA", placement['CGPA'].max())
    st.metric("Average CGPA", round(placement['CGPA'].mean(), 2))
    st.metric("Minimum CGPA", placement['CGPA'].min())

    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>relationship between CGPA and Package(FTE)</b></p>', unsafe_allow_html=True)
    st.area_chart(placement, x='CGPA', y='Package (FTE)')
    
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>hover on the bubble for details</b></p>', unsafe_allow_html=True)
    fig = px.scatter(placement, x="CGPA", y="Package (FTE)", color="CGPA", size='CGPA', hover_data=['Name'])
    st.plotly_chart(fig)
    
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>hover on the box for details</b></p>', unsafe_allow_html=True)
    fig = px.box(placement, x="CGPA_round", y="Package (FTE)", hover_data=['Name'])
    st.plotly_chart(fig)

    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>students with max package</b></p>', unsafe_allow_html=True)
    df = pd.DataFrame(placement[placement['Package (FTE)'] == placement['Package (FTE)'].max()])
    st.write(df.iloc[:, :6])

    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>student with max CGPA</b></p>', unsafe_allow_html=True)
    df = pd.DataFrame(placement[placement['CGPA'] == placement['CGPA'].max()])
    st.write(df.iloc[:, :6])

    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>student details based on CGPA</b></p>', unsafe_allow_html=True)
    select = st.selectbox('',[7,8,9,10])
    st.table(pd.DataFrame(CGPA_group.get_group(select)).iloc[:, :4])
    
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>companies that hired most number of students</b></p>', unsafe_allow_html=True)
    st.write(company_group['Name'].count().sort_values(ascending=False).head(5))
    
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Verdana; color: #c096e0; font-size: 25px;text-align: center"><b>Student details based on companies</b></p>', unsafe_allow_html=True)
    select = st.selectbox('', placement['Company Name'].unique().tolist())
    st.table(pd.DataFrame(company_group.get_group(select))[['Name', 'CGPA', 'Package (FTE)']])
    
    def create_download_link( df, title = "download the data used", filename = "data.csv"):  
        csv = df.to_csv()
        b64 = base64.b64encode(csv.encode())
        payload = b64.decode()
        html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
        html = html.format(payload=payload,title=title,filename=filename)
        return HTML(html)
        
    st.markdown('<hr style="height:5px;border:none;color:#000000;background-color:black;"/> ', unsafe_allow_html=True)
    st.write(create_download_link(data))
