#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
from sqlalchemy import text, create_engine
import urllib.parse

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('sales_data.csv')

# Handle missing values
df.dropna(inplace=True)

# Handle duplicates
df.drop_duplicates(inplace=True)

# Add a new column TotalValue that contains the total value of each order (Qty * Price)
df['TotalValue'] = df['Qty'] * df['Price']

# Convert OrderDate to datetime
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# Extract year and month from OrderDate and create a new column YearMonth (format: YYYY-MM)
df['YearMonth'] = df['OrderDate'].dt.strftime('%Y-%m')

# Create summary report and its columns 
summary_report = df.groupby(['ProductID', 'YearMonth'])['TotalValue'].sum().reset_index()
summary_report.columns = ['ProductID', 'YearMonth', 'TotalSales']

# Print summary report
print(summary_report.head())

username = 'root'
password = 'Root@12345'
host = '127.0.0.1'
port = 3306
database = 'SalesDB'

# URL-encode the password
encoded_password = urllib.parse.quote_plus(password)

# Modified connection string
connection_string = f'mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}'

# Create an engine instance
try:
    engine = create_engine(connection_string)
    print("Database connection successful.")
    
    with engine.connect() as connection:
        # Check if the column exists
        check_column = text("""
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = :database
          AND TABLE_NAME = 'sales'
          AND COLUMN_NAME = 'YearMonth'
        """)
        
        result = connection.execute(check_column, {"database": database})
        column_exists = result.scalar()

        if not column_exists:
            # Add the YearMonth column
            add_column = text("ALTER TABLE sales ADD COLUMN YearMonth VARCHAR(7)")
            connection.execute(add_column)
            print("YearMonth column added successfully.")
        else:
            print("YearMonth column already exists.")

    # Insert the DataFrame into the MySQL table
    df.to_sql('sales', con=engine, if_exists='append', index=False)
    print("Data inserted into MySQL table successfully!")

except Exception as e:
    print(f"Error: {e}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




