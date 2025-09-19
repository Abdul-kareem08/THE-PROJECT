import psycopg, sys
try:
    conn = psycopg.connect("dbname=bruno_db user=postgres host=127.0.0.1 password=kim port=5432")
    conn.close()
    print("PG OK")
except Exception as e:
    print("PG ERR:", e)
    sys.exit(1)