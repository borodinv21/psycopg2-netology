import psycopg2


class DBmanager:

    def __init__(self, cursor):
        self.cursor = cursor

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE Client (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(64),
                last_name VARCHAR(64),
                email VARCHAR(128) UNIQUE  
            );
        """)

        self.cursor.execute("""
                CREATE TABLE ClientPhones(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES Client(id),
                    phone_number VARCHAR(12) UNIQUE NULL
                );
            """)


    def add_new_client(self, first_name, last_name, email, phone_number=""):
        self.cursor.execute("""
            INSERT INTO Client (first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email))

        client_id = self.cursor.fetchone()

        if phone_number:
            self.cursor.execute("""
                INSERT INTO ClientPhones(client_id, phone_number)
                VALUES (%s, %s)
            """, (client_id, phone_number))


    def add_phone_number_to_client(self, client_id, phone_number):
        self.cursor.execute("""
            INSERT INTO ClientPhones(client_id, phone_number)
            VALUES (%s, %s);
        """, (client_id, phone_number))


    def change_client_data(self, client_id):
        print("Изменение данных клиента")
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        email = input("Введите Email: ")

        self.cursor.execute("""
            UPDATE Client
            SET first_name = %s, last_name = %s, email = %s
            WHERE id = %s
        """, (first_name, last_name, email, client_id))


    def delete_client_phone(self, client_id, phone_number):
        self.cursor.execute("""
            DELETE FROM ClientPhones WHERE client_id = %s AND phone_number = %s
        """, (client_id, phone_number))


    def delete_client(self, client_id):
        self.cursor.execute("""
                DELETE FROM ClientPhones WHERE client_id = %s
            """, (client_id,))

        self.cursor.execute("""
            DELETE FROM Client WHERE id = %s
        """, (client_id,))


    def find_client(self):
        client_data = input("Введите любые данные о клиенте: ")

        self.cursor.execute("""
            SELECT * FROM Client
            WHERE first_name = %s OR last_name = %s OR email = %s
        """, (client_data, client_data, client_data))

        client = self.cursor.fetchone()

        if client == None:
            self.cursor.execute("""
                SELECT client_id FROM ClientPhones
                WHERE phone_number = %s
            """, (client_data, ))

            client_id = self.cursor.fetchone()

            if client_id != None:
                self.cursor.execute("""
                    SELECT * FROM Client
                    WHERE id = %s
                """, (client_id[0], ))

                client = self.cursor.fetchone()

        return client


conn = psycopg2.connect(database="netology_db", user="postgres", password="123456")

with conn.cursor() as cursor:
    db = DBmanager(cursor)

    #Создадим таблицы
    db.create_tables()

    #Создадим 4 клиентов
    db.add_new_client("Вячеслав", "Бородин", "v321412@mail.ru", "89193332211")
    db.add_new_client("Иван", "Иванов", "ivanov@gmail.com", "89992224455")
    db.add_new_client("Петр", "Петров", "petrov22@mail.ru", "89113234467")
    db.add_new_client("Дмитрий", "Дмитриев", "dmitry@mail.ru")

    #Выбираем клиента с айди = 4
    client_id = 4

    #Добавляем выбранному клиенту номер телефона
    db.add_phone_number_to_client(client_id, "89003405421")

    #Выбираем клиента с айди = 3
    client_id = 3

    #Изменяем данные клиента
    db.change_client_data(client_id)

    #Выбираем клиента с айди = 1
    client_id = 1

    #Удалим номер телефона для выбранного клиента
    db.delete_client_phone(client_id, "89193332211")

    #Выбираем клиента с айди = 2
    client_id = 2

    #Удалим клиента
    db.delete_client(client_id)

    #Поиск клиента
    print(db.find_client())

    conn.commit()

conn.close()
