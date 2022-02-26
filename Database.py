import psycopg2

con = psycopg2.connect(host="", database="", user="", password="")


def add_diamond(chat_id, user_id, num):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.publicbet_diamonds SET diamond=diamond + %(num)s WHERE chat_id=%(chat_id)s AND user_id=%(user_id)s;
    INSERT INTO ali_ag_db.publicbet_diamonds (chat_id,user_id, diamond)
       SELECT %(chat_id)s,%(user_id)s , %(num)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.publicbet_diamonds WHERE chat_id=%(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id), 'user_id': int(user_id), 'num': int(num)})
    con.commit()
    cur.close()


def getactivegaps():
    cur = con.cursor()
    cur.execute("SELECT groupid FROM ali_ag_db.activegps")
    return cur.fetchall()


def activegap(chat_id):
    chat_id = int(chat_id)
    cur = con.cursor()
    cur.execute(f"SELECT groupid FROM ali_ag_db.activegps WHERE groupid = {chat_id}")
    isthere = len(cur.fetchall())
    con.commit()
    cur.close()
    if isthere == 0:
        cur = con.cursor()
        cur.execute(f"INSERT INTO ali_ag_db.activegps VALUES ({chat_id})")
        con.commit()
        cur.close()
        return "Group added to database seccesfully🟢"
    else:
        return "Group has been activated before!"


def deactivegap(chat_id):
    chat_id = int(chat_id)
    cur = con.cursor()
    cur.execute(f"SELECT groupid FROM ali_ag_db.activegps WHERE groupid = {chat_id}")
    isthere = len(cur.fetchall())
    con.commit()
    cur.close()
    if isthere != 0:
        cur = con.cursor()
        cur.execute(f"DELETE FROM ali_ag_db.activegps WHERE groupid = {chat_id}")
        con.commit()
        cur.close()
        return "Group remove from database seccesfully🔴"
    else:
        return "Group isn\'t active!"


def isactive(chat_id):
    chat_id = int(chat_id)
    cur = con.cursor()
    cur.execute(f"SELECT groupid FROM ali_ag_db.activegps WHERE groupid = {chat_id}")
    isthere = len(cur.fetchall())
    con.commit()
    cur.close()
    if isthere == 0:
        return False
    else:
        return True


