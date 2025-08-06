# Google Haritalar Firma Toplayıcı

Bu proje, **Google Haritalar** üzerinde belirttiğiniz şehir ve iş koluna göre firma listesini toplayan ve Excel dosyasına kaydeden otomatik bir bot içerir.

---

## Özellikler

- Tkinter ile basit ve kullanışlı GUI arayüzü  
- Selenium ile Google Haritalar otomasyonu  
- Firma adı, telefon numarası ve web sitesi bilgilerini toplar  
- Haritayı yakınlaştırır ve güncelleme seçeneğini aktif eder  
- Sol paneldeki firma listesini otomatik olarak kaydırır ve "Bu bölgede ara" butonuna tıklar  
- Ziyaret edilen firmaları tekrar kaydetmez  
- Verileri Excel dosyasına kaydeder, önceki verilerle birleştirir ve duplicate kayıtları siler  
- Programı arka planda çalıştırmak için threading kullanır  
- Durdurma butonu ile işlemi anında sonlandırma imkanı  

---

## Kurulum

1. Python 3 yüklü olmalı  
2. Gerekli kütüphaneler kurulmalı:

```bash
pip install selenium pandas openpyxl
