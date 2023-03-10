import streamlit as st
import pandas as pd
import plotly 
import plotly.express as px
from plotly.subplots import make_subplots
import csv
import base64
import difflib
from calendar import month_name
from time import strptime
from openpyxl import Workbook
 
#######################glabal variables
#define functions
def raw_data(input_file, sheetname):
  df=pd.read_excel(open(input_file, 'rb'), sheet_name=sheetname )
  return df
 

##############################
st.set_page_config(layout="wide", initial_sidebar_state="auto")
col11, col12 = st.columns((3,1))
with col11:
  title_1="TOEFL iBT registration vs test-taken monthly volume "
  st.markdown(f'<h1 style="text-align: center;color: green;">{title_1}</h1>',unsafe_allow_html=True)
  subj_1="-- Fiscal year 2020 to 2023"
  st.markdown(f'<h2 style="text-align: center;color: green;">{subj_1}</h2>',unsafe_allow_html=True) 
  st.markdown ("By: Sarah Rhame")
  st.markdown("Original data set include 6672 registraion and 7017 test-taken records worldwide for fiscal years 2021 to 2023 (2020/10 to 2023/2).")
   
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
df_ori_0=raw_data("./data/DataReorg_output-merge HK MC to China.xlsx", "2018-2023")
#remove NA records              
df_ori_1=df_ori_0.dropna()
df_ori_1.reset_index(drop=True)
#remove records of 2023/3 to 2023/9
df_t=df_ori_1[df_ori_1['Year']==2023]
df_t=df_t[df_t['Month'].isin (['February', 'March','April','May', 'June','July','August', 'September'])]              
df_ori=pd.concat([df_ori_1, df_t, df_t]).drop_duplicates(keep=False)
df_ori_2 = df_ori.reset_index(drop=True)
df_t1=df_ori_2[df_ori_2['Year'].isin ([2017])]
df_ori=pd.concat([df_ori_2, df_t1, df_t1]).drop_duplicates(keep=False)
df_ori = df_ori.reset_index(drop=True)
# transder month full name to month number
df_ori['Month_N'] = [strptime(str(x), '%b').tm_mon for x in df_ori['Month'].str.slice(0, 3)]
#sort the whole data by region/country/year/month
df_ori.sort_values(by=['Mode', 'Region', 'Country', 'Year', 'Month_N'])
              
#df_ori['N_group']=""
#bins= [1,1000,3000,6000,9000,12000,15000,30000,40000,50000,60000,70000]
#labels = ['(level 1: <1000)','level 2: [1000,3000)','level 3: [3000-6000)','level 4: [6000-9000)','level 5: [9000-12000)','level 6: [12000-15000)','level 7: [15000-30000)','level 8: [30000-40000)','level 9: [40000-50000)','level 10: [50000-60000)','level 11: [>=60000)']
#df_ori['N_group'] = pd.cut(df_ori['N'], bins=bins, labels=labels, right=False)
#df_ori['N_group'] = df_ori['N_group'].cat.add_categories('unknown').fillna('unknown')  

             
with col11:  
  with st.expander("**Registraion volume view**"): 
      st.write("""
        Please select which **region and country** you want to view. 
        """)
      df_ori_11=df_ori[df_ori['Mode']=="Registration"]
      Region_C1=df_ori_11['Region'].drop_duplicates()
      Region_C1=sorted(Region_C1)
      default_region1=['All region']
      default_region1.extend(Region_C1)
      region_choice1=st.multiselect("What registration region(s) you are interested", default_region1)
      if ('All region' in region_choice1):
        df_ori_12=df_ori_11
      else:
        df_ori_12=df_ori_11.query("Region in @region_choice1")
      st.dataframe(df_ori_12)
      Country_C1=df_ori_12['Country'].drop_duplicates()
      Country_C1=sorted(Country_C1)
      default_country1=['All country']
      default_country1.extend(Country_C1)
      country_choice1=st.multiselect("What registration countries you are interested", default_country1)
      if ('All country' in country_choice1):
        df_ori_13=df_ori_12
      else:
        df_ori_13=df_ori_12.query("Country in @country_choice1")
      st.dataframe(df_ori_13)

  with st.expander("Test-Taken volume view"): 
      st.write("""
        Please select which **region and country** you want to view. 
        """)
      df_ori_21=df_ori[df_ori['Mode']=="TestTaken"]
      Region_C2=df_ori_21['Region'].drop_duplicates()
      Region_C2=sorted(Region_C2)
      default_region2=['All region']
      default_region2.extend(Region_C2)
      region_choice2=st.multiselect("What test-taken region(s) you are interested", default_region2)
      if ('All region' in region_choice2):
        df_ori_22=df_ori_21
      else:
        df_ori_22=df_ori_21.query("Region in @region_choice2")
      st.dataframe(df_ori_22)
      Country_C2=df_ori_22['Country'].drop_duplicates()
      Country_C2=sorted(Country_C2)
      default_country2=['All country']
      default_country2.extend(Country_C2)
      country_choice2=st.multiselect("What test-taken countries you are interested", default_country2)
      if ('All country' in country_choice2):
        df_ori_23=df_ori_22
      else:
        df_ori_23=df_ori_22.query("Country in @country_choice2")
      st.dataframe(df_ori_23)
         
