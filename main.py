# main.py - Uygulama Başlatıcı Modül
from database_manager import DatabaseManager
from interface import KlinikSistemi

if __name__ == "__main__":
    # 1. Önce veritabanını ve tabloları hazırla
    DatabaseManager.tablolari_olustur()
    
    # 2. Arayüzü (Klinik Sistemi) başlat
    app = KlinikSistemi()
    
    # 3. Uygulamanın ekranda kalmasını sağlayan ana döngü
    app.mainloop()
