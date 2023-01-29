import mysql
import mysql.connector.cursor as cursor

config = {
    'user': 'scott',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'employees',
    'raise_on_warnings': True
}


class MySQLconnect:

    def queryDB(self):
        cnx = mysql.connector.connect(**config)
        query = ("SELECT * FROM employees "
                 "WHERE Path = %s")
        path = ()
        cursor.execute(query, path)
        for (first_name, last_name, hire_date) in cursor:
            print("{}, {} was hired on {:%d %b %Y}".format(
                last_name, first_name, hire_date))
        cursor.close()
        cnx.close()