# Filters
df_1=df_ori
st.sidebar.markdown("## Define **filters:**")
vol_1, vol_2 = st.sidebar.slider("Monthly volume range: ", min(df_ori.N), max(df_ori.N), (min(df_ori.N), max(df_ori.N)))
df_1=df_1.query("N>=@vol_1 and N<=@vol_2")

mod_choice1=df_1['Mode'].drop_duplicates().tolist()
mod_choice=mod_choice1
mod_choice.insert(0, 'All')
default_mod=mod_choice.index('All')
reg_choice1=df_1['Region'].drop_duplicates().tolist()
reg_choice1=sorted(reg_choice1)
reg_choice=reg_choice1
reg_choice.insert(0, 'All')
default_reg=reg_choice.index('All')
cty_choice1=df_1['Country'].drop_duplicates().tolist()
cty_choice1=sorted(cty_choice1)
cty_choice=cty_choice1
cty_choice.insert(0, 'All')
default_cty=cty_choice.index('All')
yy_choice1=df_1['Year'].drop_duplicates().tolist()
yy_choice=yy_choice1
yy_choice.insert(0, 'All')
default_yy=yy_choice.index('All')
mon_choice1=df_1['Month'].drop_duplicates().tolist()
month_lookup = list(month_name)
mon_choice1=sorted(mon_choice1, key=month_lookup.index)
mon_choice=mon_choice1
mon_choice.insert(0, 'All')
default_mon=mon_choice.index('All')

mod_select = st.sidebar.selectbox('Select mode:', mod_choice, index=default_mod)
reg_select = st.sidebar.selectbox('Select region:', reg_choice, index=default_reg) 
cty_select = st.sidebar.selectbox('Select country:', cty_choice, index=default_cty)
yy_select = st.sidebar.selectbox('Select year:', yy_choice, index=default_yy)
mon_select = st.sidebar.selectbox('Select month:', mon_choice, index=default_mon)

if mod_select != "All":
  df_1=df_1.query("Mode==@mod_select")
#else:
   #df_1=df_1.query("Mode in @mod_choice1")
 
if reg_select != "All":
  df_1=df_1.query("Region==@reg_select")
#else:
  #df_1=df_1.query("Region in @reg_choice1")

if cty_choice != "All":
  df_1=df_1.query("Country==@cty_select")
#else:
  #df_1=df_1.query("Country in @cty_choice1")

if yy_select != "All":
  df_1=df_1.query("Year==@yy_select")
#else:
  #df_1=df_1.query("Year in @yy_choice1")

if mon_select != "All":
  df_1=df_1.query("Month==@mon_select")
#else:
  #df_1=df_1.query("Month in @mon_choice1")
 

# figures display, based on file df_1 which is data after filters apply
N_diff = (df_1["N"].max() - df_1["N"].min()) / 10
if N_diff == 0:
   N_diff=1
df_1["N_scale"] = (df_1["N"] - df_1["N"].min()) / N_diff + 1
#df_1["N_scale"] = pow(df_1["N_scale"],2)
df_1['YY_Mon']=df_1['Year'].astype(str)+"_"+df_1['Month_N'].astype(str)
df_1['Reg_Cty']=df_1['Region']+"_"+df_1['Country']
df_2=df_1

#df_1.sort_values(by=['Mode', 'Region', 'Country', 'Year', 'Month_N'])
df_1_res=df_1[df_1['Mode']=="Registration"]
df_1_taken=df_1[df_1['Mode']=="TestTaken"] 

df_1_2020=df_1[df_1['Year']==2020] 
 
