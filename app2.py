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
import plotly.graph_objects as go



st.set_page_config(page_title='Germany Population' ,
					page_icon = ":busts_in_silhouette:",
					layout='wide')
					

names =['Mohammad Mosayebi','Mohsen Mosayebi']
usernames = ['mmosayebi','momosayebi']

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
	hashed_passwords = pickle.load(file)
	
	
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
		'some_cookie_name', 'some_signature_key',cookie_expiry_days =30)
		
		
			
name , authentication_status , username = authenticator.login(form_name="Login",location="main")

hide_style = """
				<style>
				#MainMenu {visibility : hidden;}
				footer {visibility : hidden;}
				header {visibility : hidden;}
				</style>
				"""



if authentication_status :			
	# sidebar
	authenticator.logout("Logout","sidebar")
	if username == 'mmosayebi' :
			# reading and cleaning the data :
		df = pd.read_excel('D:/Mohammad/Datasets/CSV Files/Population.xlsx',sheet_name='Cleaned Data')
		df['Date'] = pd.to_datetime(df['Date'])
		df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
		
		
		# page title
		#st.set_page_config(page_title='Germany Population' ,
					#page_icon = ":busts_in_silhouette:",
					#layout='wide')
					
		
				
		st.markdown(hide_style , unsafe_allow_html =True)
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
	elif username == 'momosayebi':
				# Reading CSV File
		df = pd.read_csv('D:/Mohammad/Datasets/CSV Files/msft.csv')
		# Transforming The Dataset
		df = df.dropna()
		df['Date'] = pd.to_datetime(df['Date'])
		df = df.sort_values(by=['Date'])
		df['Year'] = df['Date'].dt.strftime('%Y')
		df['Month'] = df['Date'].dt.strftime('%m')
		df['Day'] = df['Date'].dt.strftime('%d')
		
		
		# Seting Page
		#st.set_page_config(page_title='Books Dashboard',
					#page_icon=':books:',
					#layout='wide',
					#initial_sidebar_state = 'collapsed')
					
		hide_style = """
					<style>
					#MainMenu {visibility : hidden;}
					footer {visibility : hidden;}
					header {visibility : hidden;}
					</style>
					"""		
		st.markdown(hide_style , unsafe_allow_html =True)			
		st.title(':books: Books Dashboard')		
		st.markdown('##')
		
		# Multiselect Columns
		first_column , second_column = st.columns(2)
		with first_column :
			date = st.multiselect('Select year :' ,
				options = df['Year'].unique(),
				default = df['Year'].unique().max())
				
		with second_column :
			month = st.multiselect('select month :',
			options = df['Month'].unique(),
			default = df['Month'].unique().max())			
					
		# Sidebar
		#authenticator.logout('Logout','sidebar')
		st.sidebar.title(f'Welcome {name}')
				
		st.sidebar.header("Please select your filters : ")
		category = st.sidebar.multiselect(
			'Select a category :',
			options = df['Category'].unique(),
			default = df['Category'].unique()
		)
		 	
		 
		df_selection = df.query(
				"Category == @category & Year == @date & Month == @month")		
				
				
		 
		
		# Creating KPI's
		average_of_rating = round(df_selection['Rating'].mean(),0)
		No_of_people_rating = df_selection['No of people Rated'].sum()
		available_items = df_selection['Category'].count()
		
		left_column , middle_column , right_column = st.columns(3)
		with left_column:
			st.subheader('Average Rating :')
			st.subheader(f'{average_of_rating}')	
		with middle_column:
			st.subheader('No. of People Rating :')
			st.subheader(f'{No_of_people_rating:,}')
		with right_column:
			st.subheader('Available Items :')
			st.subheader(f'{available_items:,}')
			
		st.markdown('---')	
		
		
		# Creating Charts
		Average_rating_of_items = df_selection.groupby(['Category'],as_index=False)['Rating'].mean()
		Average_rating_of_items['Rating'] = Average_rating_of_items['Rating'].apply(lambda x: float("{:.2f}".format(x)))
		people_rating = df_selection.groupby(['Category'],as_index=False)['No of people Rated'].sum()
		
		#	| First Column = Bar Chart
		left_column , right_column = st.columns(2)
		with left_column :
			x1 = Average_rating_of_items['Category']
			y1 = Average_rating_of_items['Rating']	
			
			layout = go.Layout(xaxis={'title':'Book Categories','tickangle':360,'showgrid':False,'showline':False},
			                   yaxis={'title':'Number of people Rating','showgrid':False,'showline':False}
							   , title='Average of Rated Books Per Category',
							   width=500 , height=500)	
							   
			second_graph = go.Bar(x=x1,y=y1,text=y1,
				textfont={'size':17},textposition='auto',hoverinfo='x+y')
				
			fig = go.Figure(data = second_graph , layout = layout)	
				
			st.plotly_chart(fig,config={ 'modeBarButtonsToRemove': ['zoom', 'pan','select','lasso2d',
																			'zoomIn','zoomOut','toImage'] })
		#	| Second Column = Pie Chart
		with right_column :
			label = people_rating['Category']
			values = people_rating['No of people Rated']
			
			layout2 = go.Layout(legend={'itemclick':'toggle' , 'title':'Book Categories'} ,
								title='Percentage of Categories Rated By People',
								width=500 , height=500)
								
			first_graph = go.Pie(labels=label , values=values ,hoverinfo='label+value+percent' 
		               , titleposition='top center' ,titlefont={'size':70},textfont={'size':18}
					   )
					   
			fig2 = go.Figure(data = first_graph , layout = layout2)	
				
			st.plotly_chart(fig2,config={ 'modeBarButtonsToRemove': ['zoom', 'pan','select','lasso2d',
																			'zoomIn','zoomOut','toImage'] })	
		
		# Hiding Header , Footer and Menue Style																					
		hide_style = """
				<style>
				#MainMenu {visibility : hidden;}
				footer {visibility : hidden;}
				header {visibility : hidden;}
				</style>
				"""		
		st.markdown(hide_style , unsafe_allow_html =True)
elif authentication_status == False:
	st.error('Username/Password is incorrect !')
elif authentication_status == None:	
	st.warning('Insert username and password !')		



