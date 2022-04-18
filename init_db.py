import sqlite3

banco = sqlite3.connect('database.sqlite')

cursor = banco.cursor()

cursor.execute("CREATE TABLE Cadastros (id integer not null primary key, nome varchar (100), bairro varchar (100), cidade varchar (100), email varchar (100))")
 

banco.commit()