def set_creator(chat_id, user_id):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.publicbet_admin SET creator = TRUE WHERE chat_id=%(chat_id)s AND user_id=%(user_id)s;
    INSERT INTO ali_ag_db.publicbet_admin (chat_id,user_id, creator)
       SELECT %(chat_id)s,%(user_id)s , TRUE 
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.publicbet_admin WHERE chat_id=%(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def rem_creator(chat_id, user_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.publicbet_admin
                SET creator=FALSE 
                 Where chat_id=%(chat_id)s AND user_id=%(user_id)s;''',
                {'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def add_admin(chat_id, user_id):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.publicbet_admin (chat_id,user_id) 
               VALUES (%(chat_id)s,%(user_id)s)""", {'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def rem_admin(chat_id, user_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.publicbet_admin
                 WHERE chat_id= %(chat_id)s AND user_id = %(user_id)s''',
                {'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def load_admin(chat_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM ali_ag_db.publicbet_admin
    WHERE chat_id = %(chat_id)s''', {'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    admins = [i[0] for i in load]
    return admins


def load_creator(chat_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM ali_ag_db.publicbet_admin
    WHERE chat_id = %(chat_id)s AND creator = TRUE ''', {'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    creator = [i[0] for i in load]
    return creator


def check_register(chat_id, user_id):
    cur = con.cursor()
    cur.execute('''SELECT register FROM ali_ag_db.publicbet_registry
    WHERE user_id = %(user_id)s and chat_id = %(chat_id)s''', {'chat_id': int(chat_id), 'user_id': int(user_id)})
    load = cur.fetchone()
    con.commit()
    cur.close()
    if load is None or load == False:
        return False
    return True


def load_diamond(chat_id, user_id):
    cur = con.cursor()
    cur.execute('''SELECT diamond FROM ali_ag_db.publicbet_diamonds
    WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s''', {'chat_id': int(chat_id), 'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    dia = [i[0] for i in load]
    return dia


def save_bet(chat_id, user_id, num, team, zarib):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.publicbet_betting SET team=%(team)s , diamond = %(num)s , zarib = %(zarib)s WHERE chat_id= %(chat_id)s AND user_id=%(user_id)s ;
    INSERT INTO ali_ag_db.publicbet_betting (chat_id,user_id,team, diamond,zarib)
       SELECT %(chat_id)s,%(user_id)s, %(team)s, %(num)s, %(zarib)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.publicbet_betting WHERE chat_id= %(chat_id)s AND user_id=%(user_id)s);''',
                {'chat_id': int(chat_id), 'user_id': int(user_id), 'num': int(num), 'team': str(team),
                 'zarib': float(zarib)})
    con.commit()
    cur.close()


def winners(chat_id, team):
    cur = con.cursor()
    cur.execute('''SELECT user_id ,diamond,zarib  FROM ali_ag_db.publicbet_betting
                   WHERE chat_id = %(chat_id)s AND team = %(team)s''', {'chat_id': int(chat_id), 'team': str(team)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    win_users = [i[0] for i in load]
    bet_num = [i[1] for i in load]
    zarib = [i[2] for i in load]
    for i, user in enumerate(win_users, start=0):
        add_diamond(chat_id, user, zarib[i] * bet_num[i])
    return win_users, bet_num, zarib


def losers(chat_id, team):
    cur = con.cursor()
    cur.execute('''SELECT user_id ,diamond,team  FROM ali_ag_db.publicbet_betting
                   WHERE chat_id = %(chat_id)s AND team != %(team)s''', {'chat_id': int(chat_id), 'team': str(team)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    lose_users = [i[0] for i in load]
    bet_num = [i[1] for i in load]
    teams = [i[2] for i in load]
    return lose_users, bet_num, teams


def save_record(chat_id, user_id, team, diamond, win):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.publicbet_record (chat_id,user_id,team,diamond,win) 
               VALUES (%(chat_id)s,%(user_id)s,%(team)s,%(diamond)s,%(win)s )""",
                {'chat_id': int(chat_id), 'user_id': int(user_id), 'team': str(team), 'diamond': int(diamond),
                 'win': win})
    con.commit()
    cur.close()


def delete_data(chat_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.publicbet_betting
    WHERE chat_id = %(chat_id)s''', {'chat_id': int(chat_id)})
    con.commit()
    cur.close()


def load_state(chat_id, user_id):
    query = f'''
with play as (
    SELECT count(user_id) as plays
    FROM ali_ag_db.publicbet_record
    WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s
),
     win as (
         SELECT count(user_id) as wins
         FROM ali_ag_db.publicbet_record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = TRUE 
     ),
     lose as (
         SELECT count(user_id) as loses
         FROM ali_ag_db.publicbet_record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = FALSE 
     ),
     income as (
         SELECT SUM (diamond) as incomes
         FROM ali_ag_db.publicbet_record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = TRUE 
     ),
     lost as (
         SELECT SUM (diamond) as losts
         FROM ali_ag_db.publicbet_record
         WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = FALSE 
     )
select *
from play,
     win,
     lose,
     income, 
     lost
'''
    try:
        cur = con.cursor()
        cur.execute(query, {'chat_id': int(chat_id), 'user_id': int(user_id)})
        res = cur.fetchone()
        con.commit()
        cur.close()

        return res[0], res[1], res[2], res[3], res[4]
    except Exception as e:
        print(e)
        return 0, 0, 0, 0, 0


def stats(chat_id, user_id):
    query = f'''
    with besty as (
        SELECT MAX (diamond) as bestys
        FROM ali_ag_db.publicbet_record
        WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = TRUE 
    ),
         worst as (
             SELECT MAX (diamond) as worsts
             FROM ali_ag_db.publicbet_record
             WHERE chat_id = %(chat_id)s AND user_id = %(user_id)s AND win = FALSE 
         )
select *
from besty,
     worst
'''
    try:
        cur = con.cursor()
        cur.execute(query, {'chat_id': int(chat_id), 'user_id': int(user_id)})
        res = cur.fetchone()
        con.commit()
        cur.close()

        return res[0], res[1]
    except Exception as e:
        print(e)
        return 0, 0


def get_best(chat_id):
    cur = con.cursor()
    cur.execute('''select user_id ,diamond from ali_ag_db.publicbet_diamonds 
    WHERE chat_id = %(chat_id)s
    order by diamond desc limit 10''', {'chat_id': int(chat_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    diamond = [i[1] for i in load]
    return user, diamond


def register(chat_id, user_id):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.publicbet_registry (chat_id,user_id,channel,register) 
               VALUES (%(chat_id)s,%(user_id)s,FALSE,TRUE )""", {'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def check_channel(chat_id, user_id):
    cur = con.cursor()
    cur.execute('''SELECT channel FROM ali_ag_db.publicbet_registry
    WHERE user_id = %(user_id)s and chat_id = %(chat_id)s''', {'chat_id': int(chat_id), 'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    if not load[0][0]:
        return False
    return True


def save_channels(chat_id, user_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.publicbet_registry
                SET channel=TRUE 
                 Where user_id = %(user_id)s and chat_id = %(chat_id)s''',
                {'chat_id': int(chat_id), 'user_id': int(user_id)})
    con.commit()
    cur.close()


def resetdata(chat_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE ali_ag_db.publicbet_diamonds
                SET diamond = 50 
                 Where chat_id = %(chat_id)s''', {'chat_id': int(chat_id)})
    con.commit()
    cur.close()

# def infor(chat_id):
#     cur = con.cursor()
#     cur.execute('''SELECT user_id,diamond FROM ali_ag_db.diamonds
#     WHERE chat_id = %(chat_id)s
#     ORDER BY diamond DESC ''', {'chat_id': int(chat_id)})
#     load = cur.fetchall()
#     con.commit()
#     cur.close()
#     user = [i[0] for i in load]
#     diamond = [i[1] for i in load]
#     return user, diamond
