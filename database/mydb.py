import mysql.connector

class Database:
    def __init__(self):
        self.db = None

    def ulanish(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rustam123456b',
            database='ice_cream'
        )

    def ishlatish(self, sql, fetchall=False, fetchone=False, commit=False):
        self.db = self.ulanish()
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = None
        if fetchall:
            data = cursor.fetchall()
        elif fetchone:
            data = cursor.fetchone()
        elif commit:
            self.db.commit()

        self.db.close()
        return data

    def hodimlar(self):
        sql = "select * from hodimlar"
        return self.ishlatish(sql, fetchall=True)

    def muzqaymoqlar(self):
        sql = "select * from muzqaymoqlar"
        return self.ishlatish(sql, fetchall=True)

    def mijozlar(self):
        sql = "select * from mijozlar"
        return self.ishlatish(sql, fetchall=True)

    def hodim(self, id):
        sql = f"select * from hodimlar where id={id}"
        return self.ishlatish(sql, fetchone=True)

    def hodimqushish(self, ism, familiya, tel, ish, karta):
        sql = f"""
        insert into hodimlar(ism, familiya, tel_raqam, ish_boshlagan, karta_raqam)
        values ('{ism}', '{familiya}', '{tel}', '{ish}', '{karta}')
        """
        self.ishlatish(sql, commit=True)

    def muzqaymoqturlari(self):
        sql = "SELECT * FROM turi"
        return self.ishlatish(sql, fetchall=True)

    def muzqaymoqqushish(self, nomi, narxi, turi_id, ishlab_chiq_sana, yaroqlilik_muddati, soni, rasm):
        sql = f"""
        INSERT INTO muzqaymoqlar(nomi, narxi, turi_id, ishlab_chiq_sana, yaroqlilik_muddati, soni, rasm)
        VALUES
        ('{nomi}', {narxi}, {turi_id}, '{ishlab_chiq_sana}', '{yaroqlilik_muddati}', {soni}, '{rasm}')
        """
        self.ishlatish(sql, commit=True)

    def hodimTahrir(self,id, ism, familiya, tel, ish_boshlash, karta):
        sql = f"""
        UPDATE hodimlar SET ism='{ism}', 
        familiya='{familiya}', 
        tel_raqam='{tel}', 
        ish_boshlagan='{ish_boshlash}', 
        karta_raqam='{karta}'
        WHERE id = {id}
        """
        self.ishlatish(sql, commit=True)

    def hodimid(self, id):
        sql = f"select * from hodimlar where id = {id}"
        return self.ishlatish(sql, fetchone=True)

    def hodimdel(self, id):
        sql = f"DELETE FROM hodimlar WHERE id = {id}"
        self.ishlatish(sql, commit=True)

    def search(self, matn):
        sql = f"select * from hodimlar where ism LIKE '%{matn}%' or familiya LIKE '%{matn}%' "
        return self.ishlatish(sql, fetchall=True)

mydb = Database()