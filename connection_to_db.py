import psycopg2
username = 'vnas_quantri'
password = 'asdad!my_4_vnas_678'
hostname = '171.244.51.228'
port = 8182
db_name = 'phon_company_infor'


def get_pg_connection():
    return psycopg2.connect(user=username, password=password, host=hostname, port=port, database=db_name)


def execute_query(count_query) -> int:
    """
        Thực thi một câu lệnh count query -> trả về một số
    """
    try:
        connection = get_pg_connection()
        cursor = connection.cursor()
        cursor.execute(count_query)
        # rows = cursor.fetchall()
        # print(rows[0][0])
        # return rows[0][0] if rows else None
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        print("execute_count_query error 🐶🐶🐶🐶🐶", error)
        connection.rollback()
        cursor.close()
        connection.close()
        return error
