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


    def change_client_data(self, client_id, first_name="", last_name="", email="", phone=""):
        if first_name:
            self.cursor.execute("""
                UPDATE Client
                SET first_name = %s
                WHERE id = %s
            """, (first_name, client_id))

        if last_name:
            self.cursor.execute("""
                UPDATE Client
                SET last_name = %s
                WHERE id = %s
            """, (last_name, client_id))

        if email:
            self.cursor.execute("""
                UPDATE Client
                SET email = %s
                WHERE id = %s
            """, (email, client_id))

        if phone:
            if last_name:
                self.cursor.execute("""
                    UPDATE ClientPhones
                    SET phone_number = %s
                    WHERE client_id = %s
                """, (phone, client_id))


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


    def find_client(self, first_name=None, last_name=None, email=None, phone=None):
        client = []
        client_phones = []

        if first_name and last_name and email:
            cursor.execute("""
                SELECT * FROM Client
                WHERE first_name = %s AND last_name = %s AND email = %s
            """, (first_name, last_name, email))

            client = cursor.fetchone()

        if first_name and last_name and not email:
            cursor.execute("""
                            SELECT * FROM Client
                            WHERE first_name = %s AND last_name = %s
                        """, (first_name, last_name))

            client = cursor.fetchone()

        if first_name and not last_name and email:
            cursor.execute("""
                            SELECT * FROM Client
                            WHERE first_name = %s AND email = %s
                        """, (first_name, email))

            client = cursor.fetchone()

        if first_name and not last_name and not email:
            cursor.execute("""
                            SELECT * FROM Client
                            WHERE first_name = %s
                        """, (first_name,))

            client = cursor.fetchone()

        if not first_name and last_name and email:
            cursor.execute("""
                            SELECT * FROM Client
                            WHERE last_name = %s AND email = %s
                        """, (last_name, email))

            client = cursor.fetchone()

        if not first_name and last_name and not email:
            cursor.execute("""
                            SELECT * FROM Client
                            WHERE last_name = %s
                        """, (last_name,))

            client = cursor.fetchone()

        if not first_name and not last_name and email:
            cursor.execute("""
                            SELECT * FROM Client
                            WHERE email = %s
                        """, (email,))

            client = cursor.fetchone()

        if phone and client:
            cursor.execute("""
                SELECT * FROM ClientPhones
                WHERE phone_number = %s AND client_id = %s
            """, (phone, client[0]))

            client = cursor.fetchone()

        if phone:
            cursor.execute("""
                SELECT * FROM ClientPhones
                WHERE phone_number = %s
            """, (phone,))

            client = cursor.fetchone()

        if len(client) == 3:
            cursor.execute("""
                SELECT Client.id, first_name, last_name, email, phone_number FROM Client
                JOIN ClientPhones ON client_id = %s
            """, (client[1],))

            client = cursor.fetchone()
        elif len(client) == 4:
            cursor.execute("""
                SELECT phone_number FROM ClientPhones
                WHERE client_id = %s
            """, (client[0],))

            fetch = cursor.fetchall()

            if fetch != None:
                client_phones = [i for i in fetch]

        if client:
            print("Данные клиента: ")
            print(f"ID:{client[0]}")
            print(f"Имя:{client[1]}")
            print(f"Фамилия:{client[2]}")
            print(f"Email:{client[3]}")

            print("Телефоны:")
            if client_phones:
                for i in client_phones:
                    print(i[0])
            else:
                print("Нет телефонов")
        else:
            print("Клиент не найден")



if __name__ == '__main__':
    conn = psycopg2.connect(database="netology_db", user="postgres", password="123456")

    with psycopg2.connect(database="netology_db", user="postgres", password="123456") as conn:
        with conn.cursor() as cursor:
            db = DBmanager(cursor)

            #Создадим таблицы
            db.create_tables()

            # Создадим 4 клиентов
            db.add_new_client("Вячеслав", "Бородин", "v321412@mail.ru", "89193332211")
            db.add_new_client("Иван", "Иванов", "ivanov@gmail.com", "89992224455")
            db.add_new_client("Петр", "Петров", "petrov22@mail.ru", "89113234467")
            db.add_new_client("Дмитрий", "Дмитриев", "dmitry@mail.ru")

            # Выбираем клиента с айди = 4
            client_id = 4

            # Добавляем выбранному клиенту номер телефона
            db.add_phone_number_to_client(client_id, "89003444421")
            db.add_phone_number_to_client(client_id, "89003421421")
            db.add_phone_number_to_client(client_id, "89003455421")

            # Выбираем клиента с айди = 3
            client_id = 3

            # Изменяем данные клиента
            db.change_client_data(client_id, first_name="Григорий", phone='89193233489')

            # Выбираем клиента с айди = 1
            client_id = 1

            # Удалим номер телефона для выбранного клиента
            db.delete_client_phone(client_id, "89193332211")

            # Выбираем клиента с айди = 2
            client_id = 2

            # Удалим клиента
            db.delete_client(client_id)

            #Поиск клиента
            db.find_client(phone="89113234467")
            db.find_client(first_name="Дмитрий", email="dmitry@mail.ru")
            db.find_client(last_name="Петров")

