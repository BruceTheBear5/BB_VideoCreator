import psycopg2
try:
    connection = psycopg2.connect("postgresql://bond:hkJBMZZaRBmmcaGiKDM8rg@project-8970.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/project?sslmode=require")
    print("Connection successful")
    connection.close()
except Exception as e:
    print("Failed to connect to the database:", e)
