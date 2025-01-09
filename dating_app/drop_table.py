import psycopg2
from psycopg2 import sql


DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
DB_USER='postgres.yjjqgijsrvbuhwxqsuoe'
DB_PASSWORD='zdVZz4Ir0UoAha0U'
DB_HOST='aws-0-eu-central-1.pooler.supabase.com'
DB_PORT='6543'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = True
cursor = conn.cursor()

# SQL command to drop all tables
drop_tables_sql = """
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
"""

# Execute the SQL command
cursor.execute(drop_tables_sql)

# Close the cursor and connection
cursor.close()
conn.close()

print("All tables have been dropped.")
