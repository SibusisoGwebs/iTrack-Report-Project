import streamlit as st
from streamlit_option_menu import option_menu as op
import streamlit_javascript as st_js
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

###############################################################################################################
data = pd.read_excel('Data/JHI_Report_2023_01.xlsx', sheet_name='Data')
px.set_mapbox_access_token(
        'pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
################################################################################################################
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

ui_width = st_js.st_javascript("window.innerWidth")

period = [
    '2023-01-31',
    '2023-02-28',
    '2022-12-31',
    '2022-11-30',
    '2022-10-31',
    '2022-06-30',
    '2022-05-31',
]

site_names = ['Cavendish', 'Zone', 'Vincent Park', 'Riverside',
              'Gateway', 'Phumlani', 'Kagiso', 'Phumlani Park', 'Roseville', 'Jet Park']

##################################################################################################################

# def filterData(filterValue):
#     filteredData = data[(data['Site'] == filterValue) &
#                         (data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]
#     return filteredData[['Camera Name', 'Reads', 'Alerts']]

# @st.cache_data
# def summaryFilteredByPeriod(value):
#     filteredData = data[(data['Site'] == selected) & (
#             data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]
#     summary = filteredData.groupby('Camera Name').sum()
#     return summary
##################################################################################################################

st.title('Detailed Dashboard')
st.markdown('''
    <h5 style='color: #FFA50f'>This section is a displays more information about the data. To slice data by months of each year and site to see camera data, 
    click the arrow (>) at the top-right conner to open the side bar. (Note: Side bar must always remain closed for data display)</h5>
    ''', unsafe_allow_html=True)
st.write('---')
selected = st.sidebar.selectbox('Select The Site', site_names)
period_selected = st.sidebar.selectbox('Select Month', period)
##################################################################################################################

def filterData(filterValue):
    filteredData = data[(data['Site'] == filterValue) &
                        (data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]
    return filteredData[['Camera Name', 'Reads', 'Alerts']]

def summaryFilteredByPeriod():
    filteredData = data[(data['Site'] == selected) & (
            data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]
    summary = filteredData.groupby('Camera Name').sum()
    return summary

filteredData = data[(data['Site'] == selected) & (
    data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]
##################################################################################################################

if selected == 'Cavendish':
    st.header(f'{selected} Cameras')
if selected == 'Zone':
    st.header(f'{selected} Cameras')
if selected == 'Vincent Park':
    st.header(f'{selected} Cameras')
if selected == 'Riverside':
    st.header(f'{selected} Cameras')
if selected == 'Gateway':
    st.header(f'{selected} Cameras')
if selected == 'Phumlani':
    st.header(f'{selected} Cameras')
if selected == 'Kagiso':
    st.header(f'{selected} Cameras')
if selected == 'Phumlani Park':
    st.header(f'{selected} Cameras')
if selected == 'Roseville':
    st.header(f'{selected} Cameras')
if selected == 'Jet Park':
    st.header(f'{selected} Cameras')
#######################################################################################################################
ReadsFilteredByCam = summaryFilteredByPeriod()['Reads']
AlertsFilteredByCam = summaryFilteredByPeriod()['Alerts']
mostReadsFilteredByCam = ReadsFilteredByCam[ReadsFilteredByCam == ReadsFilteredByCam.max()]
leastReadsFilteredByCam = ReadsFilteredByCam[ReadsFilteredByCam == ReadsFilteredByCam.min()]
mostAlertsFilteredByCam = AlertsFilteredByCam[AlertsFilteredByCam == AlertsFilteredByCam.max()]
leastAlertsFilteredByCam = AlertsFilteredByCam[AlertsFilteredByCam == AlertsFilteredByCam.min()]
#######################################################################################################################
st.write('---')
st.markdown(f'<h4 style="color: #C1B7B0">Camera with:</h4>', unsafe_allow_html=True)
coll1, coll2 = st.columns(2)
with coll1:
    st.markdown(f'<h4 style="color: green">Most Reads</h4>', unsafe_allow_html=True)
    st.table(mostReadsFilteredByCam)
with coll2:
    st.markdown(f'<h4 style="color: green">Least Reads</h4>', unsafe_allow_html=True)
    st.table(leastReadsFilteredByCam)

coll3, coll4 = st.columns(2)
with coll3:
    st.markdown(f'<h4 style="color: #FF0000">Most Alerts</h4>', unsafe_allow_html=True)
    st.table(mostAlertsFilteredByCam)
with coll4:
    st.markdown(f'<h4 style="color: #FF0000">Least Alerts</h4>', unsafe_allow_html=True)
    st.table(leastAlertsFilteredByCam)
st.write('---')
###############################################################################


def sumOfSite(filterValue):
    return summary


def pieChartFiltered(values, names, widths):
    pieChart = px.pie(filterData(selected), values=values, names=names,
                      title='', hole=.5, template='ggplot2')
    pieChart.update_layout(autosize=True, height=500, width=widths,
                           margin=dict(t=80, b=80, l=80, r=80),
                           plot_bgcolor='#dedede',
                           #    title_font=dict(
                           #        size=25, color='#a5a7ab', family="Muli, sans-serif"),
                           font=dict(size=18, color='#ffffff'),
                           legend=dict(orientation="h",
                                       y=1, x=1),
                           legend_font=dict(
                               color='#dedede',
                               size=12
                           )
                           )
    return pieChart

def detailedAlerts(width):
    fig = px.bar(filterData(selected), y='Alerts',
                     x='Camera Name', orientation='v',
                     template='seaborn',
                     width=width, color='Alerts', text_auto=True)
    return fig

def detailedReads(width):
    fig = px.bar(filterData(selected), y='Reads',
                     x='Camera Name', orientation='v',
                     template='presentation',
                     width=width, color='Reads', text_auto=True)
    return fig

def MapPlot(width):
    mapFig = px.scatter_mapbox(
            filteredData,
            lon=filteredData['longitude'],
            lat=filteredData['latitude'],
            zoom=17,
            color=filteredData['Alerts'],
            size=filteredData['Reads'],
            width=width,
            height=700,
            color_continuous_scale=px.colors.cyclical.IceFire
        )
    return mapFig
###############################################################################

# with st.container():
#     first_col, second_col = st.columns(2)
#     with first_col:
#         st.subheader(f'Reads By Cameras')
#         fig = px.bar(filterData(selected), x='Reads',
#                      y='Camera Name', orientation='h', height=600, width=600)
#         st.write(fig)
#     with second_col:
#         # st.subheader(f'Table: Cameras with Reads')
#         count = filterData(selected)[['Camera Name', 'Reads']].shape
#         st.title(f'{count[0]} Camera(s)')
#         st.subheader(f'Table: Cameras with Reads')
#         st.table(filterData(selected)[['Camera Name', 'Reads']])


with st.container():
    if ui_width <= 768:
        barFig = detailedAlerts(580)
        st.subheader(f'Alerts By Cameras')
        st.write(barFig)
    elif ui_width > 768 and ui_width <= 1255:
        fig = detailedAlerts(1080)
        st.subheader(f'Alerts By Cameras')
        st.write(fig)
    elif ui_width > 1260:
        fig = detailedAlerts(1590)
        st.subheader(f'Alerts By Cameras')
        st.write(fig)
    else:
        fig = detailedAlerts(1900)
        st.subheader(f'Alerts By Cameras')
        st.write(fig)
    # st.bar_chart(filterData(selected), x='Camera Name', y='Alerts')
if ui_width <= 768:
    with st.container():
        st.subheader(f'Table: Cameras with Alerts')
        st.table(filterData(selected)[['Camera Name', 'Alerts']])
    with st.container():
        st.subheader(f'Summary Statistics')
        st.table(filterData(selected).describe())
else:
    with st.container():
        cols1, cols2 = st.columns(2)
        with cols1:
            st.subheader(f'Table: Cameras with Alerts')
            st.table(filterData(selected)[['Camera Name', 'Alerts']])
        with cols2:
            st.subheader(f'Summary Statistics')
            st.table(filterData(selected).describe())


with st.container():
    if ui_width <= 768:
        st.subheader(f'Reads By Cameras')
        barFigReads = detailedReads(580)
        # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
        #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        #                   font=dict(color='#8a8d93'))
        st.write(barFigReads)
    elif ui_width > 768 and ui_width <= 1255:
        st.subheader(f'Reads By Cameras')
        barFigReads = detailedReads(1080)
        # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
        #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        #                   font=dict(color='#8a8d93'))
        st.write(barFigReads)
    elif ui_width > 1260:
        st.subheader(f'Reads By Cameras')
        barFigReads = detailedReads(1590)
        # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
        #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        #                   font=dict(color='#8a8d93'))
        st.write(barFigReads)
    else:
        st.subheader(f'Reads By Cameras')
        barFigReads = detailedReads(1900)
        # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
        #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
        #                   font=dict(color='#8a8d93'))
        st.write(barFigReads)

    # st.subheader(f'Reads By Cameras')
    # fig = px.bar(filterData(selected), y='Reads',
    #              x='Camera Name', orientation='v',
    #              template='plotly_white',
    #              width=1100)
    # # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
    # #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
    # #                   font=dict(color='#8a8d93'))
    # st.write(fig)

with st.container():
    ReadsOrAlerts = ['Reads', 'Alerts']
    results = st.selectbox('Reads OR Alers', ReadsOrAlerts)
    if ui_width <= 768:
        st.subheader(f'{results} Percentage')
        st.write(pieChartFiltered(results, 'Camera Name', 580))
    elif ui_width > 768 and ui_width <= 1255:
        st.subheader(f'{results} Percentage')
        st.write(pieChartFiltered(results, 'Camera Name', 1080))
    elif ui_width > 1260:
        st.subheader(f'{results} Percentage')
        st.write(pieChartFiltered(results, 'Camera Name', 1590))
    else:
        st.subheader(f'{results} Percentage')
        st.write(pieChartFiltered(results, 'Camera Name', 1900))

    # st.subheader(f'{results} Percentage')
    # st.write(pieChartFiltered(results, 'Camera Name'))
    # with col1:
    #     st.subheader(f'Reads Percentage')
    #     st.write(pieChartFiltered('Reads', 'Camera Name'))
    # with col2:
    #     st.subheader(f'Alerts Percentage')
    #     st.write(pieChartFiltered('Alerts', 'Camera Name'))


def MapData(filterValue):
    filteredData = data[data['Site'] == filterValue]
    return filteredData[['Camera Name', 'Reads', 'Alerts', 'Latitude', 'Longitude']]


with st.container():

    if ui_width <= 768:
        st.title('Camera Site Locations')
        st.text('The map which displays the camera locations on site.')
        st.text(
            'The size of the point represents the number of Reads that camera have taken')
        mapFig = MapPlot(580)
        mapFig.update_layout(mapbox_style="dark",
                          mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
        st.write(mapFig)
    elif ui_width > 768 and ui_width <= 1255:
        st.title('Camera Site Locations')
        st.text('The map which displays the camera locations on site.')
        st.text(
            'The size of the point represents the number of Reads that camera have taken')
        mapFig = MapPlot(1080)
        mapFig.update_layout(mapbox_style="dark",
                          mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
        st.write(mapFig)
    elif ui_width > 1260:
        st.title('Camera Site Locations')
        st.text('The map which displays the camera locations on site.')
        st.text(
            'The size of the point represents the number of Reads that camera have taken')
        mapFig = MapPlot(1590)
        mapFig.update_layout(mapbox_style="dark",
                          mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
        st.write(mapFig)
    else:
        st.title('Camera Site Locations')
        st.text('The map which displays the camera locations on site.')
        st.text(
            'The size of the point represents the number of Reads that camera have taken')
        mapFig = MapPlot(1900)
        mapFig.update_layout(mapbox_style="dark",
                          mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
        st.write(mapFig)

