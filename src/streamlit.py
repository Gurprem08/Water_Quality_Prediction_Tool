import pandas as pd
import streamlit as st
import joblib
import mysql.connector
from streamlit_option_menu import option_menu
from streamlit_navigation_bar import st_navbar
from ml_model import predict  # Import the predict function
from mysql.connector import Error
from water_quality import calculate_wqi
import pyrebase
import firebase

st.set_page_config(layout="wide")

# Function to connect to MySQL database
def create_db_connection():
    try:
        connection = mysql.connector.connect(
        user= 'root',                # Replace with your actual MySQL username
        password= 'Guru@12345678',   # Replace with your actual MySQL password
        host= '127.0.0.1',           # Host where your MySQL server is running
        port= 3306,                  # Port number for your MySQL server
        database= 'Streamlit_DB'     # Replace with your actual database name
        )

        if connection.is_connected():
            st.success("Successfully connected to the database")
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to insert data into the MySQL database
def insert_data_to_db(df):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS water_quality_predictions (
                
                    pH FLOAT, 
                    EC FLOAT, 
                    TDS FLOAT, 
                    Temperature FLOAT,
                    p_CO3 FLOAT, 
                    p_CL FLOAT, 
                    p_SO4 FLOAT, 
                    p_TH FLOAT, 
                    p_CA FLOAT, 
                    p_MG FLOAT, 
                    p_NA FLOAT 
                )
            """)

            for _, row in df.iterrows():
                # Convert each value in the row to a native Python float type
                values = tuple(float(x) for x in row)
                cursor.execute(
                    """
                    INSERT INTO water_quality_predictions 
                    (pH, EC, TDS, Temperature, p_CO3, p_CL, p_SO4, p_TH, p_CA, p_MG, p_NA) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    values
                )
            connection.commit()
            st.success("Data inserted into the database successfully!")
            st.balloons()
        except Error as e:
            st.error(f"Error while inserting data: {e}")
        finally:
            cursor.close()
            connection.close()



# Main function to run the Streamlit app
def main():

    # Custom CSS for background color
    custom_css = """
<style>
body {
    background-color: rgb(144, 238, 144); /* Light green background color */
}
</style>
"""

