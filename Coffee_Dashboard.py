#Libraries
import streamlit as st
import pandas as pd
import altair as alt

#Page Configuration
st.set_page_config(
    page_title="Coffee Shop Sales",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#Load Data
df_reshaped = pd.read_csv('index_1.csv')
df_reshaped['datetime'] = pd.to_datetime(df_reshaped['datetime'])
df_reshaped['year_month'] = df_reshaped['datetime'].dt.to_period('M').astype(str)
df_reshaped['hour'] = df_reshaped['datetime'].dt.hour


#Adding a sidebar
with st.sidebar:
    st.title('Coffee Shop Sales')
    
    year_month_list = list(df_reshaped.year_month.unique())[::-1]
    year_month_list.insert(0, "All")  # Add "All" at the beginning


    selected_year = st.selectbox('Select a Date', year_month_list, index=1)

    if selected_year == "All":
        df_selected_year_month = df_reshaped.copy()  # Use full dataset
    else:
        df_selected_year_month = df_reshaped[df_reshaped.year_month == selected_year]

    df_selected_year_month_sorted = df_selected_year_month.sort_values(by="money", ascending=False)


    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#Heatmap

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = (
        alt.Chart(input_df)
        .mark_rect()
        .encode(y=alt.Y(f"{input_y}:O",axis=alt.Axis(title="Sales",titleFontSize=18,titlePadding=15,titleFontWeight=900,labelAngle=0),),
            x=alt.X(f"{input_x}:O",axis=alt.Axis(title="",titleFontSize=18,titlePadding=15,titleFontWeight=900),),
            color=alt.Color(f"sum({input_color}):Q",  legend=None,scale=alt.Scale(scheme=input_color_theme),),stroke=alt.value("black"),
            strokeWidth=alt.value(0.25),).properties(width=900).configure_axis(labelFontSize=12,titleFontSize=12,))
    return heatmap


def make_line_chart(df, x, y, color=None, color_scheme=None, title="Line Chart"):
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(x, title=x),
        y=alt.Y(y, title=y),
        tooltip=[x, y] + ([color] if color else [])
    )

    if color:
        chart = chart.encode(color=alt.Color(color, scale=alt.Scale(scheme=color_scheme)))

    chart = chart.properties(
        title=title,
        width=900,
        height=400
    ).interactive()

    return chart

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[1]:

    st.markdown('#### Total Sales')

    heatmap = make_heatmap(df_selected_year_month_sorted, 'hour', 'coffee_name', 'money', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)

    # Sum money by year_month
    df_grouped = df_reshaped.groupby('year_month', as_index=False)['money'].sum()
    line_chart = make_line_chart(df_grouped, 'year_month', 'money', title="Total Sales Over Time")
    st.altair_chart(line_chart, use_container_width=True)


df_top_drinks = (
    df_selected_year_month.groupby("coffee_name", as_index=False)["money"]
    .sum()
    .sort_values(by="money", ascending=False)
)

with col[2]:
    st.markdown('#### Top Drinks')

    st.dataframe(
        df_top_drinks,
        hide_index=True,
        column_config={
            "coffee_name": st.column_config.TextColumn("Drink"),
            "money": st.column_config.ProgressColumn(
                "Total Sales",
                format="£%d",
                min_value=0,
                max_value=df_top_drinks["money"].max(),  # largest sum determines full bar
            ),
        }
    )
