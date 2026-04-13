import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123456",
        host="127.0.0.1",
        port=5432
    )
    return conn

def inform_add(conn):
    cur = conn.cursor()
    name = input("Enter a name: ")
    phone = input("Enter a phone: ")
    cur.execute(
        "INSERT INTO book(name,phone) VALUES(%s, %s);",
        (name, phone)
    )
    conn.commit()
    print("Information added!")
    cur.close()

def inform_update(conn):
    cur = conn.cursor()
    person_to_update = input("Enter a person:")
    print("Information for update:")
    print("1 - Name")
    print("2 - Phone")
    choice = input("Choose information to update:")
    if choice == "1":
        new_name = input("Enter new name:")
        cur.execute(
            "UPDATE book SET name = %s WHERE name = %s;",
            (new_name, person_to_update)
        )
    elif choice == "2":
        new_phone = input("Enter new phone:")
        cur.execute(
            "UPDATE book SET phone = %s WHERE name = %s;",
            (new_phone, person_to_update)
        )
    else:
        print("Choose from given variants!")
        cur.close()
        return
    conn.commit()
    if cur.rowcount == 0:
        print("Error for name!")
    else:
        print("Information updated!")
    cur.close()

def inform_delete(conn):
    cur = conn.cursor()
    person_to_delete = input("Enter a person:")
    cur.execute(
        "DELETE FROM book WHERE name = %s",
        (person_to_delete,)
    )
    conn.commit()
    if cur.rowcount == 0:
        print("Error for name!")
    else:
        print("Information deleted!")
    cur.close()

def inform_search(conn):
    cur = conn.cursor()
    print("Search by:")
    print("1 - Name")
    print("2 - ID")
    print("3 - Phone")
    choice = input("Choose: ")
    if choice == "1":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM book WHERE name = %s;", (name,))
    elif choice == "2":
        id_val = input("Enter id: ")
        cur.execute("SELECT * FROM book WHERE id = %s;", (id_val,))
    elif choice == "3":
        phone = input("Enter phone: ")
        cur.execute("SELECT * FROM book WHERE phone = %s;", (phone,))
    else:
        print("Invalid choice!")
        cur.close()
        return
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No results found!")

    cur.close()

def inform_pagination(conn):
    cur = conn.cursor()
    limit = int(input("Enter LIMIT: "))
    offset = int(input("Enter OFFSET: "))
    cur.execute(
        "SELECT * FROM book ORDER BY id LIMIT %s OFFSET %s;",
        (limit, offset)
    )
    rows = cur.fetchall()
    print("Paginated results:")
    for row in rows:
        print(row)
    cur.close()

def inform_bulk(conn):
    cur = conn.cursor()
    names = input("Enter full names (use ';' between people): ").split(";")
    phones = input("Enter phones (use ';' between numbers): ").split(";")
    for i in range(len(names)):
        name = names[i].strip()   
        phone = phones[i].strip()
        cur.execute(
            "INSERT INTO book(name, phone) VALUES (%s, %s);",
            (name, phone)
        )
    conn.commit()
    print("Bulk insert completed!")
    cur.close()

def inform_show(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM book ORDER BY id;")
    rows = cur.fetchall()
    print("All information:")
    for row in rows:
        print(row)
    cur.close()


conn = connect_db()

while True:
    print("\n--- MENU ---")
    print("1 - Add information")
    print("2 - Update information")
    print("3 - Delete information")
    print("4 - Show all contacts")
    print("5 - Search information")
    print("6 - Pagination")
    print("7 - Bulk insert")
    print("0 - EXIT")

    choice = input("Choose a function:")

    if choice == "1":
        inform_add(conn)
    elif choice == "2":
        inform_update(conn)
    elif choice == "3":
        inform_delete(conn)
    elif choice == "4":
        inform_show(conn)
    elif choice == "5":
        inform_search(conn)
    elif choice == "6":
        inform_pagination(conn)
    elif choice == "7":
        inform_bulk(conn)
    elif choice == "0":
        print("Thank you for using Phonebook")
        break
    else:
        print("Choose from given variants!")

conn.close()