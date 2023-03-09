import streamlit as st
from streamlit_option_menu import option_menu as op
import streamlit_javascript as st_js
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image

st.set_page_config(page_title='iTrack JHI Report',
                   page_icon=':camera', layout='wide')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

ui_width = st_js.st_javascript("window.innerWidth")

site_names = ['Cavendish', 'Zone', 'Vincent Park', 'Riverside',
              'Gateway', 'Phumlani', 'Kagiso', 'Phumlani Park', 'Roseville', 'Jet Park']
period = [
    '2023-01-31',
    '2023-02-28',
    '2022-12-31',
    '2022-11-30',
    '2022-10-31',
    '2022-06-30',
    '2022-05-31',
]


header = st.container()
dataset = st.container()

data = pd.read_excel('Data/JHI_Report_2023_01.xlsx', sheet_name='Data')
summaryByReads = data[['Reads', 'Site']].groupby('Site').sum()
summaryByAlerts = data[['Alerts', 'Site']].groupby('Site').sum()
summary = data.groupby('Site').sum()


###############################################################################

@st.cache_data
def filteredDataFrame(value):
    return data[data['Period'] == pd.to_datetime(
        value, format="%Y-%m-%d %H:%M:%S")]


def summaryByAlertsfiltered():
    return filteredDataFrame(period_selected1)[['Alerts', 'Site']].groupby('Site').sum()

@st.cache_data
def summaryByReadsfiltered():
    return filteredDataFrame(period_selected1)[['Reads', 'Site']].groupby('Site').sum()

@st.cache_data
def summaryFilteredByPeriod(value):
    filteredData = data[data['Period'] == pd.to_datetime(
        period_selected1, format="%Y-%m-%d %H:%M:%S")]
    summary = filteredData.groupby('Site').sum()
    return summary

