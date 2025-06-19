import pandas as pd
import psycopg2
from datetime import datetime
from sqlalchemy import create_engine
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from elasticsearch import Elasticsearch

default_args = {
    'owner': 'Farhan',
    'start_date': datetime(2025, 6, 1)
}

with DAG(
    dag_id='Finpro', 
    description='from csv to postgres',
    schedule_interval='*/10 * 9 * 6',
    default_args=default_args,
    catchup=False
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    @task()
    def Create_table():
        # load data (create connection to postgresql)
        
        # '''
        # change DB_NAME, PG_USER, PG_PASSWORD, PG_HOST and PG_PORT
        # to your own configuration
        # '''
        pgConn = psycopg2.connect(
        database = 'airflow',
        user = 'airflow',
        password = 'airflow',
        host = 'postgres',
        port="5432"

        )

        # create cursor
        cur = pgConn.cursor()

        # create table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS finpro_amazon(
                    index INTEGER, 
                    "Order ID" TEXT,
                    "Date" TEXT,
                    "Status" TEXT,
                    "Fulfilment" TEXT,
                    "Sales Channel " TEXT,
                    "ship-service-level" TEXT,
                    "Style" TEXT,
                    "SKU" TEXT,
                    "Category" TEXT,
                    "Size" TEXT,
                    "ASIN" TEXT,
                    "Courier Status" TEXT,
                    "Qty" INTEGER,
                    "currency" TEXT,
                    "Amount" NUMERIC(10, 2),
                    "ship-city" TEXT,
                    "ship-state" TEXT,
                    "ship-postal-code" TEXT,
                    "ship-country" TEXT,
                    "promotion-ids" TEXT,
                    "B2B" TEXT,
                    "fulfilled-by" TEXT,
                    "Unnamed: 22" TEXT

                
            ); 

            """         
        )

        df = pd.read_csv('/opt/airflow/data/Amazon Sale Report.csv', index_col=False)

        # insert data to table (ini masih proses loading data ke dalam data warehouse)
        for row in df.to_dict(orient='records'):
            cur.execute(
                "INSERT INTO finpro_amazon VALUES (%s, %s, %s, %s,%s, %s, %s , %s, %s,%s, %s, %s , %s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s, %s)", # %s is for placeholder of your value
                (row['index'], row['Order ID'], row['Date'], row['Status'], row['Fulfilment'], row['Sales Channel '],row['ship-service-level'], 
                 row['Style'], row['SKU'], row['Category'], row['Size'], row['ASIN'], row['Courier Status'], row['Qty'], row['currency'], 
                 row['Amount'], row['ship-city'], row['ship-state'], row['ship-postal-code'], row['ship-country'], row['promotion-ids'], 
                 row['B2B'], row['fulfilled-by'], row['Unnamed: 22'])
            )

        # commit and close connection
        pgConn.commit() # harus commit klo misalnya pake psycho pg2
        pgConn.close()

    @task()
    def extract():
        database = 'airflow'
        username = 'airflow'
        password = 'airflow'
        host = 'postgres'

        postgres_url = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'

        engine = create_engine(postgres_url)
        conn = engine.connect()

        df = pd.read_sql('select * from finpro_amazon', conn)
        df.to_csv(
            '/opt/airflow/data/amazon_sample_finpro.csv', index=False)
        print('Success extract to airflow')

    @task()
    def preprocessing():
        '''
        Function used to transform data
        '''
        df = pd.read_csv('/opt/airflow/data/amazon_sample_finpro.csv')

        # drop kolom yang tidak perlu
        df.drop(columns='index', inplace=True)
        df.drop(columns='Unnamed: 22', inplace=True)

        # Adjust nama kolom
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ','_')
        df.columns = df.columns.str.replace('-','_')
        df.columns = df.columns.str.lower()
        df.rename(columns={'amount':'sales', 'asin':'amazon_standard_id'}, inplace=True)

        # ubah format waktu
        df['date'] = pd.to_datetime(df['date'],format='%m-%d-%y')

        # ubah 
        df['ship_postal_code'] = df['ship_postal_code'].astype('Int64')

        # Remove Duplicates (tidak ada)
        df.drop_duplicates(inplace=True)

        # maaping nama state terbaru
        state_mapping = {
            'andaman & nicobar': 'Andaman & Nicobar',
            'andhra pradesh': 'Andhra Pradesh',
            'arunachal pradesh': 'Arunachal Pradesh',
            'ar': 'Arunachal Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chandigarh': 'Chandigarh',
            'chhattisgarh': 'Chhattisgarh',
            'dadra and nagar': 'Dadra and Nagar Haveli',
            'delhi': 'Delhi',
            'new delhi': 'Delhi',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal pradesh': 'Himachal Pradesh',
            'jammu & kashmir': 'Jammu & Kashmir',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'ladakh': 'Ladakh',
            'lakshadweep': 'Lakshadweep',
            'madhya pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'nl': 'Nagaland',
            'odisha': 'Odisha',
            'orissa': 'Odisha',
            'pb': 'Punjab',
            'punjab': 'Punjab',
            'punjab/mohali/zirakpur': 'Punjab',
            'puducherry': 'Puducherry',
            'pondicherry': 'Puducherry',
            'rajasthan': 'Rajasthan',
            'rajshthan': 'Rajasthan',
            'rajsthan': 'Rajasthan',
            'rj': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil nadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar pradesh': 'Uttar Pradesh',
            'uttarakhand': 'Uttarakhand',
            'west bengal': 'West Bengal',
            'apo': 'APO (Unknown)'
        }

        # Fungsi normalisasi
        def clean_state(state):
            if pd.isna(state):
                return 'UNKNOWN'
            state = state.strip().lower()
            return state_mapping.get(state, f'UNKNOWN ({state})')

        # Membuat kolom baru dengan nama yang sudah dibersihkan
        df['clean_ship_state'] = df['ship_state'].apply(clean_state)

        # Filter data
        df = df[df['status'] == 'Shipped']

        # Drop kolom yang tidak perlu
        df.drop(columns=['ship_city', 'ship_postal_code', 'fulfilled_by', 'style', 'sku', 'ship_country', 'order_id', 'courier_status', 'b2b', 'ship_state'], inplace=True)

        # Filter data
        df = df[df['clean_ship_state'] != 'UNKNOWN']

        # Fungsi normalisasi promotion ID agar menjadi boolean
        def clean_prom(prom):
            if pd.isna(prom):
                return False
            prom = prom.strip().lower()
            return True

        # Membuat kolom baru dengan nama yang sudah dibersihkan
        df['promotion_used'] = df['promotion_ids'].apply(clean_prom)

        df = df.drop(columns='promotion_ids')

        # Handling missing value
        df['currency'] = df['currency'].fillna(value='INR')

        lookup_sales = df[df['sales'] > 0].groupby(['category', 'size', 'qty'])['sales'].first().reset_index()
        lookup_sales.rename(columns={'sales': 'lookup_sales'}, inplace=True)

        # Step 2: Merge into the data
        df = df.merge(lookup_sales, on=['category', 'size', 'qty'], how='left')

        # Step 3: Imputation
        df['sales'] = df.apply(
            lambda row: row['lookup_sales'] if row['sales'] == 0 and pd.notnull(row['lookup_sales']) else row['sales'],
            axis=1
        )

        # Step 4: Drop dummy column
        df = df.drop(columns='lookup_sales')

        qty_error = df[(df['qty']==0 )]

        df = df.drop(qty_error.index)

        print('Preprocessed data is success')
        print(df.head())
        df.to_csv(
            '/opt/airflow/data/data_for_modelling.csv', index=False)
        

    @task
    def loading():

        pgConn = psycopg2.connect(
        database = 'airflow',
        user = 'airflow',
        password = 'airflow',
        host = 'postgres',
        port="5432"

        )

        # create cursor
        cur = pgConn.cursor()

        # create table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS finpro_amazon_cleaned(
                    date DATE, 
                    status TEXT,
                    fulfilment TEXT,
                    sales_channel TEXT,
                    ship_service_level TEXT,
                    category TEXT,
                    size TEXT,
                    amazon_standard_id TEXT,
                    qty INTEGER,
                    currency TEXT,
                    sales FLOAT,
                    clean_ship_state TEXT,
                    promotion_used BOOLEAN
            ); 

            """         
        )

        df = pd.read_csv('/opt/airflow/data/data_for_modelling.csv', index_col=False)

        # insert data to table (ini masih proses loading data ke dalam data warehouse)
        for row in df.to_dict(orient='records'):
            cur.execute(
                "INSERT INTO finpro_amazon_cleaned VALUES (%s, %s, %s, %s,%s, %s, %s , %s, %s,%s, %s, %s , %s)", # %s is for placeholder of your value
                (row['date'], row['status'], row['fulfilment'], row['sales_channel'], row['ship_service_level'], row['category'],row['size'], 
                 row['amazon_standard_id'], row['qty'], row['currency'], row['sales'], row['clean_ship_state'], row['promotion_used'])
            )

        # commit and close connection
        pgConn.commit() # harus commit klo misalnya pake psycho pg2
        pgConn.close()

    # definisikan flownya
    start >> Create_table() >> extract() >> preprocessing() >> loading() >> end
