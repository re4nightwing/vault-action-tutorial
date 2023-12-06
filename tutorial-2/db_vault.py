import hvac
import mysql.connector

VAULT_ADDR = 'http://127.0.0.1:8200'
VAULT_TOKEN = 'root'
DB_ROLE = 'myrole'

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)


def get_database_credentials():
    response = client.secrets.database.generate_credentials(name=DB_ROLE)
    return response.get('data', {})

def connect_to_database(credentials):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user=credentials.get('username'),
        password=credentials.get('password'),
        database='vault_test'
    )
    return connection

if __name__ == '__main__':
    credentials = get_database_credentials()
    print(credentials)
    connection = connect_to_database(credentials)
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

    # Close the database connection
    connection.close()