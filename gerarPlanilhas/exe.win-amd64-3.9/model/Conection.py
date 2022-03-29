
# Gerador de planilhas
#
# By: Victor Vasconcelos
#
import psycopg2
db_name = '*******'
db_host = '*******'
db_user = 'postgres'
db_password = '********'
connect = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
cursor = connect.cursor()

def query(sql):
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        connect.commit()
        return result
    except Exception as e:
        print(e)
        cursor.rollback()
        connect.rollback()

def commit(sql):
    print(sql)
    try:
        cursor.execute(sql)
        connect.commit()
        print('comitou')

    except Exception as e:
        print(e)
        cursor.rollback()
        connect.rollback()



