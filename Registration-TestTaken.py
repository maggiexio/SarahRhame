import streamlit as st
import pandas as pd
import plotly 
import plotly.express as px
import csv
import base64
import difflib
 
#@st.cache
def raw_data(input_file):
   df=pd.read_csv(input_file, encoding = "ISO-8859-1")
#  df=pd.read_csv(input_file)
   return df

#######################glabal variables
#define functions

##############################
st.set_page_config(layout="wide", initial_sidebar_state="auto")
col11, col12 = st.columns((3,1))
with col11:
  title_1="TOEFL iBT registration vs test-taken monthly volume "
  st.markdown(f'<h1 style="text-align: center;color: green;">{title_1}</h1>',unsafe_allow_html=True)
  subj_1="-- Fical year 2020 to 2023"
  st.markdown(f'<h2 style="text-align: center;color: green;">{subj_1}</h2>',unsafe_allow_html=True) 
  st.markdown ("By: Sarah Rhame")
  st.markdown("Data file include 6694 registraion and 7105 test-taken records for each region/country/year/month from fical year 2020 to 2022  ")
   
with col12:
  title_11="Hello! I am Alexa. Can I help you?"
  st.markdown(f'<h2 style="text-align: center;color: purple;">{title_11}</h2>',unsafe_allow_html=True)
  user_input =''
  user_input = st.text_area("Type your questions here (enter 'contrl+enter' to finish your questions)", value="", max_chars=5000)
  if user_input.lower().find('no question') != -1:
    st.write ("Great! Have a nice day!")
  else:
    if user_input.lower().find('item level plots') != -1:
      st.write ("Item level plot will be added into a different page! At this point, only test level plots are provided.")
    else: 
      if user_input.lower()!='': 
        st.write ("Sorry, I am not sure! Please contact xxiong@ets.org")
         
# read in data
df_ori=raw_data("./data/DataReorg_output.xlsx")
df_ori['rt_gs_1']=""
df_ori['state_corr']=""
df_ori['state_abbr']=""
df_ori['country_abbr']=""
df_ori['age_group']=""
bins= [0,20,35,55,80]
labels = ['Teen(<20)','Young Adult(20,35)','Mid-aged Adult(35-55)','Older Adult(>55)']
df_ori['age_group'] = pd.cut(df_ori['age'], bins=bins, labels=labels, right=False)
df_ori['age_group'] = df_ori['age_group'].cat.add_categories('unknown').fillna('unknown')  

state_list_up=[t.upper() for t in state_list]
country_list_up=[t.upper() for t in country_list]
name_list_up = list(set(state_list_up) | set(country_list_up))

for i,state_t in enumerate(df_ori.state):
    state_t=state_t.upper()
    result=[s for f in state_t.split() for s in name_list_up if is_similar(f,s, 0.8)]
    if len(result)==0:
      result=[s for f in state_t.split(',') for s in name_list_up if is_similar(f,s, 0.8)]
    df_ori['state_corr'][i]=",".join(result)

with col11:  
  with st.expander("Registraion volume view"): 
      st.write("""
        Please select which **region and country** you want to view. 
        """)
      df_ori_11=df_ori[df_ori['Mode']="Registration"]
      Region_C1=df_ori_11['Region'].drop_duplicates()
      default_region1=['All region']
      default_region1.extend(Region_C1)
      region_choice=st.multiselect("", default_Region1)
      if ('All region' in region_choice1):
        df_ori_12=df_ori_11
      else:
        df_ori_12=df_ori_11.query("Region in @region_choice1")
      st.dataframe(df_ori_12)
      Country_C1=df_ori_11['Country'].drop_duplicates()
      default_country1=['All country']
      default_country1.extend(Country_C1)
      country_choice1=st.multiselect("", default_country1)
      if ('All country' in country_choice1):
        df_ori_13=df_ori_12
      else:
        df_ori_13=df_ori_12.query("Country in @country_choice1")
      st.dataframe(df_ori_13)

      with st.expander("Test-Taken volume view"): 
      st.write("""
        Please select which **region and country** you want to view. 
        """)
      df_ori_21=df_ori[df_ori['Mode']="TestTaken"]
      Region_C2=df_ori_21['Region'].drop_duplicates()
      default_region2=['All region']
      default_region2.extend(Region_C2)
      region_choice2=st.multiselect("", default_Region2)
      if ('All region' in region_choice2):
        df_ori_22=df_ori_21
      else:
        df_ori_22=df_ori_21.query("Region in @region_choice2")
      st.dataframe(df_ori_22)
      Country_C2=df_ori_21['Country'].drop_duplicates()
      default_country2=['All country']
      default_country2.extend(Country_C2)
      country_choice2=st.multiselect("", default_country2)
      if ('All country' in country_choice2):
        df_ori_23=df_ori_22
      else:
        df_ori_23=df_ori_22.query("Country in @country_choice")
      st.dataframe(df_ori_23)
         