# Inject the custom CSS into the Streamlit app
    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown(
    """
    <style>
    /* Remove top margin/padding and set full viewport height */
    .main {
        padding-top: 50px;
    }
    .viewerBadge_container__1QSob {
        display: none;
    }
    .viewerBadge_link__1S137 {
        display: none;
    }
    .block-container {
        padding-top: 5px;
        padding-bottom: 0px;
        padding-left: 0px;
        padding-right: 0px;
    }
    body {
        margin: 0vh;
        padding: 50vh;
        height: 100vh;
        background-color:white;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1000px;
        background-color: "black";
        width: 100%;
    }
    .header-container .logo {
        font-size: 24px;
        font-weight: bold;
        color: "black";
    }
    .centered-text {
        text-align: center;
    }
    .custom-header {
        font-size: 24px;
        font-weight: bold;
        color: #007bff;
        text-align: center;
    }
    .custom-paragraph {
        font-size: 18px;
        color: #333333;
        text-align: center;
    }
 
    .iframe-container {
        flex: 1;
        alig-items:center;
        justpfy-content: center;
        width: 100%;
        height: calc(100vh - 80px); /* Adjust height based on the header height */
    }
    iframe {
        width: 100%;
        height: 100%;
        border: 0;
    }

    [data-testid="stForm"] {
    font-family: Arial, sans-serif; /* Change font family */
    font-size: 50px; /* Change font size */
    color: white; /* Change text color */
    }

    .center-text {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px; /* Adjust the height as needed */
        font-size: 24px;
        color: green;
    }
    .centered-dataframe {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .dataframe-container {
        width: 50%;
    }
    .stAlert {
        width: 100%; /* Make sure the alert takes the full width */
        text-align: center; /* Center align the text inside the alert */
        font-size: 100px;
    }
    .video-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Adjust this value if needed */
        background-color: #f0f0f0; /* Optional: background color */
    }}
    iframe {{
        width: 80%; /* Adjust this value to control the video width */
        max-width: 800px; /* Optional: limit the max width */
        border: none; /* Remove iframe border */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
    
# Define CSS styles
    # Define CSS styles
    st.markdown(
        """
        <div class = "header-container"; style="display: flex; align-items: center; justify-content: Center; padding: 0px; background-color: black; margin:0px;">
            <div style="font-size: 50px; font-weight: bold; color: White; padding:10px;">Aqua Insights</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Inject the option menu into the navbar container
    with st.container():

        page = option_menu(
        menu_title=None,  # Hide the menu title to align it with the header
        options=["Home", "Prediction", "Visualize", "About", "Login"],  # required
        icons=["house", "water", "bar-chart", "info-circle"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",  # Make the menu horizontal
        styles= { 
            "container": {"padding": "50", "background-color": "black","width":"1000in"},
            "icon": {"color": "red", "font-size": "18px"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin":"10px", "--hover-color": "grey"},
            "nav-link-selected": {"background-color": "grey", "color": "black"},
        }
    )



    # Display content based on the selected page
    if page == "Home":
        home()
    elif page == "Prediction":
        predict_water_quality()
    elif page == "Visualize":
        data_analysis()
    elif page == "About":
        about()
    elif page == "Login":
        login()    

# Function to display the home page
def home():
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 20vh; flex-direction: column;margin:100px">
    <div>
        <h1>Welcome to the Water Quality Prediction App</h1>
    </div>
    <div>
        <h2>This app is designed to predict the water quality based on various factors.</h2>
    </div>
</div>

    """, unsafe_allow_html=True
    )

# Function to display the water quality prediction page
def predict_water_quality():

    st.markdown("""
      <div style="display: flex; justify-content: center; align-items: center; height: 20vh; flex-direction: column; margin:100px">
    <div>
        <h1>Predict Water Quality Parameters</h1>
    </div>
    <div>
        <h2>Enter the water quality parameters and obtain the Water Quality Index</h2>
    </div>
</div>          
    """, unsafe_allow_html=True
    )

    
# Example form to enter water quality parameters
    with st.form("water_quality_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)
        ec = st.number_input("EC (µS/cm)", min_value=0.0, value=0.0)
        tds = st.number_input("Total Dissolved Solids (mg/L)", min_value=0.0, value=0.0)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, value=20.0)
        submit_button = st.form_submit_button(label="Submit")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        try:
            parameters = [ph, ec, tds, temperature]
            predictions = predict(parameters)
    
    # Create a DataFrame with the input and predicted values
            df = pd.DataFrame({
            'pH': [ph],
            'EC': [ec],
            'TDS': [tds],
            'Temperature': [temperature],
            'p_CO3': [predictions['CO3']],
            'p_CL': [predictions['Cl']],
            'p_SO4': [predictions['SO4']],
            'p_TH': [predictions['TH']],
            'p_CA': [predictions['Ca']],
            'p_MG': [predictions['Mg']],
            'p_NA': [predictions['Na']],
        
            })
            




# # Centered success message
            # st.markdown('<div class="center-text"><div class="stAlert">Water Quality Parameters Submitted Successfully!</div></div>', unsafe_allow_html=True)

            st.success("Water Quality Parameters Submitted Successfully!")
            st.markdown('<div class="center-text">Entered and Predicted Parameters</div>', unsafe_allow_html=True)

            st.markdown('<div class="centered-dataframe"><div class = "dataframe-container">', unsafe_allow_html=True)
            st.dataframe(df,use_container_width=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            
    # # Calculate WAWQI
     # Calculate WAWQI
            standard_values = {
    'p_CO3': 250,
    'p_CL': 250,
    'p_SO4': 250,
    'p_TH': 500,
    'p_CA': 75,
    'p_MG': 30,
    'p_NA': 200,
    'pH': 8.5,
    'TDS': 500
}

            ideal_values = {
    'p_CO3': 0,
    'p_CL': 0,
    'p_SO4': 0,
    'p_TH': 0,
    'p_CA': 0,
    'p_MG': 0,
    'p_NA': 0,
    'pH': 7,
    'TDS': 0
}

            weights = {
    'p_CO3': 1,
    'p_CL': 1,
    'p_SO4': 1,
    'p_TH': 1,
    'p_CA': 1,
    'p_MG': 1,
    'p_NA': 1,
    'pH': 1,
    'TDS': 1
}

            # standard_values = {
            #     'p_CO3': 250, 'p_CL': 250, 'p_SO4': 250, 'p_TH': 500, 'p_CA': 75, 'p_MG': 30, 'p_NA': 200, 
            #     'pH': 8.5, 'TDS': 500
            # }

            # # Ideal values (usually the values for the least polluted water)
            # ideal_values = {
            #     'p_CO3': 0, 'p_CL': 0, 'p_SO4': 0, 'p_TH': 0, 'p_CA': 0, 'p_MG': 0, 'p_NA': 0, 
            #     'pH': 7, 'TDS': 0
            # }

            # # Weights for the parameters
            # weights = {
            #     'p_CO3': 0.000016, 'p_CL': 0.000016, 'p_SO4': 0.000016, 'p_TH': 0.000004, 'p_CA': 0.000177778, 'p_MG': 0.001111111, 'p_NA': 0.000025, 
            #     'pH': 0.01384083, 'TDS': 0.000004 
            # }
            
            WAWQI = calculate_wqi(df.to_dict('records')[0], standard_values, ideal_values, weights)
            
            st.markdown(f'<div class="center-text">Weighted Arithmetic Water Quality Index (WAWQI): {WAWQI}</div>', unsafe_allow_html=True)

            # Insert the data into the database
            insert_data_to_db(df)
        except Exception as e:
            print(e)
            st.error(f"An Error has occurred during prediction{e}")
    
        

        # Option to download the results as a CSV file
        csv = df.to_csv(index=False).encode()
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='predicted_water_quality.csv',
            mime='text/csv',
        )

# Function to display the data analysis page
def data_analysis():
    st.markdown("""
<h1 style="text-align: center;">Visualize the Data</h1>
                <h1 style="text-align: center;">Tableau Dashboard Embedding</h2>
    """, unsafe_allow_html=True
    )

# Embed the HTML file that contains the Tableau dashboard and JavaScript API code
    html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>Tableau JavaScript API Example</title>
  <script type="text/javascript" src="https://public.tableau.com/javascripts/api/tableau-2.min.js"></script>
</head>
<body>
  <div id="vizContainer" style="width:100%; height:100%;"></div>
  <button onclick="filterDashboard()">Filter Dashboard</button>

  <script type="text/javascript">
    var viz;

    function initViz() {
      var containerDiv = document.getElementById("vizContainer");
      var url = "https://public.tableau.com/shared/3KZ8TKBQY?:display_count=n&:origin=viz_share_link"; // Replace with your Tableau dashboard URL
      var options = {
        width: '100%',
        height: '100%',
        hideTabs: true,
        onFirstInteractive: function () {
          console.log("Dashboard is interactive");
        }
      };
      viz = new tableau.Viz(containerDiv, url, options);
    }

    function filterDashboard() {
      const sheet = viz.getWorkbook().getActiveSheet();
      if (sheet.getSheetType() === 'dashboard') {
        const dashboard = sheet;
        const worksheet = dashboard.getWorksheets().get("YourSheetName"); // Replace with your sheet name
        worksheet.applyFilterAsync("YourFieldName", "YourFilterValue", tableau.FilterUpdateType.REPLACE); // Replace with your field name and filter value
      }
    }

    document.addEventListener("DOMContentLoaded", initViz);
  </script>
</body>
</html>
"""

# Use components.html to embed the HTML code
    st.components.v1.html(html_code, width=100, height=80)

# Optionally, add additional Streamlit components, like input forms
# ph = st.number_input('pH', value=7.0)
# ec = st.number_input('EC (µS/cm)', value=100.0)
# tds = st.number_input('Total Dissolved Solids (mg/L)', value=150.0)
# temperature = st.number_input('Temperature (°C)', value=20.0)

# Functionality to get predictions from an API could be added here
# if st.button('Get Predictions'):
#     predictions = get_predictions(ph, ec, tds, temperature)
#     st.write(predictions)



    # # Insert your Tableau dashboard URL here
    # tableau_url = "https://public.tableau.com/views/WaterQualityDashboard-FieldAgencies/Dashboard"

    # st.markdown(
    #     f"""
    #     <div class="iframe-container">
    #         <iframe src="{tableau_url}"></iframe>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    

# Function to display the about page
def about():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 50vh; flex-direction: column">
            <h2>"This application was developed to predict and analyze water quality parameters."</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 10vh;">
            <h1>Our Journey</h1>
        </div>
        """,
        unsafe_allow_html=True
    )   

# # Path to your local video file
    video_file = open('pitch.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)


def login():
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
            <h1>This is the LOGIN Page</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

#     # Firebase configuration details
#     firebaseConfig = {
#   "apiKey": "AIzaSyBTqd4oEyw9y-2FSsvaI1ryatmGJg4SFRo",
#   "authDomain": "final-project-b03d6.firebaseapp.com",
#   "projectId": "final-project-b03d6",
#   "storageBucket": "final-project-b03d6.appspot.com",
#   "messagingSenderId": "321009636869",
#   "appId": "1:321009636869:web:cf5630518155dfad03ae6c",
#   "measurementId": "G-YE9HMNWV0L"
# }

#     # Initialize Firebase
#     firebase = pyrebase.initialize_app(firebaseConfig)
#     auth = firebase.auth()
    
#     # Streamlit app
#     st.title("Streamlit with Firebase Authentication")
    
#     # Login Form
#     st.subheader("Login")
    
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     login = st.button("Login")
#     signup = st.button("Sign Up")
    
#     if login:
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             st.success("Login successful!")
#             st.write(f"Welcome {email}!")
#         except:
#             st.error("Invalid email or password")
    
#     if signup:
#         try:
#             user = auth.create_user_with_email_and_password(email, password)
#             st.success("Account created successfully!")
#         except:
#             st.error("Error creating account")
    
#     # Logout
#     if st.button("Logout"):
#         auth.current_user = None
#     st.success("Logged out successfully!")


if __name__ == "__main__":
    main()