@st.cache_data
def filterData(filterValue):
    filteredData = data[(data['Site'] == filterValue) &
                        (data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]
    return filteredData[['Camera Name', 'Reads', 'Alerts']]

@st.cache_data
def pieChartData(values, name, widths):
    pieChart = px.pie(data, values=values, names=name, hole=.5, template='ggplot2')
    pieChart.update_layout(autosize=True, height=500, width=widths,
                           margin=dict(t=80, b=80, l=80, r=80),
                           plot_bgcolor='#dedede',
                           #    title_font=dict(
                           #        size=25, color='#a5a7ab', family="Muli, sans-serif"),
                           font=dict(size=18, color='#ffffff'),
                           legend=dict(orientation="h", yanchor="top",
                                       y=1, xanchor="left", x=1),
                           legend_font=dict(
                               color='#dedede',
                               size=12
                           )
                           )
    return pieChart

@st.cache_data
def barChartData(name, widths):
    barChart = px.bar(summaryByAlerts, y=name,
                      template='seaborn', width=widths, color='Alerts', text_auto=True)
    # barChart.update_layout(uniform_minsize=8)
    return barChart


def barChartfiltered(dataframe, name, widths):
    barChart = px.bar(dataframe, y=name,
                      width=widths,template='seaborn', color='Alerts', text_auto=True)
    # barChart.update_layout(uniform_minsize=8)
    return barChart
###############################################################################
st.sidebar.success('')
image = Image.open('Logo.png')
insight_button = st.sidebar.button('Insight')

with header:
    # st.image(image, use_column_width=10)
    st.title('Welcome To iTrack Report')
    st.markdown('<h5>The JHI Report on Various Site<h5>', unsafe_allow_html=True)
    st.write('---')
    # st.header('Summary Data:')

###############################################################################
mostReads = summaryByReads[summaryByReads['Reads'] == summaryByReads['Reads'].max()]
minReads = summaryByReads[summaryByReads['Reads'] == summaryByReads['Reads'].min()]
mostAlerts = summaryByAlerts[summaryByAlerts['Alerts'] == summaryByAlerts['Alerts'].max()]
minAlerts = summaryByAlerts[summaryByAlerts['Alerts'] == summaryByAlerts['Alerts'].min()]

insight = f"""
Site with most number of Reads is: {summaryByReads[summaryByReads['Reads'] == summaryByReads['Reads'].max()]}
"""
###############################################################################


with dataset:
    # with st.container():
    #     st.write(summaryByAlerts)
    st.title('Overview Dashboard')
    st.markdown('''
    <h5 style='color: #FFA50f'>This section displays all available data from all available months. To slice data by months of each year, 
    click the arrow (>) at the top-right conner to open the side bar. (Note: Side bar must always remain closed for data display)</h5>
    ''', unsafe_allow_html=True)
    st.write('---')

    typeOfSummary = ['Summary', 'Statistics']
    totalOrSubtotal = ['Total', 'Subtotal']
    selectedSummary = st.sidebar.selectbox('Select Summary Type', typeOfSummary)
    typeTotal = st.sidebar.selectbox('Select Period', totalOrSubtotal)

    if typeTotal == 'Subtotal':
        period_selected1 = st.selectbox('Select Period',period)
        ########################################################################################################
        ReadsFiltered = summaryFilteredByPeriod(period_selected1)['Reads']
        AlertsFiltered = summaryFilteredByPeriod(period_selected1)['Alerts']
        mostReadsFiltered = ReadsFiltered[ReadsFiltered == ReadsFiltered.max()]
        leastReadsFiltered = ReadsFiltered[ReadsFiltered == ReadsFiltered.min()]
        mostAlertsFiltered = AlertsFiltered[AlertsFiltered == AlertsFiltered.max()]
        leastAlertsFiltered = AlertsFiltered[AlertsFiltered == AlertsFiltered.min()]
        #########################################################################################################
    
        f1Col, f2Col = st.columns(2)
        with f1Col:
            st.markdown(f'<h3 style="color: green">Total Reads: {filteredDataFrame(period_selected1)["Reads"].sum()}</h3>', unsafe_allow_html=True)
            st.write('---')
        with f2Col:
            st.markdown(f'''<h3 style="color: #ff0000">Total Alerts: {filteredDataFrame(period_selected1)["Alerts"].sum()}</h3>''', unsafe_allow_html=True)
            st.write('---')
            # st.warning(f'Total Alerts: {filteredDataFrame(period_selected1)["Alerts"].sum()}')
    if typeTotal == 'Total':
        coll1, coll2, = st.columns(2)
        with coll1:
            st.markdown(f'<h3 style="color: green">Most Reads</h3>', unsafe_allow_html=True)
            st.write(mostReads)
        with coll2:
            st.markdown(f'<h3 style="color: green">Least Reads</h3>', unsafe_allow_html=True)
            st.write(minReads)
        coll3, coll4 = st.columns(2)
        with coll3:
            st.markdown(f'<h3 style="color: #FF0000">Most Alerts</h3>', unsafe_allow_html=True)
            st.write(mostAlerts)
        with coll4:
            st.markdown(f'<h3 style="color: #FF0000">Least Alerts</h3>', unsafe_allow_html=True)
            st.write(minAlerts)
    else:
        coll1, coll2, coll3, coll4 = st.columns(4)
        with coll1:
            st.markdown(f'<h3 style="color: green">Most Reads</h3>', unsafe_allow_html=True)
            st.write(mostReadsFiltered)
        with coll2:
            st.markdown(f'<h3 style="color: green">Least Reads</h3>', unsafe_allow_html=True)
            st.write(leastReadsFiltered)
        with coll3:
            st.markdown(f'<h3 style="color: #FF0000">Most Alerts</h3>', unsafe_allow_html=True)
            st.write(mostAlertsFiltered)
        with coll4:
            st.markdown(f'<h3 style="color: #FF0000">Least Alerts</h3>', unsafe_allow_html=True)
            st.write(leastAlertsFiltered)



    left_coloumn, right_column = st.columns((2, 1))

    with left_coloumn:
        if typeTotal == "Total":
            if ui_width <= 768:
                st.subheader('Site\'s Total Alerts')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartData('Alerts', 420))
            elif ui_width > 768 and ui_width <= 1255:
                st.subheader('Site\'s Total Alerts')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartData('Alerts', 680))
            elif ui_width > 1260:
                st.subheader('Site\'s Total Alerts')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartData('Alerts', 1000))
            else:
                st.subheader('Site\'s Total Alerts')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartData('Alerts', 1200))
        else:
            if ui_width <= 768:
                st.subheader(f'Site\'s Total Alerts of {period_selected1}')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartfiltered(
                    summaryByAlertsfiltered(), 'Alerts', 580))
            elif ui_width > 768 and ui_width <= 1255:
                st.subheader(f'Site\'s Total Alerts of {period_selected1}')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartfiltered(
                    summaryByAlertsfiltered(), 'Alerts', 680))
            elif ui_width > 1260:
                st.subheader(f'Site\'s Total Alerts of {period_selected1}')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartfiltered(
                    summaryByAlertsfiltered(), 'Alerts', 1000))
            else:
                st.subheader(f'Site\'s Total Alerts of {period_selected1}')
                # figSummaryAlerts = px.bar(barChartData('Alerts'))
                st.write(barChartfiltered(
                    summaryByAlertsfiltered(), 'Alerts', 1200))

    with right_column:
        if typeTotal == "Total":
            if selectedSummary == 'Summary':
                # st.subheader(f'10 JHI Sites')
                st.subheader('Summary of Sites')
                st.table(summary[['Reads', 'Alerts']])
            else:
                camera_count = data.shape[0]
                # st.subheader(f'Total of {camera_count} Camera(s)')
                st.subheader('Summary Statistics')
                st.table(data[['Reads', 'Alerts']].describe())
        else:
            if selectedSummary == 'Summary':
                st.subheader(f'Site Summary for {period_selected1}')
                st.table(summaryFilteredByPeriod(period_selected1)[['Reads', 'Alerts']])
            else:
                st.subheader(f'Site Statistics for {period_selected1}')
                st.table(summaryFilteredByPeriod(period_selected1)[['Reads', 'Alerts']].describe())

    left1_coloumn, right1_column = st.columns(2)
    with st.container():
        if ui_width <= 768:
            st.subheader('Site\'s Total Reads')
            figSummaryReads = px.bar(
                summaryByReads, y='Reads', width=580, template='presentation', color='Reads', text_auto=True)
            st.write(figSummaryReads)
        elif ui_width > 768 and ui_width <= 1255:
            st.subheader('Site\'s Total Reads')
            figSummaryReads = px.bar(
                summaryByReads, y='Reads', width=1080, template='presentation', color='Reads', text_auto=True)
            st.write(figSummaryReads)
        elif ui_width > 1260:
            st.subheader('Site\'s Total Reads')
            figSummaryReads = px.bar(
                summaryByReads, y='Reads', width=1590, template='presentation', color='Reads', text_auto=True)
            st.write(figSummaryReads)
        else:
            st.subheader('Site\'s Total Reads')
            figSummaryReads = px.bar(
                summaryByReads, y='Reads', width=1900, template='presentation', color='Reads', text_auto=True)
            st.write(figSummaryReads)

    with st.container():
        if ui_width <= 768:
            st.subheader('Site\'s Reads Percentage')
            readsPieChart = pieChartData('Reads', 'Site', 580)
            st.write(readsPieChart)
        elif ui_width > 768 and ui_width <= 1255:
            st.subheader('Site\'s Reads Percentage')
            readsPieChart = pieChartData('Reads', 'Site', 1080)
            st.write(readsPieChart)
        elif ui_width > 1260:
            st.subheader('Site\'s Reads Percentage')
            readsPieChart = pieChartData('Reads', 'Site', 1590)
            st.write(readsPieChart)
        else:
            st.subheader('Site\'s Reads Percentage')
            readsPieChart = pieChartData('Reads', 'Site', 1900)
            st.write(readsPieChart)
    st.write('---')
        # fig_pie = px.pie(data, values='Reads', names='Site', title='')
        # st.write(pieChart('Reads', 'Site'))
    # fig_map = px.scatter_geo(data, locations="USA", color="Site",
    #                          hover_name="Site", size="pop",
    #                          projection="natural earth")
    # st.write(fig_map)
