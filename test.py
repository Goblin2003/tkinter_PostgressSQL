from optparse import Values
from tkinter import *
import psycopg2
import tkinter.ttk as ttk
import csv
from tkinter import messagebox as mb
bol=("NOT NULL","NULL")
val =("serial","smallserial", "bigserial","smallint","integer","bigint","numeric","decimal","real","double precision","char","varchar","text","bytea","timestamp","date","time","time with time zone","interval","boolean")
### OPEN FILE WITCH INFO ABOUT CONNECTING BD###
with open('text.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
###############################################
#### CONNECT BD AND GET SHEME BD######
connection = psycopg2.connect(user="%s" %row[0],password="%s" %row[1],host="%s" %row[2],port="%s" %row[3],database="%s" %row[4])

cursor = connection.cursor()

ssql2 ="""select nspname from pg_namespace where nspowner = current_user::regrole;""" 
cursor.execute(ssql2)
sheme = cursor.fetchall()
print("========",sheme,"=========")
######################################


def callbackFunc1(event):
    pass
def two_window():
    enttipSheme = ent_tip_sh.get()
    
    def save_new_table():
        entSozdan = ent_sozdan.get()
        """connection = psycopg2.connect(user="%s" %row[0],
        password="%s" %row[1],
        host="%s" %row[2],
        port="%s" %row[3],
        database="%s" %row[4])"""
        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        if entSozdan != "":
            query = '''CREATE TABLE %s.%s(id Serial);; ''' % (enttipSheme,entSozdan)
            # Выполнение команды: это создает новую таблицу
            cursor.execute(query, (entSozdan))
            connection.commit()
        else:
            query1 = """SELECT table_name FROM information_schema.tables WHERE table_schema='%s'""" %enttipSheme
            
            
            #cursor.execute(query1)
            #obnov =cursor.fetchall()
            #print(obnov)
            #connection.commit()
        #connection.commit()
        print("Таблица успешно создана в PostgreSQL")
        connection.close()
    def create_pole_table():
        
        entNameTable = ent_name_table.get()
        entName = ent_name.get()
        entTip = ent_tip.get()
        entNull = ent_null.get()
        entOpis = ent_opis.get()
        entPsev = ent_psev.get()
        print(enttipSheme)
        print(entNameTable)

        conn = psycopg2.connect(user="%s" %row[0],password="%s" %row[1],host="%s" %row[2],port="%s" %row[3],database="%s" %row[4])
        cursor = conn.cursor()
        query ="""ALTER TABLE %s.%s ADD %s %s %s;""" %(enttipSheme,entNameTable, entName, entTip, entNull)
        query2 ="""%s [ AS ] "%s";""" %(entName, entPsev)
        query3 ="""COMMENT ON COLUMN %s.%s.%s IS '%s'; """ %(enttipSheme,entNameTable, entName, entOpis)
        cursor.execute(query,query2)
        cursor.execute(query3)
        print("succesfully data inserted")
        conn.commit()
        conn.close()
    def otpravka_v_BD(ent_dannie, ent_tip_sh):
    
        
        conn = psycopg2.connect(user="%s" %row[0],password="%s" %row[1],host="%s" %row[2],port="%s" %row[3],database="%s" %row[4])
        cursor = conn.cursor()
        tbl = "%s" % ent_dannie
        
        cursor.execute("""SET search_path TO %s;""" % ent_tip_sh)
        #query ="""SELECT * FROM %s.%s ORDER BY id DESC LIMIT 1;""" %(ent_tip_sh,ent_dannie)
        query ="""SELECT MAX(id) FROM %s.%s GROUP BY id;""" %(ent_tip_sh,ent_dannie)

        with open('dobav.csv') as d:
            cursor.copy_from(d, tbl, sep=",")
            print("succesfully data inserted")
            conn.commit()
            conn.close()


    def refresh():
        
        conn = psycopg2.connect(user="%s" %row[0],password="%s" %row[1],host="%s" %row[2],port="%s" %row[3],database="%s" %row[4])
        cursor = conn.cursor()
        tbl = "%s" % ent_dannie
        
        cursor.execute("""SET search_path TO %s;""" % ent_tip_sh.get())
        query ="""SELECT MAX(id) FROM %s.%s;""" %(ent_tip_sh.get(),combo.get())
        
        cursor.execute(query)
        query = cursor.fetchone()
        lbl2.config(text=str(f"Последний элемент: {query}"))

            
  
        
    
    window2 = Toplevel(window)
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='%s'" %enttipSheme

    cursor.execute(sql)
    tab = cursor.fetchall()
    print(tab)
    connection.commit()
    
    lbl = Label(window2, text = "Введите название таблици котороую хотите создать:")
    lbl.grid(column=0, row = 0)
    ent_sozdan = Entry(window2, width=10)
    ent_sozdan.grid(column=1, row= 0)
    

    lbl2 = Label(window2, text="Здесь будет последние значение ID")
    lbl2.grid(column=3, row =3)
    
    but= Button(window2, text="Создать!", command=save_new_table)
    but.grid(column=2,row=0)
    #название

    lbl_name = Label(window2, text="Название: ")
    lbl_name.grid(column=0,row=1)
    ent_name = Entry(window2, width=10)
    ent_name.grid(column=1, row= 1)

    #псевдоним
    lbl_psev = Label(window2, text="Псевдоним: " )
    lbl_psev.grid(column=0,row=2)
    ent_psev = Entry(window2, width=10)
    ent_psev.grid(column=1, row= 2)

    lbl_tip = Label(window2, text="Тип: " )
    lbl_tip.grid(column=0,row=3)
    ent_tip = ttk.Combobox(window2,values=val,width=10)
    ent_tip.bind("<<ComboboxSelected>>", callbackFunc1)
    ent_tip.grid(column=1, row= 3)

    lbl_opis = Label(window2, text="Описание поля: ")
    lbl_opis.grid(column=0,row=4)
    ent_opis = Entry(window2, width=10)

    ent_opis.grid(column=1, row= 4)
    lbl_name_table = Label(window2, text="Название таблицы: ")
    lbl_name_table.grid(column=0,row=5)

    ent_name_table = ttk.Combobox(window2, width=10)
    ent_name_table.bind("<<ComboboxSelected>>", callbackFunc1)
    ent_name_table.grid(column=1, row= 5)

    lbl_null = Label(window2, text="Not null: ")
    lbl_null.grid(column=0,row=6)
    ent_null = ttk.Combobox(window2,values=bol,width=10)
    ent_null.bind("<<ComboboxSelected>>", callbackFunc1)
    ent_null.grid(column=1, row= 6)

    but_dobav=Button(window2, text="Добавить!", command=create_pole_table)
    but_dobav.grid(column=0, row=7)

    

    dannie = Label(window2, text ="Выберети таблицу в которую хотите\n отправить данные")
    dannie.grid(column=0, row = 8,pady=(15, 0))
    ent_dannie = ttk.Combobox(window2, width=10)
    ent_dannie.bind("<<ComboboxSelected>>", callbackFunc1)
    ent_dannie.grid(column=1, row= 8)
    but_dobav_info=Button(window2, text="Отправить!", command=lambda:(otpravka_v_BD(ent_dannie.get(),ent_tip_sh.get())))
    but_dobav_info.grid(column=0, row=9)
    ent_dannie["values"] = tab
    ent_name_table["values"] = tab

    combo = ttk.Combobox(window2, width=10)
    combo.bind("<<ComboboxSelected>>", callbackFunc1)
    combo.grid(column=3, row= 4)
    combo["values"] = tab
    button = Button(window2, text="Обновить1", command=refresh)
    button.grid(column=3, row=5)
    
    

    

#def asd(ent_dannie,ent_name_table):
        #connection = psycopg2.connect(user="%s" %row[0],password="%s" %row[1],host="%s" %row[2],port="%s" %row[3],database="%s" %row[4])

        # Создайте курсор для выполнения операций с базой данных
        #cursor = connection.cursor()
        


window = Tk()
window.title("2практика")
lbl1 = Label(window, text = "Введите название схемы:")
lbl1.grid(column=0, row = 0)
ent_tip_sh = ttk.Combobox(window,values=sheme, width=10)
ent_tip_sh.bind("<<ComboboxSelected>>", callbackFunc1)
ent_tip_sh.grid(column=1, row= 0)

but_dobav1=Button(window, text="Обновить", command=two_window)
but_dobav1.grid(column=0, row=1, columnspan=2)
window.mainloop()
