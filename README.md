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
```

3. [ChromeDriver](https://sites.google.com/chromium.org/driver/) indirilmeli ve `CHROMEDRIVER_PATH` değişkeni uygun şekilde ayarlanmalı  
4. `USER_AGENT` ve `KAYIT_DOSYASI` gibi ayarları isteğe göre düzenleyin  

---

## Kullanım

1. Programı çalıştırın  
2. Açılan pencerede **Şehir / Semt** ve **İş kolu** bilgilerini girin  
3. **Başlat** butonuna basarak işlemi başlatın  
4. İsterseniz **Durdur** butonuyla işlemi durdurabilirsiniz  
5. İşlem tamamlandığında Excel dosyasına kaydedildiğine dair bilgi alırsınız  

---

## Kodun Detayları ve İşleyişi

- Program, Google Haritalar'da belirtilen arama kelimeleriyle sonuçları getirir ve listeden tek tek firmaların detaylarını açar.  
- Firma adı, telefon numarası ve varsa web sitesi bilgilerini çeker.  
- Telefon numarası regex ile doğrulanır; numara yoksa o firma atlanır.  
- Harita yakınlaştırılır ve "Harita hareket ettiğinde sonuçları güncelle" seçeneği açılır.  
- Sol paneldeki firma listesi belirli aralıklarla scroll edilerek yeni sonuçların yüklenmesi sağlanır.  
- Her firma seçildikten sonra "Bu bölgede ara" butonuna tıklanarak bölgedeki yeni firmalar listeye eklenir.  
- Ziyaret edilen firmalar tekrar kaydedilmez.  
- Veriler pandas kullanılarak Excel dosyasına yazılır, mevcut dosya varsa üstüne eklenir ve duplicate kayıtlar temizlenir.  
- Bot, arayüzü kilitlemeden threading ile arka planda çalışır.  

---

## Geliştirme Önerileri

- Arama kelimelerini liste olarak alıp otomatik sırayla aratmak  
- Daha sağlam bekleme mekanizmaları (`WebDriverWait`) eklemek  
- Log dosyası tutmak  
- Web API ile lisans / kullanım kontrolü eklemek  
- Arayüzü geliştirmek, kayıt dosyasını seçilebilir yapmak  

---

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

---

## İletişim

Geliştirici: İsmail  
Email: info@caliskanbilisim.net  
Web: [Çalışkan Bilişim Web Tasarım](https://caliskanbilisim.net)

---

*Teşekkürler!*