###############################################################################

# st.title('Detailed Dashboard')
# period_selected = st.selectbox('Select Month', period)
# selected = st.selectbox('Select The Site', site_names)

# if selected == 'Cavendish':
#     st.header(f'{selected} Cameras')
# if selected == 'Zone':
#     st.header(f'{selected} Cameras')
# if selected == 'Vincent Park':
#     st.header(f'{selected} Cameras')
# if selected == 'Riverside':
#     st.header(f'{selected} Cameras')
# if selected == 'Gateway':
#     st.header(f'{selected} Cameras')
# if selected == 'Phumlani':
#     st.header(f'{selected} Cameras')
# if selected == 'Kagiso':
#     st.header(f'{selected} Cameras')
# if selected == 'Phumlani Park':
#     st.header(f'{selected} Cameras')
# if selected == 'Roseville':
#     st.header(f'{selected} Cameras')
# if selected == 'Jet Park':
#     st.header(f'{selected} Cameras')

# ###############################################################################

# @st.cache_data
# def sumOfSite(filterValue):
#     return summary

# @st.cache_data
# def pieChartFiltered(values, names, widths):
#     pieChart = px.pie(filterData(selected), values=values, names=names,
#                       title='', hole=.5)
#     pieChart.update_layout(autosize=True, height=500, width=widths,
#                            margin=dict(t=80, b=80, l=80, r=80),
#                            plot_bgcolor='#dedede', paper_bgcolor='#00172B',
#                            #    title_font=dict(
#                            #        size=25, color='#a5a7ab', family="Muli, sans-serif"),
#                            font=dict(size=18, color='#ffffff'),
#                            legend=dict(orientation="h",
#                                        y=1, x=1),
#                            legend_font=dict(
#                                color='#dedede',
#                                size=12
#                            )
#                            )
#     return pieChart
# ###############################################################################

