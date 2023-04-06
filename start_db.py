import psycopg2
import os
try:
    credenciales = {
        "dbname": "rifasdb",
        "user": "rifasuser",
        "password": "f4^BULw08Q03",
        "host": "localhost",
        "port": 5432
    }
    conexion = psycopg2.connect(**credenciales)
    with conexion.cursor() as cursor:        
        with open('estados.txt') as archivo:
            for linea in archivo:
                cursor.execute("INSERT INTO rifa_mxestados(nombre) VALUES('"+linea.rstrip('\n')+"')")
        conexion.commit()
except psycopg2.Error as e:
    print("Ocurrió un error al conectar a PostgreSQL: ", e)
finally:
    conexion.close()
