#pip install mysql-connector-python
#pip install streamlit plotly mysql-connector-python
#pip install streamlit
import mysql.connector 
import pandas as pd
#import psycopg2
import streamlit as st
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import requests
import base64
import mysql # connect to the database
#establishing the connection
conn = mysql.connector.connect(user='root', password='Csa1809', host='localhost', database="phonepe_pulse")
# create a cursor object

cursor = conn.cursor()
#with st.sidebar:
SELECT = option_menu(
    menu_title = None,
    options = ["Home","About","Data Insight","Profile"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})

#---------------------Data Insights -----------------#

if SELECT == "Data Insight":
    st.title("DATA INSIGHTS")
    st.write("----")
    st.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\data banner.png"))
    st.subheader("Here are some of the basic insights of data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District"]
               #1
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT States, Transaction_Year, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM top_tran GROUP BY States, Transaction_Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Transaction_Year', 'Transaction_Amount'])
        st.write(df)
        st.title("Top 10 states and amount of transaction")
        st.bar_chart(data=df,x="Transaction_Amount",y="States")
         #2        
    elif select=="List 10 states based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT States, SUM(Transaction_Count) as Total FROM top_tran GROUP BY States ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Total_Transaction'])
        st.write(df)
        st.title("List 10 states based on type and amount of transaction")
        st.bar_chart(data=df,x="Total_Transaction",y="States")
         #3   
    elif select=="Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute("SELECT DISTINCT Transaction_Type, SUM(Transaction_Amount) AS Amount FROM agg_user GROUP BY Transaction_Type ORDER BY Amount DESC LIMIT 5");
        df = pd.DataFrame(cursor.fetchall(),columns=['Transaction_Type','Transaction_Amount'])
        st.write(df)
        st.title("Top 5 Transaction_Type based on Transaction_Amount")
        st.bar_chart(data=df,x="Transaction_Type",y="Amount")
         #4           
    elif select=="Top 10 Registered-users based on States and District":
        cursor.execute("SELECT DISTINCT State, District, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY State, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','RegisteredUsers'])
        st.write(df)
        st.title("Top 10 Registered-users based on States and District")
        st.bar_chart(data=df,x="State",y="RegisteredUsers")   
            #5     
    elif select=="Top 10 Districts based on states and Count of transaction":
        cursor.execute("SELECT DISTINCT States,District,SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        st.write(df)
        st.title("Top 10 Districts based on states and Count of transaction")
        st.bar_chart(data=df,x="States",y="Transaction_Count") 
            #6          
    elif select=="List 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT States,Transaction_year,SUM(Transaction_Amount) AS Amount FROM agg_trans GROUP BY States, Transaction_year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Transaction_year','Transaction_Amount'])
        st.write(df)
        st.title("Least 10 Districts based on states and amount of transaction")
        st.bar_chart(data=df,x="States",y="Transaction_Amount")
            
            #7     
    elif select=="List 10 Transaction_Count based on Districts and states":
        cursor.execute("SELECT DISTINCT States, District, SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        st.write(df)
        st.title("List 10 Transaction_Count based on Districts and states")
        st.bar_chart(data=df,x="States",y="Transaction_Count")
            
            #8        
    elif select=="Top 10 RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT States,District, SUM(RegisteredUsers) AS Users FROM map_user GROUP BY States,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
        st.write(df)
        st.title("Top 10 RegisteredUsers based on states and District")
        st.bar_chart(data=df,x="States",y="RegisteredUsers")

    cursor = conn.cursor()
# execute a SELECT statement
    cursor.execute("SELECT * FROM agg_trans")
# fetch all rows
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['States', 'Transaction_Year', 'Quarters', 'Transaction_Type', 'Transaction_Count','Transaction_Amount'])
    fig = px.choropleth(df, locations="States", scope="asia", color="States", hover_name="States",
        title="Live Geo Visualization of India")
    st.plotly_chart(fig)

#----------------Home----------------------#

if SELECT == "Home":
    col1,col2, = st.columns(2)
    col1.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\phonepewording.png"),width = 300)
    st.title("Click The Button To download The App Now")
    st.download_button("DOWNLOAD", "https://www.phonepe.com/app-download/")
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
    with col2:
        st.video(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\transactionvideo.mp4")     
    
    
#----------------About-----------------------#

if SELECT == "About":
    st.video(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\home1st video.mp4")
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\About.png"))
    with col2:
        st.subheader("PhonePe is a digital wallet and online payment system that allows users to transfer money, pay bills, and recharge mobile phones. It was founded in December 2015 and is headquartered in Bangalore, India. PhonePe is available in 11 Indian languages and is accepted by over 200 million users and 15 million merchants across India. It is owned by Flipkart, one of India's largest e-commerce companies.")
    st.write("---")
    st.title("THE GROWTH OF PHONEPE")
    st.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\partner-section-desk.png"))
    st.subheader("Phonepe became a leading digital payments company")
    st.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\leading.png"))
    with open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\annual report.pdf","rb") as f:
     data = f.read()
     st.title("Click the button to download the Annual Report")
     st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    

#----------------------Profile---------------#

if SELECT == "Profile":
    st.write("---")
    st.title("Hi! This is Akshyashree")
    st.write("---")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("Mail : snakshyashree@gmail.com")
    with col2:
        st.write("Github : https://github.com/Akshyashree")
    with col3:
        st.write("Linkedin : https://www.linkedin.com/in/akshyashree")
    st.write("---")
    st.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\aboutme.png"),width=500)
    st.write("An aspiring person Currently working as .NET developer at CTS, Looking for career transition career in Data Science. Strong in design and integration with intuitive problem-solving skills. Passionate about implementing and launching new projects. Ability to translate business requirements into technical solutions.")
    st.write("---")
    st.title("About this Project")
    st.image(Image.open(r"C:\Users\snaks\OneDrive\Desktop\Phonepe_Pulse_Data_Visualization-main\myfolder\maxresdefault.jpg"))
    st.write("The result of this project will be a live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner. The dashboard will have at least 10 different dropdown options for users to select different facts and figures to display. The data will be stored in a MySQL database for efficient retrieval and the dashboard will be dynamically updated to reflect the latest data. Users will be able to access the dashboard from a web browser and easily navigate the different visualizations and facts and figures displayed. The dashboard will provide valuable insights and information about the data in the Phonepe pulse Github repository, making it a valuable tool for data analysis and decision-making. Overall, the result of this project will be a comprehensive and user-friendly solution for extracting, transforming, and visualizing data from the Phonepe pulse Github repository.")
    