# # with st.container():
# #     first_col, second_col = st.columns(2)
# #     with first_col:
# #         st.subheader(f'Reads By Cameras')
# #         fig = px.bar(filterData(selected), x='Reads',
# #                      y='Camera Name', orientation='h', height=600, width=600)
# #         st.write(fig)
# #     with second_col:
# #         # st.subheader(f'Table: Cameras with Reads')
# #         count = filterData(selected)[['Camera Name', 'Reads']].shape
# #         st.title(f'{count[0]} Camera(s)')
# #         st.subheader(f'Table: Cameras with Reads')
# #         st.table(filterData(selected)[['Camera Name', 'Reads']])


# with st.container():
#     if ui_width <= 768:
#         fig = px.bar(filterData(selected), y='Alerts',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=580)
#         st.subheader(f'Alerts By Cameras')
#         st.write(fig)
#     elif ui_width > 768 and ui_width <= 1255:
#         fig = px.bar(filterData(selected), y='Alerts',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=1080)
#         st.subheader(f'Alerts By Cameras')
#         st.write(fig)
#     elif ui_width > 1260:
#         fig = px.bar(filterData(selected), y='Alerts',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=1590)
#         st.subheader(f'Alerts By Cameras')
#         st.write(fig)
#     else:
#         fig = px.bar(filterData(selected), y='Alerts',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=1900)
#         st.subheader(f'Alerts By Cameras')
#         st.write(fig)
#     # st.bar_chart(filterData(selected), x='Camera Name', y='Alerts')

# with st.container():
#     cols1, cols2 = st.columns(2)
#     with cols1:
#         st.subheader(f'Table: Cameras with Alerts')
#         st.write(filterData(selected)[['Camera Name', 'Alerts']])
#     with cols2:
#         st.subheader(f'Summary Statistics')
#         st.table(filterData(selected).describe())


# with st.container():
#     if ui_width <= 768:
#         st.subheader(f'Reads By Cameras')
#         fig = px.bar(filterData(selected), y='Reads',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=580)
#         # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
#         #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
#         #                   font=dict(color='#8a8d93'))
#         st.write(fig)
#     elif ui_width > 768 and ui_width <= 1255:
#         st.subheader(f'Reads By Cameras')
#         fig = px.bar(filterData(selected), y='Reads',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=1080)
#         # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
#         #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
#         #                   font=dict(color='#8a8d93'))
#         st.write(fig)
#     elif ui_width > 1260:
#         st.subheader(f'Reads By Cameras')
#         fig = px.bar(filterData(selected), y='Reads',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=1590)
#         # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
#         #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
#         #                   font=dict(color='#8a8d93'))
#         st.write(fig)
#     else:
#         st.subheader(f'Reads By Cameras')
#         fig = px.bar(filterData(selected), y='Reads',
#                      x='Camera Name', orientation='v',
#                      template='plotly_white',
#                      width=1900)
#         # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
#         #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
#         #                   font=dict(color='#8a8d93'))
#         st.write(fig)

#     # st.subheader(f'Reads By Cameras')
#     # fig = px.bar(filterData(selected), y='Reads',
#     #              x='Camera Name', orientation='v',
#     #              template='plotly_white',
#     #              width=1100)
#     # # fig.update_layout(autosize=True, margin=dict(t=80, b=30, l=70, r=40),
#     # #                   plot_bgcolor='#2d3035', paper_bgcolor='#2d3035', title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
#     # #                   font=dict(color='#8a8d93'))
#     # st.write(fig)

# with st.container():
#     ReadsOrAlerts = ['Reads', 'Alerts']
#     results = st.selectbox('Reads OR Alers', ReadsOrAlerts)
#     if ui_width <= 768:
#         st.subheader(f'{results} Percentage')
#         st.write(pieChartFiltered(results, 'Camera Name', 580))
#     elif ui_width > 768 and ui_width <= 1255:
#         st.subheader(f'{results} Percentage')
#         st.write(pieChartFiltered(results, 'Camera Name', 1080))
#     elif ui_width > 1260:
#         st.subheader(f'{results} Percentage')
#         st.write(pieChartFiltered(results, 'Camera Name', 1590))
#     else:
#         st.subheader(f'{results} Percentage')
#         st.write(pieChartFiltered(results, 'Camera Name', 1900))

