## Klinik Yönetim Sistemi (Clinic Management System)

Bu proje, bir sağlık kliniğindeki hasta kayıtları, doktor bilgileri ve randevu süreçlerini modern bir arayüzle yönetmek için tasarlanmıştır. Veriler, ilişkisel bir veritabanı (SQLite) üzerinde güvenli ve kalıcı bir şekilde saklanmaktadır.

## Projenin Amacı
Manuel kayıt tutma süreçlerini dijitalleştirerek hata payını azaltmak, verilere hızlı erişim sağlamak ve modern nesne tabanlı programlama (OOP) prensiplerini gerçek bir senaryoda uygulamaktır.

##  Kullanılan Teknolojiler
- **Programlama Dili:** Python 3.x
- **Kullanıcı Arayüzü:** CustomTkinter (Modern ve Responsive GUI)
- **Veritabanı:** SQLite3 (Serverless SQL Database)
- **Versiyon Kontrol:** Git & GitHub

##  Modüllerin Amacı
Proje, "Sorumlulukların Ayrılması" (Separation of Concerns) prensibine göre modüllere ayrılmıştır:
- **`veritabanı_yöneticisi.py`:** SQL bağlantılarını, tablo oluşturma işlemlerini ve veri alışverişini (CRUD) yöneten katmandır.
- **`arayüz.py`:** Kullanıcı panellerini, buton fonksiyonlarını ve görsel geri bildirimleri yöneten katmandır.
- **`modeller.py`:** Sistemdeki hasta ve doktor gibi temel nesnelerin şablonlarını (sınıflarını) barındırır.

## Nasıl Çalıştırılır?
1. Bilgisayarınızda Python'un kurulu olduğundan emin olun.
2. Gerekli kütüphaneyi yükleyin: `pip install customtkinter`
3. Terminal veya IDE üzerinden `ana.py` (veya ana dosyanız hangisiyse) dosyasını çalıştırın.
