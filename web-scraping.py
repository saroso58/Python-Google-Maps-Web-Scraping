import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import threading
import re
import os
import ctypes
import time

# === Ayarlar ===
CHROMEDRIVER_PATH = "C:/chromedriver-win64/chromedriver.exe"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
KAYIT_DOSYASI = "kayitli_veriler.xlsx"
durdur_flag = False

# Konsolu gizle
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def telefon_al(driver):
    try:
        time.sleep(1)
        tum_divler = driver.find_elements(By.TAG_NAME, "div")
        for div in tum_divler:
            text = div.text.strip()
            if re.match(r"^05[0-9]{2} [0-9]{3} [0-9]{2} [0-9]{2}$", text) or \
               re.match(r"^05[0-9]{9}$", text) or \
               re.match(r"^\(?05[0-9]{2}\)? ?[0-9]{3} ?[0-9]{4}$", text):
                return text
        return "Yok"
    except:
        return "Yok"

def zoom_in(driver, kere=3):
    try:
        zoom_buton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Yakınlaştır"]'))
        )
        for _ in range(kere):
            zoom_buton.click()
            time.sleep(0.3)
    except Exception as e:
        print(f"Zoom hatası: {e}")

def harita_hareket_tik_ac(driver):
    try:
        tik_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[role="checkbox"][jsaction*="pane.queryOnPan.toggle"]'))
        )
        aria_checked = tik_button.get_attribute("aria-checked")
        if aria_checked == "false":
            tik_button.click()
            time.sleep(0.5)
    except Exception as e:
        print(f"Harita hareket tik açma hatası: {e}")

def listeyi_kaydir(driver, element, miktar=500):
    driver.execute_script("arguments[0].scrollTop += arguments[1];", element, miktar)

def bu_bolgede_ara(driver):
    try:
        buton = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Bu bölgede ara")] | //div[contains(text(),"Bu bölgede ara")]'))
        )
        driver.execute_script("arguments[0].click();", buton)
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
        )
    except:
        pass

def kartlar_bekle(driver, timeout=7):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
        )
        return driver.find_elements(By.CLASS_NAME, "hfpxzc")
    except:
        return []

def durdur():
    global durdur_flag
    durdur_flag = True
    messagebox.showinfo("Bilgi", "Bot durduruluyor... Pencere kapanınca işlem sona erer.")

def calistir():
    global durdur_flag
    durdur_flag = False

    sehir = entry_sehir.get().strip()
    is_kolu = text_is_kolu.get("1.0", tk.END).strip()

    if not sehir or not is_kolu:
        messagebox.showwarning("Uyarı", "Lütfen şehir ve iş kolu(ları) girin.")
        return

    kelimeler = [k.strip() for k in is_kolu.split("\n") if k.strip()]
    if not kelimeler:
        messagebox.showwarning("Uyarı", "En az bir arama kelimesi girin.")
        return

    btn_baslat.config(state="disabled")
    btn_durdur.config(state="normal")

    thread = threading.Thread(target=bot_multi_calistir, args=(sehir, kelimeler))
    thread.start()

def bot_multi_calistir(sehir, kelimeler):
    global durdur_flag
    tum_veriler = []

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(f"user-agent={USER_AGENT}")
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        for is_kolu in kelimeler:
            if durdur_flag:
                break

            print(f"\n>> '{is_kolu}' için arama başlıyor...")
            arama_url = f"https://www.google.com/maps/search/{is_kolu}+{sehir}"
            driver.get(arama_url)

            time.sleep(5)  # Açılış beklemesi

            zoom_in(driver, kere=3)
            harita_hareket_tik_ac(driver)

            kaydirma_alani = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
            )

            ziyaret_edilen = set()
            veriler = []

            while not durdur_flag:
                kartlar = kartlar_bekle(driver, 7)
                if not kartlar:
                    break

                for i, kart in enumerate(kartlar):
                    if durdur_flag:
                        break

                    try:
                        kart_id = kart.get_attribute("aria-label")
                        if not kart_id or kart_id in ziyaret_edilen:
                            continue

                        ziyaret_edilen.add(kart_id)
                        kart.click()

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf"))
                        )

                        bu_bolgede_ara(driver)

                        ad = driver.find_element(By.CLASS_NAME, "DUwDvf").text
                        tel = telefon_al(driver)

                        if tel == "Yok":
                            continue

                        try:
                            site = driver.find_element(By.XPATH, "//a[contains(@href,'http') and contains(@aria-label,'Web sitesi')]").get_attribute("href")
                        except:
                            site = "Yok"

                        if (ad, tel, site) in [(v["İsim"], v["Telefon"], v["Web Sitesi"]) for v in veriler]:
                            continue

                        kayit = {
                            "İsim": ad,
                            "Telefon": tel,
                            "Web Sitesi": site,
                            "Şehir/Semt": sehir,
                            "İş Kolu": is_kolu
                        }

                        veriler.append(kayit)
                        tum_veriler.append(kayit)

                        print(f"{len(veriler)}. {ad} | {tel} | {site} | {sehir} | {is_kolu}")

                        if (i + 1) % 3 == 0:
                            listeyi_kaydir(driver, kaydirma_alani, 400)
                            time.sleep(0.7)

                    except Exception as e:
                        print(f"Hata: {e}")
                        continue

                try:
                    daha_fazla = driver.find_element(By.XPATH, "//button[contains(text(),'Daha fazla')] | //span[contains(text(),'Daha fazla')]")
                    driver.execute_script("arguments[0].click();", daha_fazla)
                    WebDriverWait(driver, 7).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
                    )
                except:
                    break

            print(f"'{is_kolu}' araması tamamlandı.")

        if tum_veriler:
            try:
                if os.path.exists(KAYIT_DOSYASI):
                    eski_df = pd.read_excel(KAYIT_DOSYASI)
                    df = pd.concat([eski_df, pd.DataFrame(tum_veriler)], ignore_index=True)
                else:
                    df = pd.DataFrame(tum_veriler)

                df.drop_duplicates(inplace=True)
                df.to_excel(KAYIT_DOSYASI, index=False)
            except Exception as e:
                print(f"Dosya kaydetme hatası: {e}")

        driver.quit()
        if not durdur_flag:
            messagebox.showinfo("Bitti", f"Tüm aramalar tamamlandı.\nExcel dosyasına kaydedildi:\n{KAYIT_DOSYASI}")
        else:
            messagebox.showinfo("Durduruldu", "İşlem kullanıcı tarafından durduruldu.")

    except Exception as e:
        messagebox.showerror("Hata", str(e))
        try:
            driver.quit()
        except:
            pass
    finally:
        btn_baslat.config(state="normal")
        btn_durdur.config(state="disabled")

# === Arayüz ===
root = tk.Tk()
root.title("Google Haritalar Firma Toplayıcı")
root.geometry("400x350")
root.resizable(False, False)

lbl_sehir = tk.Label(root, text="Şehir / Semt:")
lbl_sehir.pack(pady=(15, 5))
entry_sehir = tk.Entry(root, width=40)
entry_sehir.pack()

lbl_is = tk.Label(root, text="İş Kolu (her satıra bir arama kelimesi):")
lbl_is.pack(pady=(15, 5))
text_is_kolu = scrolledtext.ScrolledText(root, width=40, height=8)
text_is_kolu.pack()

btn_baslat = tk.Button(root, text="Başlat", command=calistir)
btn_baslat.pack(pady=(20, 5))

btn_durdur = tk.Button(root, text="Durdur", command=durdur, state="disabled")
btn_durdur.pack(pady=(0, 10))

root.mainloop()