#     # st.subheader(f'{results} Percentage')
#     # st.write(pieChartFiltered(results, 'Camera Name'))
#     # with col1:
#     #     st.subheader(f'Reads Percentage')
#     #     st.write(pieChartFiltered('Reads', 'Camera Name'))
#     # with col2:
#     #     st.subheader(f'Alerts Percentage')
#     #     st.write(pieChartFiltered('Alerts', 'Camera Name'))

# @st.cache_data
# def MapData(filterValue):
#     filteredData = data[data['Site'] == filterValue]
#     return filteredData[['Camera Name', 'Reads', 'Alerts', 'Latitude', 'Longitude']]


# with st.container():
#     px.set_mapbox_access_token(
#         'pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
#     filteredData = data[(data['Site'] == selected) & (
#         data['Period'] == pd.to_datetime(period_selected, format="%Y-%m-%d %H:%M:%S"))]

#     if ui_width <= 768:
#         st.title('Camera Site Locations')
#         st.text('The map which displays the camera locations on site.')
#         st.text(
#             'The size of the point represents the number of Reads that camera have taken')
#         mapFig = px.scatter_mapbox(
#             filteredData,
#             lon=filteredData['longitude'],
#             lat=filteredData['latitude'],
#             zoom=17,
#             color=filteredData['Alerts'],
#             size=filteredData['Reads'],
#             width=580,
#             height=700,
#             color_continuous_scale=px.colors.cyclical.IceFire
#         )
#         fig.update_layout(mapbox_style="dark",
#                           mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
#         st.write(mapFig)
#     elif ui_width > 768 and ui_width <= 1255:
#         st.title('Camera Site Locations')
#         st.text('The map which displays the camera locations on site.')
#         st.text(
#             'The size of the point represents the number of Reads that camera have taken')
#         mapFig = px.scatter_mapbox(
#             filteredData,
#             lon=filteredData['longitude'],
#             lat=filteredData['latitude'],
#             zoom=17,
#             color=filteredData['Alerts'],
#             size=filteredData['Reads'],
#             width=1080,
#             height=700,
#             color_continuous_scale=px.colors.cyclical.IceFire
#         )
#         fig.update_layout(mapbox_style="dark",
#                           mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
#         st.write(mapFig)
#     elif ui_width > 1260:
#         st.title('Camera Site Locations')
#         st.text('The map which displays the camera locations on site.')
#         st.text(
#             'The size of the point represents the number of Reads that camera have taken')
#         mapFig = px.scatter_mapbox(
#             filteredData,
#             lon=filteredData['longitude'],
#             lat=filteredData['latitude'],
#             zoom=17,
#             color=filteredData['Alerts'],
#             size=filteredData['Reads'],
#             width=1590,
#             height=700,
#             color_continuous_scale=px.colors.cyclical.IceFire
#         )
#         fig.update_layout(mapbox_style="dark",
#                           mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
#         st.write(mapFig)
#     else:
#         st.title('Camera Site Locations')
#         st.text('The map which displays the camera locations on site.')
#         st.text(
#             'The size of the point represents the number of Reads that camera have taken')
#         mapFig = px.scatter_mapbox(
#             filteredData,
#             lon=filteredData['longitude'],
#             lat=filteredData['latitude'],
#             zoom=17,
#             color=filteredData['Alerts'],
#             size=filteredData['Reads'],
#             width=1900,
#             height=700,
#             color_continuous_scale=px.colors.cyclical.IceFire
#         )
#         fig.update_layout(mapbox_style="dark",
#                           mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
#         st.write(mapFig)

#     st.map(data=filteredData[['latitude', 'longitude']],
#            zoom=3, use_container_width=True)
#     st.title('Camera Site Locations')
#     st.text('The map which displays the camera locations on site.')
#     st.text(
#         'The size of the point represents the number of Reads that camera have taken')
#     mapFig = px.scatter_mapbox(
#         filteredData,
#         lon=filteredData['longitude'],
#         lat=filteredData['latitude'],
#         zoom=17,
#         color=filteredData['Alerts'],
#         size=filteredData['Reads'],
#         width=1100,
#         height=700,
#         color_continuous_scale=px.colors.cyclical.IceFire
#     )
#     fig.update_layout(mapbox_style="dark",
#                       mapbox_accesstoken='pk.eyJ1Ijoia2luZy1nd2Viczk4IiwiYSI6ImNsZWN3cHRiajAxOGozbnF6bGszcGNiZnIifQ.qUPfTxO16M0WDjjEoPaXzw')
#     st.write(mapFig)
