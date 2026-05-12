# models.py - Nesne Tabanlı Programlama (OOP) Mimarisi

class Kisi:
    """
    Ata Sınıf (Base Class): Hasta ve Doktor sınıfları bu sınıftan türetilir (Inheritance). [cite: 20, 31]
    """
    def __init__(self, ad, soyad, tc):
        self.ad = ad
        self.soyad = soyad
        # Kapsülleme (Encapsulation): TC numarası '__' ile gizlenmiştir. 
        # Bu veriye sınıf dışından doğrudan erişilemez, güvenliği sağlar.
        self.__tc = tc 

    def kimlik_bilgisi(self):
        """Kalıtım yoluyla alt sınıflarda kullanılacak ortak metod."""
        return f"{self.ad} {self.soyad}"

    def get_tc(self):
        """Kapsüllenmiş (gizli) TC verisine güvenli erişim sağlayan metod (Getter)."""
        return self.__tc

class Hasta(Kisi):
    """
    Kalıtım (Inheritance): Kisi sınıfının tüm özelliklerini miras alır. [cite: 20, 31]
    """
    def __init__(self, ad, soyad, tc, kan_grubu):
        # super() kullanarak Kisi sınıfındaki özellikleri içeri aktarıyoruz.
        super().__init__(ad, soyad, tc)
        self.kan_grubu = kan_grubu

class Doktor(Kisi):
    """
    Kalıtım (Inheritance): Doktorlar da birer 'Kisi'dir. [cite: 20, 31]
    """
    def __init__(self, ad, soyad, tc, uzmanlik):
        super().__init__(ad, soyad, tc)
        self.uzmanlik = uzmanlik

class Randevu:
    """
    Bu sınıf, Hasta ve Doktor nesnelerini bir araya getirir (Nesne İlişkilendirme). 
    """
    def __init__(self, hasta, doktor, tarih):
        self.hasta = hasta
        self.doktor = doktor
        self.tarih = tarih