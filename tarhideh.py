# 1- import necessary libraries
import streamlit as st
import pandas as pd
from datetime import date 
import datetime
import openpyxl
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu


# Page style
st.set_page_config(page_title='Tarh-ideh BTL Agency' ,
			page_icon = "logo.png",
			layout='wide')
			
hide_style = """
		<style>
		#MainMenu {visibility : hidden;}
		footer {visibility : hidden;}
		header {visibility : hidden;}
		</style>
		"""
		
st.markdown(hide_style , unsafe_allow_html =True)		
		
		
# Create a time and date for dataframe table to check sales situation per time
Today = date.today()
current_date = Today.strftime("%yyyy-%m-%d")

Now = datetime.datetime.now()
current_time = Now.strftime("%H:%M")

		
names = ["پروموتر طرح ایده"]
usernames = ['tarh-ideh']

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
	hashed_passwords = pickle.load(file)
			

authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
		'some_cookie_name', 'some_signature_key',cookie_expiry_days =30)
			
name , authentication_status , username = authenticator.login(form_name="Login",location="main")


				

# Check user's authentication
if authentication_status == False:
	st.error('! نام کاربری یا پسورد اشتباه است ')
	
if authentication_status == None:	
	st.warning(' ! نام کاربری و پسورد خود را وارد کنید ')
	
						
if authentication_status :
	st.sidebar.header('Welcome Buddy 👋')
	
	
	
	authenticator.logout("Logout","sidebar")
	# Enter data by promoters
	if username == 'tarh-ideh' :
		City = ["شهر خود را انتخاب کنید","اهواز" , "کرمانشاه" , "تبریز"]
		with st.sidebar:
			selected = option_menu("Menu",['About','Test'] , icons = ['house','gear'] , default_index=0)
		
		if selected == 'About':
			
			with st.sidebar:
		
				with st.form(key= 'form1' , clear_on_submit=True):
					checkbox = st.selectbox(label = ": شهر خود را انتخاب کنید" , options=City)
					name = st.text_input(": نام خود را وارد کنید")
			
					submit_button = st.form_submit_button(label = 'Submit')
		
		
		
			if checkbox == "تبریز" :
			# Create a increment button
			
				with st.form(key= 'form2' , clear_on_submit=True):
					No_of_promoted_people = st.number_input(': تعداد افراد پروموت شده', value = 0)
					No_of_sample = st.number_input(': تعداد سمپل ارائه شده', value = 0)
					first_product = st.number_input(': پنیر لبنه کلاسیک آنا', value = 0)
					Second_product = st.number_input(': پنیر لبنه کم چرب آنا', value = 0)
					
					
					submit_button = st.form_submit_button(label = 'Submit')
				
			
			# Create situation table
				df = pd.DataFrame({'Name': name ,
							   'Date': Today ,
							   'Time' : current_time ,
							   'No. of promoted people':No_of_promoted_people ,
							   'No. of sample' : No_of_sample ,
							   'Amount sales of first product': [first_product] ,
							   'Amount sales of second product':[Second_product]})
							   
							   
				st.write(df)
				
				
				
				file_path = 'D:\\Data\\Orginal Data.xlsx'	
				new_data = df
				df_new = pd.DataFrame(new_data)

				df_existing = pd.read_excel(file_path)
				df_combined = df_existing.append(df_new ,ignore_index=True)

				df_combined.to_excel(file_path , index=False)			
		
		
		
			   
			
					   	
			
			
			
			
		
							