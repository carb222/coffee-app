#Libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#Page Configuration
st.set_page_config(
    page_title="Coffee Shop Sales",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#Load Data
df_reshaped = pd.read_csv('Coffee_Sales_Kaggle/index_1.csv')
df_reshaped['datetime'] = pd.to_datetime(df_reshaped['datetime'])
df_reshaped['year_month'] = df_reshaped['datetime'].dt.to_period('M').astype(str)
df_reshaped['hour'] = df_reshaped['datetime'].dt.hour

#Adding a sidebar
with st.sidebar:
    st.title('Coffee Shop Sales')
    
    year_list = list(df_reshaped.year_month.unique())[::-1]

    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year_month = df_reshaped[df_reshaped.year_month == selected_year]
    df_selected_year_month_sorted = df_selected_year_month.sort_values(by="money", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#Heatmap

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap


col = st.columns((1.5, 4.5, 2), gap='medium')



with col[1]:
    st.markdown('#### Total Sales')
    
    heatmap = make_heatmap(df_reshaped, 'hour', 'coffee_name', 'money', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)
