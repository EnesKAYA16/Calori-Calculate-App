# 🥗 Kalori Takip Uygulaması

Günlük kalori alımını takip etmek için geliştirilmiş, masaüstü tabanlı bir **PyQt5** uygulaması.  
Çoklu kullanıcı desteği, profil yönetimi, BMR hesaplama ve tema sistemi içerir.

---

## 📸 Özellikler

- 🔐 **Kullanıcı Sistemi** — Kayıt ol, giriş yap, şifre değiştir (SHA-256 hash ile güvenli saklama)
- 👤 **Profil Yönetimi** — Boy, kilo, yaş, cinsiyet ve aktivite seviyesi girişi
- 🧮 **Otomatik Kalori Hesaplama** — Mifflin-St Jeor formülüyle BMR ve günlük kalori ihtiyacı (TDEE) hesaplama
- 🍽️ **Günlük Takip** — Yiyecek ekle / sil, anlık kalori özeti
- 📊 **İlerleme Çubuğu** — Hedefe göre renkli durum göstergesi (yeşil / kırmızı)
- 🎨 **Tema Sistemi** — Koyu 🌙 ve Açık ☀️ tema desteği, tercih hesaba kaydedilir
- 💾 **Kalıcı Veri** — SQLite veritabanı, tüm kayıtlar yerel olarak saklanır
- 🖥️ **Tam Ekran Desteği** — Yeniden boyutlandırılabilir, tam ekran yapılabilir pencere

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- PyQt5

### Adımlar

```bash
# Repoyu klonla
git clone https://github.com/kullanici-adin/kalori-takip.git
cd kalori-takip

# Gerekli paketi yükle
pip install PyQt5

# Uygulamayı çalıştır
python Proje.py
```

> **Not:** Uygulama ilk çalıştırmada `kalori.db` adlı bir SQLite veritabanı oluşturur.  
> Bu dosya `.py` dosyasıyla aynı klasörde yer alır.

---

## 🗂️ Proje Yapısı

```
kalori-takip/
│
├── Proje.py          # Ana uygulama dosyası
├── kalori.db         # SQLite veritabanı (otomatik oluşturulur)
└── README.md
```

---

## 🧠 BMR Hesaplama Yöntemi

Uygulama, **Mifflin-St Jeor** formülünü kullanır:

| Cinsiyet | Formül |
|----------|--------|
| Erkek    | `(10 × kilo) + (6.25 × boy) − (5 × yaş) + 5` |
| Kadın    | `(10 × kilo) + (6.25 × boy) − (5 × yaş) − 161` |

Bulunan BMR değeri aktivite katsayısıyla çarpılarak **TDEE** (günlük toplam enerji harcaması) hesaplanır:

| Aktivite Seviyesi | Katsayı |
|-------------------|---------|
| Hareketsiz        | 1.20    |
| Hafif aktif       | 1.375   |
| Orta aktif        | 1.55    |
| Aktif             | 1.725   |
| Çok aktif         | 1.90    |

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| Python 3  | Ana programlama dili |
| PyQt5     | Masaüstü arayüz kütüphanesi |
| SQLite3   | Yerel veritabanı |
| hashlib   | SHA-256 şifre hashleme |

---

## 📋 Veritabanı Şeması

```
kullanicilar   → id, kullanici_adi, sifre_hash
profil         → kullanici_id, cinsiyet, yas, boy, kilo, aktivite, tema
hedef          → kullanici_id, gunluk_kcal
yiyecekler     → id, kullanici_id, isim, kalori, tarih
```

---

## 🔮 Gelecek Özellikler

- [ ] Haftalık / aylık kalori grafiği (matplotlib)
- [ ] Yiyecek veritabanı ve otomatik tamamlama
- [ ] Öğün kategorileri (kahvaltı, öğle, akşam)
- [ ] Makro besin takibi (protein, karbonhidrat, yağ)
- [ ] Excel / PDF rapor dışa aktarma
- [ ] Su takibi

---

## 👨‍💻 Geliştirici

Bu proje **Görsel Programlama** dersi kapsamında geliştirilmiştir.
