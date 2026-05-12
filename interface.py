import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# ==========================================
# 1. VERİTABANI MOTORU (Database Manager)
# ==========================================
class DatabaseManager:
    @staticmethod
    def baglan():
        return sqlite3.connect("klinik_merkezi.db")

    @staticmethod
    def tablolari_olustur():
        with DatabaseManager.baglan() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS hastalar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, soyad TEXT, tc TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS doktorlar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, soyad TEXT, uzmanlik TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS randevular (id INTEGER PRIMARY KEY AUTOINCREMENT, hasta_bilgi TEXT, doktor_bilgi TEXT, tarih TEXT)")
            conn.commit()

# ==========================================
# 2. ARAYÜZ (Interface)
# ==========================================
class KlinikSistemi(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Klinik Yönetim Sistemi - FINAL")
        self.geometry("1000x700")
        
        # Sol Menü
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkButton(self.sidebar, text="Hasta Kayıt", command=self.hasta_ekrani).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Doktor Kayıt", command=self.doktor_ekrani).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Randevu Al", command=self.randevu_ekrani, fg_color="green").pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Randevu Listesi", command=self.liste_ekrani).pack(pady=10, padx=10)

        # Sağ İçerik
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.welcome_text = ctk.CTkLabel(self.main_frame, text="LÜTFEN SOL MENÜDEN İŞLEM SEÇİN", font=("Arial", 20))
        self.welcome_text.pack(expand=True)

    def temizle(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- HASTA KAYIT ---
    def hasta_ekrani(self):
        self.temizle()
        ctk.CTkLabel(self.main_frame, text="HASTA KAYIT FORMU", font=("Arial", 18, "bold")).pack(pady=20)
        self.h_ad = ctk.CTkEntry(self.main_frame, placeholder_text="Hasta Adı"); self.h_ad.pack(pady=5)
        self.h_soyad = ctk.CTkEntry(self.main_frame, placeholder_text="Hasta Soyadı"); self.h_soyad.pack(pady=5)
        ctk.CTkButton(self.main_frame, text="VERİTABANINA KAYDET", command=self.hasta_kaydet).pack(pady=20)

    def hasta_kaydet(self):
        with DatabaseManager.baglan() as conn:
            conn.execute("INSERT INTO hastalar (ad, soyad) VALUES (?, ?)", (self.h_ad.get(), self.h_soyad.get()))
        messagebox.showinfo("Başarılı", "Hasta SQL'e eklendi!")

    # --- DOKTOR KAYIT ---
    def doktor_ekrani(self):
        self.temizle()
        ctk.CTkLabel(self.main_frame, text="DOKTOR KAYIT FORMU", font=("Arial", 18, "bold")).pack(pady=20)
        self.d_ad = ctk.CTkEntry(self.main_frame, placeholder_text="Doktor Adı"); self.d_ad.pack(pady=5)
        self.d_uzm = ctk.CTkOptionMenu(self.main_frame, values=["Göz", "Kardiyoloji", "Dahiliye"]); self.d_uzm.pack(pady=10)
        ctk.CTkButton(self.main_frame, text="VERİTABANINA KAYDET", command=self.doktor_kaydet).pack(pady=20)

    def doktor_kaydet(self):
        with DatabaseManager.baglan() as conn:
            conn.execute("INSERT INTO doktorlar (ad, uzmanlik) VALUES (?, ?)", (self.d_ad.get(), self.d_uzm.get()))
        messagebox.showinfo("Başarılı", "Doktor SQL'e eklendi!")

    # --- RANDEVU AL (KRİTİK NOKTA) ---
    def randevu_ekrani(self):
        self.temizle()
        with DatabaseManager.baglan() as conn:
            hastalar = conn.execute("SELECT ad, soyad FROM hastalar").fetchall()
            doktorlar = conn.execute("SELECT ad, uzmanlik FROM doktorlar").fetchall()

        if not hastalar or not doktorlar:
            ctk.CTkLabel(self.main_frame, text="HATA: Önce hasta ve doktor kaydetmelisiniz!", text_color="red").pack(pady=50)
            return

        h_liste = [f"{h[0]} {h[1]}" for h in hastalar]
        d_liste = [f"Dr. {d[0]} ({d[1]})" for d in doktorlar]

        self.sec_h = ctk.CTkOptionMenu(self.main_frame, values=h_liste); self.sec_h.pack(pady=10)
        self.sec_d = ctk.CTkOptionMenu(self.main_frame, values=d_liste); self.sec_d.pack(pady=10)
        self.r_tarih = ctk.CTkEntry(self.main_frame, placeholder_text="Tarih"); self.r_tarih.pack(pady=10)
        ctk.CTkButton(self.main_frame, text="RANDEVUYU ONAYLA", command=self.randevu_kaydet, fg_color="green").pack(pady=20)

    def randevu_kaydet(self):
        with DatabaseManager.baglan() as conn:
            conn.execute("INSERT INTO randevular (hasta_bilgi, doktor_bilgi, tarih) VALUES (?, ?, ?)", 
                         (self.sec_h.get(), self.sec_d.get(), self.r_tarih.get()))
        messagebox.showinfo("Başarılı", "Randevu kaydedildi!")

    def liste_ekrani(self):
        self.temizle()
        with DatabaseManager.baglan() as conn:
            randevular = conn.execute("SELECT * FROM randevular").fetchall()
        for r in randevular:
            ctk.CTkLabel(self.main_frame, text=f"{r[3]} | {r[1]} -> {r[2]}").pack(pady=2)

# ==========================================
# 3. BAŞLATICI
# ==========================================
if __name__ == "__main__":
    DatabaseManager.tablolari_olustur()
    app = KlinikSistemi()
    app.mainloop()