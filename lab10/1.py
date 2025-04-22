import psycopg2 

con = psycopg2.connect(
    dbname='phonebook',  
    user='postgres',  
    password='postgres',  
    host='localhost',  
    port='5432' 
)

cur = con.cursor()  

cur.execute('CREATE TABLE IF NOT EXISTS phone_book('
            'id SERIAL PRIMARY KEY,'  
            'name VARCHAR(256),'
            'phone VARCHAR(256)'  
            ');'
)

con.commit()  #потверждение изменений в базе

#добавление нового контакта
def insert(name, phone):
    cur.execute(
        'INSERT INTO phonebook(name, phone) VALUES (%s, %s)', (name, phone)  
    )
    con.commit() 

#для обновления данных в таблице по ID
def update(id, name, phone):
    cur.execute(
        'UPDATE phonebook SET name=%s, phone=%s WHERE id=%s', (name, phone, id)  
    )
    con.commit()  

#для получения записи по ID
def getById(id):
    cur.execute(
        'SELECT * FROM phonebook WHERE id=%s', (id,) 
    ) 
    return cur.fetchone()  

#для получения всех записей
def getAll(asc=True):
    sortDir = 'ASC'  #сортировка по возрастанию
    if not asc:
        sortDir = 'DESC'  #сортировка по убыванию

    cur.execute(
        'SELECT * FROM phonebook ORDER BY id ' + sortDir  
    )
    return cur.fetchall()  

#для получения записи по имени
def getByName(name):
    cur.execute(
        "SELECT * FROM phonebook WHERE name=%s", (name,) 
    )
    return cur.fetchall()  

#для удаления записи по имени или телефону
def delete(value):
    cur.execute(
        'DELETE FROM phonebook WHERE name=%s OR phone=%s', (value, value)  
    )
    con.commit()  


#для добавления нового контакта
def insertFromConsole():
    name = input("Enter name: ")  
    phone = input("Enter phone number: ")  
    insert(name, phone)  
    print('New phone added to phone book!')  

#для обновления
def updateFromConsole():
    id = input("Enter id of row: ")  
    row = getById(id)  
    if row is None:
        print('No such phone row')  
        return

    name = input("Enter name: ")  
    if name == '':
        name = row[1]  

    phone = input("Enter phone number: ")  
    if phone == '':
        phone = row[2]  
    update(id, name, phone)  
    print('Row updated successfully!')  
#отображение
def printPhoneBook():
    user_input = int(input("Enter sorting direction (1-ASC,2-DESC): "))  #направление сортировки
    phone_book = None
    if user_input == 2:
        phone_book = getAll(asc=False)  #по убыванию
    else:
        phone_book = getAll()  #по возрастанию

    for row in phone_book:
        print(f'ID: {row[0]}, Name: {row[1]}, Phone number: {row[2]}')  

#для поиска контакта по имени
def searchByName():
    name = input("Enter name to search: ")  
    result = getByName(name)  
    if result:
        for row in result:
            print(f'ID: {row[0]}, Name: {row[1]}, Phone number: {row[2]}')  
    else:
        print("Not found.") 

#для удаления записи по имени
def deleteByName():
    name = input("Enter name to delete: ")  
    delete(name)  
    print(f'Name {name} and corresponding phone number deleted.')  

#для сортировки записей по имени
def sortByName():
    print("Sorting by name...")
    result = getAll(asc=True)  #в порядке возрастания
    for row in result:
        print(f'ID: {row[0]}, Name: {row[1]}, Phone number: {row[2]}')  

run = True

while run:
    input("phonebook menu--->")
    user_input = int(input("choose option:\n 1 - insert by console\n 2 - update from console\n 3 - search by name\n 4 - delete by name\n 5 - sort by name\n 6 - show full phone book\n 0 - close program\n"))
    
    # Выбираем действия в зависимости от ввода пользователя
    if user_input == 1:
        insertFromConsole()  #добавление
    elif user_input == 2:
        updateFromConsole()  #обновление
    elif user_input == 3:
        searchByName()  #поиск по имени
    elif user_input == 4:
        deleteByName()  #удаление по имени
    elif user_input == 5:
        sortByName()  #сортировка по имени
    elif user_input == 6:
        printPhoneBook()  #печать
    elif user_input == 0:
        input("goodbye!")  #выход
        run = False
    else:
        print("oops,invalid option.try again!")  

con.close()