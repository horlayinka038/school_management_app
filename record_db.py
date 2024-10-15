import psycopg2
from decouple import config


connect_db = {
    'dbname': config('DB_NAME'),
    'user': config('DB_USER'),
    'host': config('DB_HOST'),
    'password': config('DB_PASSWORD'),
    'port': config('DB_PORT')
}
def connect():
    try:
        conn = psycopg2.connect(**connect_db)
        cursor = conn.cursor()
        
        create_table = (
            """
            CREATE TABLE IF NOT EXISTS student (
            id SERIAL PRIMARY KEY,
            surname VARCHAR(100),
            other_names VARCHAR(100),
            password VARCHAR(100),
            gender VARCHAR(10),
            email VARCHAR(100),
            phone_number VARCHAR(11),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS exam_records(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            gender VARCHAR(10),
            matrix_number VARCHAR(10) UNIQUE,
            math_score NUMERIC(3),
            phy_score NUMERIC(3),
            chm_score NUMERIC(3),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(create_table)
        conn.commit()
        print("Table created successfully")
        return conn
    except psycopg2.Error as e:
        conn.rollback()
        print(e)
        return None
    # finally:
    #     if conn:
    #         conn.close()
    #     if cursor:
    #         cursor.close()
    
connect ()    
