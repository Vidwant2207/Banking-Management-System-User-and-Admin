import sqlite3

def generate():
    conn_obj=sqlite3.connect("bank.sqlite")

    curs_obj=conn_obj.cursor()
    query='''create table if not exists accounts(
        acn_acno integer  primary key autoincrement,
        acn_name text,
        acn_pass text,
        acn_email text,
        acn_mob text,
        acn_adhar text,
        acn_dob text,
        acn_bal float,
        acn_od text)
    '''
    curs_obj.execute(query)
    curs_obj.close()