# Filters
df_1=df_ori
st.sidebar.markdown("## Define **filters:**")
vol_1, vol_2 = st.sidebar.slider("Monthly volume range: ", min(df_ori.sum_score), max(df_ori.sum_score), (min(df_ori.sum_score), max(df_ori.sum_score)))
df_1=df_1.query("sum_score>=@vol_1 and sum_score<=@vol_2")

mod_choice=df_1['Mode'].drop_duplicates()
mod_choice.insert(0, "All")
reg_choice=df_1['Region'].drop_duplicates()
reg_choice.insert(0, "All")
cty_choice=df_1['Country'].drop_duplicates()
cty_choice.insert(0, "All")
yy_choice=df_1['Year'].drop_duplicates()
yy_choice.insert(0, "All")
mon_choice=df_1['Month'].drop_duplicates()
mon_choice.insert(0, "All")
#sex_choice = st.sidebar.selectbox('Select gender:', ['All', 'Male', 'Female'])

if mod_choice != "All":
  df_1=df_1.query("Mode==@mod_choice")
if reg_choice != "All":
  df_1=df_1.query("region==@reg_choice")
#mode_choice = st.sidebar.radio('Whether take the test at home:', ['All', 'Yes', 'No'])
if cty_choice != "All":
  df_1=df_1.query("Country==@cty_choice")
if yy_choice != "All":
  df_1=df_1.query("Year==@yy_choice")
if mon_choice != "All":
  df_1=df_1.query("Month==@mon_choice")


# figures display
rt_diff = (df_1["rt_total"].max() - df_1["rt_total"].min()) / 10
df_1["rt_scale"] = (df_1["rt_total"] - df_1["rt_total"].min()) / rt_diff + 1
df_1["rt_scale"] = pow(df_1["rt_scale"],2)
with col11:  
  title_ch1='Data Visualizaion'
  st.markdown(f'<h3 style="text-aligh: center;color: green;">{title_ch1}</h3>',unsafe_allow_html=True)
  title_ch2='****2D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch2}</h4>',unsafe_allow_html=True)
  with st.expander("Histogram:   distributions of sum score for male/female, under different test-taking mode: take the test at home or not "):    
    fig_hist1=px.histogram(df_1, x='sum_score', color='gender', facet_col='home_computer', marginal='box')
    st.plotly_chart(fig_hist1,  use_container_width=True, height=600)
  with st.expander("Bar charts:    sum score distribution for each age group"): 
    sorted_df = df_1.sort_values(by='age')
    sorted_df = sorted_df.reset_index(drop=True)
    opac = st.text_input('Opacity(0-1)', '0.8')
    fig_bar1=px.bar(sorted_df, y='sum_score', color='age_group', facet_row='age_group', opacity=float(opac), facet_row_spacing=0.01)
    st.plotly_chart(fig_bar1, use_container_width=True, height=400)
  with st.expander("Animation:    display the sum score pattern across states and the relationship with age"):  
    fig_ani1=px.bar(df_1, x='age_group', animation_frame='state_abbr', color='gender')
    fig_ani1.update_layout(transition = {'duration': 30000})
    st.plotly_chart(fig_ani1,  use_container_width=True, height=600)
    fig_ani2=px.scatter(df_1, y='sum_score', x='age', animation_frame='state_abbr', color='gender', size='rt_scale', size_max=60)
    fig_ani2.update_layout(transition = {'duration': 30000})
    st.plotly_chart(fig_ani2,  use_container_width=True, height=600)   
  with st.expander("Pie Charts:    check sum score distribution under country and state"):    
    fig_3=px.sunburst(df_1, color='sum_score',  path=['country_abbr','state_abbr'])
    st.plotly_chart(fig_3,   use_container_width=True, height=600)
  with st.expander("Tree Map:    check total response time distribution under country and state"):    
    fig_tree=px.treemap(df_1, color='rt_total',  path=['country_abbr','state_abbr'])
    st.plotly_chart(fig_tree, use_container_width=True, height=600)    
  with st.expander("choropleth map:    check score distribution from a choropleth map"):
    mean_df = df_1.groupby("country_abbr").mean()
    mean_df.reset_index(inplace=True)
    mean_df = mean_df.rename(columns = {'index':'country_abbr'})
    fig_4=px.choropleth(mean_df, color='sum_score',  locations='country_abbr', locationmode='ISO-3')
    st.plotly_chart(fig_4,  use_container_width=True, height=600)
  title_ch3='****3D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch3}</h4>',unsafe_allow_html=True)
  with st.expander("Check the relationship between total score, age, and test-taking mode (home taking or not) in an interactive 3D way"): 
    fig_scatter1=px.scatter_3d(df_1, y='sum_score', x='age', z='home_computer', color='gender', size='rt_scale', size_max=50)
    st.plotly_chart(fig_scatter1,  use_container_width=True, height=3000)
