import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Tema Ayarı
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ==========================================
# 1. VERİTABANI MOTORU
# ==========================================
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

# ==========================================
# 2. ARAYÜZ
# ==========================================
class KlinikSistemi(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Klinik Yönetim Sistemi")
        self.geometry("1100x750")
        self.configure(fg_color="#f8f4eb")

        # Sol Menü
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#e9ecef")
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="KLİNİK PANEL", font=("Arial", 22, "bold"), text_color="#343a40").pack(pady=40)
        
        # Butonlar - Hatanın düzeltildiği yer burası!
        ctk.CTkButton(self.sidebar, text="Hasta Kayıt", command=self.hasta_ekrani, width=180, height=40).pack(pady=12, padx=20)
        ctk.CTkButton(self.sidebar, text="Doktor Kayıt", command=self.doktor_ekrani, width=180, height=40).pack(pady=12, padx=20)
        ctk.CTkButton(self.sidebar, text="Randevu Al", command=self.randevu_ekrani, fg_color="#76c893", hover_color="#52b788", width=180, height=40).pack(pady=12, padx=20)
        ctk.CTkButton(self.sidebar, text="Randevu Listesi", command=self.liste_ekrani, width=180, height=40).pack(pady=12, padx=20)

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#ffffff", border_width=2, border_color="#dee2e6")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        self.ana_yazi()

    def temizle(self):
        for widget in self.main_frame.winfo_children(): widget.destroy()

    def ana_yazi(self):
        self.temizle()
        ctk.CTkLabel(self.main_frame, text="HOŞ GELDİNİZ", font=("Arial", 35, "bold"), text_color="#1f538d").pack(expand=True)

    def hasta_ekrani(self):
        self.temizle()
        ctk.CTkLabel(self.main_frame, text="YENİ HASTA KAYDI", font=("Arial", 20, "bold")).pack(pady=20)
        self.h_ad = ctk.CTkEntry(self.main_frame, placeholder_text="Adı", width=300); self.h_ad.pack(pady=10)
        self.h_soyad = ctk.CTkEntry(self.main_frame, placeholder_text="Soyadı", width=300); self.h_soyad.pack(pady=10)
        self.h_tc = ctk.CTkEntry(self.main_frame, placeholder_text="TC No", width=300); self.h_tc.pack(pady=10)
        self.h_kan = ctk.CTkEntry(self.main_frame, placeholder_text="Kan Grubu", width=300); self.h_kan.pack(pady=10)
        ctk.CTkButton(self.main_frame, text="KAYDET", command=self.hasta_kaydet, width=200).pack(pady=30)

    def hasta_kaydet(self):
        with DatabaseManager.baglan() as conn:
            conn.execute("INSERT INTO hastalar (ad, soyad, tc, kan) VALUES (?, ?, ?, ?)", (self.h_ad.get(), self.h_soyad.get(), self.h_tc.get(), self.h_kan.get()))
        messagebox.showinfo("Başarılı", "Hasta eklendi!")
        self.ana_yazi()

    def doktor_ekrani(self):
        self.temizle()
        ctk.CTkLabel(self.main_frame, text="YENİ DOKTOR KAYDI", font=("Arial", 20, "bold")).pack(pady=20)
        self.d_ad = ctk.CTkEntry(self.main_frame, placeholder_text="Adı", width=300); self.d_ad.pack(pady=10)
        self.d_soyad = ctk.CTkEntry(self.main_frame, placeholder_text="Soyadı", width=300); self.d_soyad.pack(pady=10)
        uzm = ["Göz", "Kardiyoloji", "Dahiliye", "KBB", "Nöroloji", "Ortopedi", "Cildiye", "Pediatri"]
        self.d_uzm = ctk.CTkOptionMenu(self.main_frame, values=uzm, width=300); self.d_uzm.pack(pady=10)
        ctk.CTkButton(self.main_frame, text="KAYDET", command=self.doktor_kaydet, width=200).pack(pady=30)

    def doktor_kaydet(self):
        with DatabaseManager.baglan() as conn:
            conn.execute("INSERT INTO doktorlar (ad, soyad, uzmanlik) VALUES (?, ?, ?)", (self.d_ad.get(), self.d_soyad.get(), self.d_uzm.get()))
        messagebox.showinfo("Başarılı", "Doktor eklendi!")
        self.ana_yazi()

    def randevu_ekrani(self):
        self.temizle()
        with DatabaseManager.baglan() as conn:
            h = conn.execute("SELECT ad, soyad FROM hastalar").fetchall()
            d = conn.execute("SELECT ad, soyad, uzmanlik FROM doktorlar").fetchall()
        if not h or not d:
            ctk.CTkLabel(self.main_frame, text="Kayıt bulunamadı!", text_color="red").pack(pady=50); return
        h_l = [f"{i[0]} {i[1]}" for i in h]
        d_l = [f"Dr. {i[0]} {i[1]} ({i[2]})" for i in d]
        self.sec_h = ctk.CTkOptionMenu(self.main_frame, values=h_l, width=350); self.sec_h.pack(pady=10)
        self.sec_d = ctk.CTkOptionMenu(self.main_frame, values=d_l, width=350); self.sec_d.pack(pady=10)
        self.r_t = ctk.CTkEntry(self.main_frame, placeholder_text="Tarih", width=350); self.r_t.pack(pady=20)
        ctk.CTkButton(self.main_frame, text="ONAYLA", command=self.randevu_kaydet, fg_color="#2a9d8f", width=250).pack(pady=20)

    def randevu_kaydet(self):
        with DatabaseManager.baglan() as conn:
            conn.execute("INSERT INTO randevular (hasta_bilgi, doktor_bilgi, tarih) VALUES (?, ?, ?)", (self.sec_h.get(), self.sec_d.get(), self.r_t.get()))
        messagebox.showinfo("Sistem", "Randevu kaydedildi!")
        self.liste_ekrani()

    def liste_ekrani(self):
        self.temizle()
        ctk.CTkLabel(self.main_frame, text="AKTİF RANDEVU LİSTESİ", font=("Arial", 22, "bold")).pack(pady=30)
        scroll = ctk.CTkScrollableFrame(self.main_frame, width=700, height=450, fg_color="transparent")
        scroll.pack(pady=10, fill="both", expand=True)
        with DatabaseManager.baglan() as conn:
            randevular = conn.execute("SELECT * FROM randevular").fetchall()
        for r in randevular:
            f = ctk.CTkFrame(scroll, fg_color="#f1f3f5", corner_radius=10)
            f.pack(pady=8, fill="x", padx=10)
            ctk.CTkLabel(f, text=f"📅 {r[3]} | 👤 {r[1]} ➔ 🏥 {r[2]}", font=("Arial", 14)).pack(pady=12)

if __name__ == "__main__":
    DatabaseManager.tablolari_olustur()
    app = KlinikSistemi()
    app.mainloop()