#!/usr/bin/env python
# coding: utf-8


# Import libraries :
import pickle
from pathlib import Path


import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
from datetime import datetime
import streamlit_authenticator as stauth
import matplotlib.pyplot as plt



# reading and cleaning the data :
df = pd.read_excel('D:/Mohammad/Datasets/CSV Files/Population.xlsx',sheet_name='Cleaned Data')
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')


# page title
st.set_page_config(page_title='Germany Population' ,
			page_icon = ":busts_in_silhouette:",
			layout='wide')
			
hide_style = """
		<style>
		#MainMenu {visibility : hidden;}
		footer {visibility : hidden;}
		header {visibility : hidden;}
		</style>
		"""
		
st.markdown(hide_style , unsafe_allow_html =True)			

names =['Mohammad Mosayebi','Mohsen Mosayebi']
usernames = ['mmosayebi','momosayebi']

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
	hashed_passwords = pickle.load(file)
	
	
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
		'some_cookie_name', 'some_signature_key',cookie_expiry_days =30)
		
		
			
name , authentication_status , username = authenticator.login(form_name="Login",location="main")



if authentication_status == False:
	st.error('Username/Password is incorrect !')
if authentication_status == None:	
	st.warning('Insert username and password !')

if authentication_status :			
	# sidebar
	authenticator.logout("Logout","sidebar")
	st.sidebar.title(f'Welcome {name}')
	st.sidebar.header('Please select a value :')
	date = st.sidebar.multiselect(
			'Filter your date :',
			options = df['Date'].unique(),
			default = df['Date'].max()
			)		
	gender = st.sidebar.multiselect(
			'Filter your gender :',
			options = df['Gender'].unique(),
			default = df['Gender'].unique()
			)	
	nationality = st.sidebar.multiselect(
			'Filter your nationality :',
			options = df['Nationality'].unique(),
			default = df['Nationality'].unique()
			)				
			
				
	df_selection = df.query(
		"Date == @date & Gender == @gender & Nationality == @nationality")			
	
	
	# In[2]:
		
			
	# Mainpage
	st.title(':busts_in_silhouette:  Germany Population')
	st.markdown('##')
	
	# Top KPI's
	total_population = df_selection['Population'].sum()
	average_of_age = int(round(df_selection['Age'].mean(),0))
	
	first_column , second_column = st.columns(2)
	with first_column:
		st.subheader('Total Population :')
		st.subheader(f"{total_population:,}")
	with second_column:
		st.subheader('Average of Age :')
		st.subheader(average_of_age)	
		
	st.markdown("---")	
	
	
	# Charts
	df_population = df_selection.groupby(['Date'],as_index=False)['Population'].sum()
	
	first_graph = px.line(
		data_frame=df_population ,
		x='Date',
		y = 'Population',
		text = 'Population',
		title='<b>Population Per Year</b>')
		
	st.plotly_chart(first_graph)	
	
	# ------
	fig = plt.figure(figsize=(200,100))
	plt.bar(df_population['Date'],df_population['Population'])
	fig.title('Some title')
	st.pyplot(fig)
	
	hide_style = """
		<style>
		#MainMenu {visibility : hidden;}
		footer {visibility : hidden;}
		header {visibility : hidden;}
		</style>
		"""
		
	st.markdown(hide_style , unsafe_allow_html =True)	
	# In[ ]:




