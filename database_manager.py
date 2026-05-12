import sqlite3

class DatabaseManager:
    @staticmethod
    def baglan():
        return sqlite3.connect("klinik_merkezi.db")

    @staticmethod
    def tablolari_olustur():
        with DatabaseManager.baglan() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS hastalar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, soyad TEXT, tc TEXT, kan TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS doktorlar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, soyad TEXT, uzmanlik TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS randevular (id INTEGER PRIMARY KEY AUTOINCREMENT, hasta_bilgi TEXT, doktor_bilgi TEXT, tarih TEXT)")
            conn.commit()

    @staticmethod
    def veri_ekle(sorgu, veriler):
        with DatabaseManager.baglan() as conn:
            cursor = conn.cursor()
            cursor.execute(sorgu, veriler)
            conn.commit()

    @staticmethod
    def veri_cek(sorgu):
        with DatabaseManager.baglan() as conn:
            cursor = conn.cursor()
            cursor.execute(sorgu)
            return cursor.fetchall()