with col11:  
 
  title_ch1='Volume Data Visualizaion'
  st.markdown(f'<h3 style="text-aligh: center;color: green;">{title_ch1}</h3>',unsafe_allow_html=True)
  title_ch2='****2D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch2}</h4>',unsafe_allow_html=True)
  
  #with st.expander("Histogram: distributions of monthly registration/TestTaken volume for each region/country/year/month "):    
     #fig_hist1 = px.histogram(df_1_2020, x='N_group', animation_frame='Reg_Cty', color='Month', facet_row='Mode', marginal='box')
     #st.plotly_chart(fig_hist1,  use_container_width=True, height=800)

  #with st.expander("Bar charts:  monthly registration/TestTaken volume distribution for each region/country/year/month"): 
    #sorted_df = df_1.sort_values(by=['Region', 'Country', 'Year', 'Month_N'])
    #sorted_df = sorted_df.reset_index(drop=True)
    #opac = st.text_input('Opacity(0-1)', '0.8')
    #fig_bar1=px.bar(sorted_df, y='N', color='Reg_Cty', facet_row='Mode', opacity=float(opac), facet_row_spacing=0.01)
    #st.plotly_chart(fig_bar1, use_container_width=True, height=400)
    
  with st.expander("Animation:    display the volume pattern for each region/country/year/month"):  
    #fig_ani1=px.bar(df_1, x='YY_Mon', y='N', animation_frame='Reg_Cty', color='Mode')
    #fig_ani1.update_layout(transition = {'duration': 30000})
    #st.plotly_chart(fig_ani1,  use_container_width=True, height=600)
    fig_ani2=px.scatter(df_1, y='N', x='YY_Mon', animation_frame='Reg_Cty',  color='Mode', size='N_scale', size_max=60)
    fig_ani2.update_layout(transition = {'duration': 10000})
    st.plotly_chart(fig_ani2,  use_container_width=True, height=600)   
  
  with st.expander("Pie Charts: check volume distribution for each region/country/year/month. Top left plot is for registration volume and the top right plot is for test-taken volume. The plot at bottom is for both types of volumes."):    
    fig_31=px.sunburst(df_1_res, color='N', values='N', path=['Region', 'Country', 'Year', 'Month'], color_continuous_scale='Inferno')
    #st.plotly_chart(fig_31,   use_container_width=True, height=600)
    fig_32=px.sunburst(df_1_taken, color='N', values='N', path=['Region', 'Country', 'Year', 'Month'], color_continuous_scale='Inferno')
    #st.plotly_chart(fig_32,   use_container_width=True, height=600) 
    fig_33=px.sunburst(df_1, color='N', values='N', path=['Mode', 'Region', 'Country', 'Year', 'Month'], color_continuous_scale='Inferno')
    fig_3 = make_subplots(rows=1, cols=2, specs=[
          [{"type": "sunburst"}, {"type": "sunburst"}]
          ])
    fig_3.add_trace(fig_31.data[0], row=1, col=1)
    fig_3.add_trace(fig_32.data[0], row=1, col=2)
    st.plotly_chart(fig_3,   use_container_width=True, height=600) 
    st.plotly_chart(fig_33,   use_container_width=True, height=600) 
  
  with st.expander("Tree Map:    check volume distribution for each region/country/year/month"):    
    fig_tree1=px.treemap(df_1, color='N',  path=['Mode', 'Region', 'Country', 'Year', 'Month'])
    st.plotly_chart(fig_tree1, use_container_width=True, height=600) 
        
  with st.expander("choropleth map:    check volume distribution from a choropleth map"):
    mean_df_res = df_1_res.groupby("Country").mean()
    mean_df_res.reset_index(inplace=True)
    mean_df_res = mean_df_res.rename(columns = {'index':'Country'})
    fig_4=px.choropleth(mean_df_res, color='N',  locations='Country', locationmode='country names')
    st.plotly_chart(fig_4,  use_container_width=True, height=600)
  title_ch3='****3D interactive plots********'
  st.markdown(f'<h4 style="text-aligh: center;color: green;">{title_ch3}</h4>',unsafe_allow_html=True)
  
  with st.expander("Check the relationship between volume distribution for each region/country/year/month and test-taking mode (registration vs test taken) in an interactive 3D way"):
    fig_scatter1=px.scatter_3d(df_1, y='N', x='YY_Mon', z='Reg_Cty', color='Mode', size='N_scale', size_max=50)
    st.plotly_chart(fig_scatter1,  use_container_width=True, height=600)
