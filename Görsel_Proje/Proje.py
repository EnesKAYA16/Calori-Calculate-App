import sys
import os
import sqlite3
import hashlib
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox,
    QProgressBar, QSpinBox, QDoubleSpinBox, QGroupBox,
    QStackedWidget, QFrame, QSizePolicy, QScrollArea,
    QComboBox, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette


# ══════════════════════════════════════════════════════
#  TEMA SİSTEMİ
# ══════════════════════════════════════════════════════
TEMALAR = {
    "koyu": {
        "bg":           "#0f1923",
        "bg_kart":      "#1a2535",
        "bg_kart2":     "#1e2d42",
        "vurgu":        "#00d4a0",
        "vurgu_koyu":   "#00a87e",
        "vurgu_acik":   "#33ddb3",
        "tehlike":      "#ff5c5c",
        "tehlike_koyu": "#cc3c3c",
        "metin":        "#e8f0fe",
        "metin_soluk":  "#8899aa",
        "sinir":        "#263548",
        "basarili_bg":  "rgba(0,212,160,0.12)",
        "hata_bg":      "rgba(255,92,92,0.15)",
    },
    "acik": {
        "bg":           "#f0f4f8",
        "bg_kart":      "#ffffff",
        "bg_kart2":     "#e8f0f8",
        "vurgu":        "#00956e",
        "vurgu_koyu":   "#007055",
        "vurgu_acik":   "#00b885",
        "tehlike":      "#e53935",
        "tehlike_koyu": "#b71c1c",
        "metin":        "#1a2535",
        "metin_soluk":  "#607080",
        "sinir":        "#c8d8e8",
        "basarili_bg":  "rgba(0,149,110,0.10)",
        "hata_bg":      "rgba(229,57,53,0.10)",
    }
}

_aktif_tema = "koyu"

def R(anahtar):
    """Aktif temadan renk döndürür."""
    return TEMALAR[_aktif_tema][anahtar]

def tema_sec(ad):
    global _aktif_tema
    _aktif_tema = ad


# ══════════════════════════════════════════════════════
#  STİL ÜRETİCİLER  (tema değişince yeniden çağrılır)
# ══════════════════════════════════════════════════════
def genel_stil():
    return f"""
        QMainWindow, QWidget {{
            background-color: {R('bg')};
            color: {R('metin')};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        }}
        QScrollBar:vertical {{
            background: {R('bg_kart')};
            width: 8px; border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {R('sinir')};
            border-radius: 4px; min-height: 30px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """

def giris_stil():
    return f"""
        QLineEdit {{
            background-color: {R('bg_kart2')};
            color: {R('metin')};
            border: 1.5px solid {R('sinir')};
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 13px;
        }}
        QLineEdit:focus {{ border: 1.5px solid {R('vurgu')}; }}
    """

def kart_stil():
    return f"""
        QGroupBox {{
            background-color: {R('bg_kart')};
            border: 1px solid {R('sinir')};
            border-radius: 14px;
            margin-top: 10px; padding: 12px;
            color: {R('metin')};
            font-size: 12px; font-weight: 600;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 14px; top: -2px;
            color: {R('vurgu')}; font-size: 12px;
        }}
    """

def liste_stil():
    return f"""
        QListWidget {{
            background-color: {R('bg_kart2')};
            border: 1px solid {R('sinir')};
            border-radius: 10px;
            color: {R('metin')};
            font-size: 12px; outline: none; padding: 4px;
        }}
        QListWidget::item {{
            padding: 8px 12px; border-radius: 7px; margin: 2px;
        }}
        QListWidget::item:selected {{
            background-color: {R('bg_kart')};
            color: {R('vurgu')};
            border: 1px solid {R('vurgu')};
        }}
        QListWidget::item:hover:!selected {{ background-color: {R('sinir')}; }}
    """

def spinbox_stil():
    return f"""
        QSpinBox, QDoubleSpinBox {{
            background-color: {R('bg_kart2')};
            color: {R('metin')};
            border: 1.5px solid {R('sinir')};
            border-radius: 8px; padding: 5px 8px; font-size: 13px;
        }}
        QSpinBox:focus, QDoubleSpinBox:focus {{ border: 1.5px solid {R('vurgu')}; }}
        QSpinBox::up-button, QSpinBox::down-button,
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
            background-color: {R('sinir')}; border-radius: 4px; width: 18px;
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover,
        QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
            background-color: {R('vurgu')};
        }}
    """

def combo_stil():
    return f"""
        QComboBox {{
            background-color: {R('bg_kart2')};
            color: {R('metin')};
            border: 1.5px solid {R('sinir')};
            border-radius: 8px; padding: 5px 10px; font-size: 13px;
        }}
        QComboBox:focus {{ border: 1.5px solid {R('vurgu')}; }}
        QComboBox::drop-down {{ border: none; width: 24px; }}
        QComboBox QAbstractItemView {{
            background-color: {R('bg_kart')};
            color: {R('metin')};
            border: 1px solid {R('sinir')};
            selection-background-color: {R('vurgu')};
        }}
    """

def yesil_btn(boyut=13):
    return (
        f"QPushButton {{ background-color: {R('vurgu')}; color: #0f1923; "
        f"border-radius: 10px; font-size: {boyut}px; font-weight: 700; padding: 6px; border: none; }}"
        f"QPushButton:hover {{ background-color: {R('vurgu_acik')}; }}"
        f"QPushButton:pressed {{ background-color: {R('vurgu_koyu')}; }}"
    )

def kirmizi_btn(boyut=12):
    return (
        f"QPushButton {{ background-color: {R('tehlike')}; color: white; "
        f"border-radius: 10px; font-size: {boyut}px; font-weight: 700; padding: 6px; border: none; }}"
        f"QPushButton:hover {{ background-color: #ff7a7a; }}"
        f"QPushButton:pressed {{ background-color: {R('tehlike_koyu')}; }}"
    )

def gri_btn(boyut=12):
    return (
        f"QPushButton {{ background-color: {R('sinir')}; color: {R('metin_soluk')}; "
        f"border-radius: 10px; font-size: {boyut}px; font-weight: 600; padding: 6px; border: none; }}"
        f"QPushButton:hover {{ background-color: {R('bg_kart2')}; color: {R('metin')}; }}"
        f"QPushButton:pressed {{ background-color: {R('bg')}; }}"
    )


# ══════════════════════════════════════════════════════
#  VERİTABANI
# ══════════════════════════════════════════════════════
class Veritabani:
    def __init__(self, db_adi="kalori.db"):
        script_klasor = os.path.dirname(os.path.abspath(__file__))
        self.db_adi = os.path.join(script_klasor, db_adi)
        self.baglanti = sqlite3.connect(self.db_adi)
        self.baglanti.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.baglanti.cursor()
        self._migrasyonu_kontrol_et()
        self.tablolari_olustur()

    def _migrasyonu_kontrol_et(self):
        """Eski şema varsa sıfırla."""
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='yiyecekler'"
        )
        if self.cursor.fetchone():
            self.cursor.execute("PRAGMA table_info(yiyecekler)")
            sutunlar = [r[1] for r in self.cursor.fetchall()]
            if "kullanici_id" not in sutunlar:
                for t in ("yiyecekler", "hedef", "kullanicilar"):
                    self.cursor.execute(f"DROP TABLE IF EXISTS {t}")
                self.baglanti.commit()

    def tablolari_olustur(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT    NOT NULL UNIQUE,
                sifre_hash    TEXT    NOT NULL
            );
            CREATE TABLE IF NOT EXISTS profil (
                kullanici_id INTEGER PRIMARY KEY,
                cinsiyet     TEXT    NOT NULL DEFAULT 'erkek',
                yas          INTEGER NOT NULL DEFAULT 25,
                boy          REAL    NOT NULL DEFAULT 170,
                kilo         REAL    NOT NULL DEFAULT 70,
                aktivite     TEXT    NOT NULL DEFAULT 'orta',
                tema         TEXT    NOT NULL DEFAULT 'koyu',
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
            );
            CREATE TABLE IF NOT EXISTS hedef (
                kullanici_id INTEGER PRIMARY KEY,
                gunluk_kcal  INTEGER NOT NULL DEFAULT 2000,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
            );
            CREATE TABLE IF NOT EXISTS yiyecekler (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                isim         TEXT    NOT NULL,
                kalori       INTEGER NOT NULL,
                tarih        TEXT    NOT NULL,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
            );
        """)
        self.baglanti.commit()

    # ── Kullanıcı ──
    @staticmethod
    def _hash(sifre):
        return hashlib.sha256(sifre.encode()).hexdigest()

    def kullanici_kayit(self, kullanici_adi, sifre):
        try:
            self.cursor.execute(
                "INSERT INTO kullanicilar (kullanici_adi, sifre_hash) VALUES (?,?)",
                (kullanici_adi, self._hash(sifre))
            )
            self.baglanti.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def kullanici_giris(self, kullanici_adi, sifre):
        self.cursor.execute(
            "SELECT id FROM kullanicilar WHERE kullanici_adi=? AND sifre_hash=?",
            (kullanici_adi, self._hash(sifre))
        )
        r = self.cursor.fetchone()
        return r[0] if r else None

    def sifre_degistir(self, kullanici_id, eski_sifre, yeni_sifre):
        self.cursor.execute(
            "SELECT id FROM kullanicilar WHERE id=? AND sifre_hash=?",
            (kullanici_id, self._hash(eski_sifre))
        )
        if not self.cursor.fetchone():
            return False
        self.cursor.execute(
            "UPDATE kullanicilar SET sifre_hash=? WHERE id=?",
            (self._hash(yeni_sifre), kullanici_id)
        )
        self.baglanti.commit()
        return True

    # ── Profil ──
    def profil_getir(self, kullanici_id):
        self.cursor.execute(
            "SELECT cinsiyet,yas,boy,kilo,aktivite,tema FROM profil WHERE kullanici_id=?",
            (kullanici_id,)
        )
        r = self.cursor.fetchone()
        if r:
            return {"cinsiyet": r[0], "yas": r[1], "boy": r[2],
                    "kilo": r[3], "aktivite": r[4], "tema": r[5]}
        return {"cinsiyet": "erkek", "yas": 25, "boy": 170.0,
                "kilo": 70.0, "aktivite": "orta", "tema": "koyu"}

    def profil_kaydet(self, kullanici_id, cinsiyet, yas, boy, kilo, aktivite, tema):
        self.cursor.execute("""
            INSERT OR REPLACE INTO profil
            (kullanici_id,cinsiyet,yas,boy,kilo,aktivite,tema)
            VALUES (?,?,?,?,?,?,?)
        """, (kullanici_id, cinsiyet, yas, boy, kilo, aktivite, tema))
        self.baglanti.commit()

    # ── Hedef ──
    def hedef_getir(self, kullanici_id):
        self.cursor.execute(
            "SELECT gunluk_kcal FROM hedef WHERE kullanici_id=?", (kullanici_id,)
        )
        r = self.cursor.fetchone()
        if r:
            return r[0]
        self.cursor.execute(
            "INSERT INTO hedef (kullanici_id,gunluk_kcal) VALUES (?,2000)", (kullanici_id,)
        )
        self.baglanti.commit()
        return 2000

    def hedef_guncelle(self, kullanici_id, yeni_hedef):
        self.cursor.execute(
            "INSERT OR REPLACE INTO hedef (kullanici_id,gunluk_kcal) VALUES (?,?)",
            (kullanici_id, yeni_hedef)
        )
        self.baglanti.commit()

    # ── Yiyecek ──
    def yiyecek_ekle(self, kullanici_id, isim, kalori, tarih):
        self.cursor.execute(
            "INSERT INTO yiyecekler (kullanici_id,isim,kalori,tarih) VALUES (?,?,?,?)",
            (kullanici_id, isim, kalori, tarih)
        )
        self.baglanti.commit()
        return self.cursor.lastrowid

    def yiyecek_sil(self, kayit_id):
        self.cursor.execute("DELETE FROM yiyecekler WHERE id=?", (kayit_id,))
        self.baglanti.commit()

    def gun_kayitlari(self, kullanici_id, tarih):
        self.cursor.execute(
            "SELECT id,isim,kalori FROM yiyecekler WHERE kullanici_id=? AND tarih=? ORDER BY id",
            (kullanici_id, tarih)
        )
        return self.cursor.fetchall()

    def baglanti_kapat(self):
        self.baglanti.close()


# ══════════════════════════════════════════════════════
#  BMR HESAPLAMA YARDIMCISI
# ══════════════════════════════════════════════════════
AKTIVITE_KATSAYI = {
    "hareketsiz":  1.2,
    "hafif":       1.375,
    "orta":        1.55,
    "aktif":       1.725,
    "cok_aktif":   1.9,
}

def bmr_hesapla(cinsiyet, yas, boy, kilo, aktivite):
    """Mifflin-St Jeor formülü → TDEE döndürür."""
    if cinsiyet == "erkek":
        bmr = 10 * kilo + 6.25 * boy - 5 * yas + 5
    else:
        bmr = 10 * kilo + 6.25 * boy - 5 * yas - 161
    return round(bmr * AKTIVITE_KATSAYI.get(aktivite, 1.55))


# ══════════════════════════════════════════════════════
#  GİRİŞ SAYFASI
# ══════════════════════════════════════════════════════
class GirisSayfasi(QWidget):
    def __init__(self, db, giris_cb):
        super().__init__()
        self.db = db
        self.giris_cb = giris_cb
        self._olustur()

    def _olustur(self):
        ana = QVBoxLayout(self)
        ana.setAlignment(Qt.AlignCenter)
        ana.setContentsMargins(0, 0, 0, 0)

        kart = QFrame()
        kart.setStyleSheet(f"""
            QFrame {{
                background-color: {R('bg_kart')};
                border: 1px solid {R('sinir')};
                border-radius: 20px;
            }}
        """)
        kart.setFixedWidth(380)
        kl = QVBoxLayout(kart)
        kl.setSpacing(12)
        kl.setContentsMargins(36, 32, 36, 32)

        # Logo
        ikon = QLabel("🥗")
        ikon.setAlignment(Qt.AlignCenter)
        ikon.setFont(QFont("Segoe UI Emoji", 36))
        kl.addWidget(ikon)

        baslik = QLabel("Kalori Takip")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet(
            f"color: {R('vurgu')}; font-size: 24px; font-weight: 800; letter-spacing: 1px;"
        )
        kl.addWidget(baslik)

        alt = QLabel("Sağlıklı yaşam, bilinçli beslenme")
        alt.setAlignment(Qt.AlignCenter)
        alt.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; margin-bottom: 6px;")
        kl.addWidget(alt)

        # Sekmeler
        sekme_cerceve = QFrame()
        sekme_cerceve.setStyleSheet(
            f"background-color: {R('bg_kart2')}; border-radius: 10px; border: none;"
        )
        sl = QHBoxLayout(sekme_cerceve)
        sl.setContentsMargins(4, 4, 4, 4)
        sl.setSpacing(4)

        self.giris_tab = QPushButton("Giriş Yap")
        self.kayit_tab = QPushButton("Kayıt Ol")
        for b in [self.giris_tab, self.kayit_tab]:
            b.setFixedHeight(32)
            b.setFont(QFont("Segoe UI", 10, QFont.Bold))
            b.setCursor(Qt.PointingHandCursor)
        sl.addWidget(self.giris_tab)
        sl.addWidget(self.kayit_tab)
        kl.addWidget(sekme_cerceve)

        self._aktif = "giris"

        # Alanlar
        for lbl_text, attr, ph, gizli in [
            ("Kullanıcı Adı", "kullanici_edit", "kullanıcı adınızı girin", False),
            ("Şifre",         "sifre_edit",     "şifrenizi girin",         True),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; font-weight: 600;")
            kl.addWidget(lbl)
            edit = QLineEdit()
            edit.setPlaceholderText(ph)
            edit.setFixedHeight(40)
            edit.setStyleSheet(giris_stil())
            if gizli:
                edit.setEchoMode(QLineEdit.Password)
                edit.returnPressed.connect(self._islem)
            setattr(self, attr, edit)
            kl.addWidget(edit)

        self.hata = QLabel("")
        self.hata.setAlignment(Qt.AlignCenter)
        self.hata.setStyleSheet(f"color: {R('tehlike')}; font-size: 11px; min-height: 16px;")
        kl.addWidget(self.hata)

        self.islem_btn = QPushButton("Giriş Yap")
        self.islem_btn.setFixedHeight(42)
        self.islem_btn.setCursor(Qt.PointingHandCursor)
        self.islem_btn.setStyleSheet(yesil_btn(13))
        self.islem_btn.clicked.connect(self._islem)
        kl.addWidget(self.islem_btn)

        # Bağlantılar
        self.giris_tab.clicked.connect(lambda: self._sekme("giris"))
        self.kayit_tab.clicked.connect(lambda: self._sekme("kayit"))
        self._sekme_guncelle()

        ana.addWidget(kart, alignment=Qt.AlignCenter)

    def _sekme(self, ad):
        self._aktif = ad
        self._sekme_guncelle()
        self.hata.setText("")

    def _sekme_guncelle(self):
        ak = (f"QPushButton {{ background-color: {R('vurgu')}; color: #0f1923; "
              f"border-radius: 8px; font-size: 10px; font-weight: 700; border: none; }}")
        pa = (f"QPushButton {{ background-color: transparent; color: {R('metin_soluk')}; "
              f"border-radius: 8px; font-size: 10px; font-weight: 600; border: none; }}"
              f"QPushButton:hover {{ color: {R('metin')}; }}")
        if self._aktif == "giris":
            self.giris_tab.setStyleSheet(ak)
            self.kayit_tab.setStyleSheet(pa)
            self.islem_btn.setText("Giriş Yap")
        else:
            self.giris_tab.setStyleSheet(pa)
            self.kayit_tab.setStyleSheet(ak)
            self.islem_btn.setText("Kayıt Ol")

    def _islem(self):
        k = self.kullanici_edit.text().strip()
        s = self.sifre_edit.text()
        self.hata.setText("")
        if not k or not s:
            self.hata.setText("⚠  Tüm alanları doldurun.")
            return
        if self._aktif == "giris":
            uid = self.db.kullanici_giris(k, s)
            if uid:
                self.giris_cb(uid, k)
            else:
                self.hata.setText("⚠  Kullanıcı adı veya şifre hatalı.")
        else:
            if len(s) < 4:
                self.hata.setText("⚠  Şifre en az 4 karakter olmalı.")
                return
            uid = self.db.kullanici_kayit(k, s)
            if uid:
                self.giris_cb(uid, k)
            else:
                self.hata.setText("⚠  Bu kullanıcı adı zaten kullanılıyor.")


# ══════════════════════════════════════════════════════
#  PROFİL SAYFASI
# ══════════════════════════════════════════════════════
class ProfilSayfasi(QWidget):
    def __init__(self, db, kullanici_id, geri_cb, hedef_degisti_cb):
        super().__init__()
        self.db = db
        self.kid = kullanici_id
        self.geri_cb = geri_cb
        self.hedef_degisti_cb = hedef_degisti_cb
        self.profil = db.profil_getir(kullanici_id)
        self._olustur()

    def _olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        # Üst bar
        ust = QFrame()
        ust.setFixedHeight(52)
        ust.setStyleSheet(
            f"background-color: {R('bg_kart')}; border-bottom: 1px solid {R('sinir')};"
        )
        ul = QHBoxLayout(ust)
        ul.setContentsMargins(16, 0, 16, 0)

        geri = QPushButton("← Geri")
        geri.setFixedSize(80, 30)
        geri.setCursor(Qt.PointingHandCursor)
        geri.setStyleSheet(gri_btn(11))
        geri.clicked.connect(self.geri_cb)
        ul.addWidget(geri)

        baslik = QLabel("👤  Profil & Ayarlar")
        baslik.setStyleSheet(
            f"color: {R('metin')}; font-size: 15px; font-weight: 700;"
        )
        ul.addWidget(baslik, alignment=Qt.AlignCenter)
        ul.addStretch()
        ana.addWidget(ust)

        # Scroll alan
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        ic = QWidget()
        ic.setStyleSheet("background: transparent;")
        il = QVBoxLayout(ic)
        il.setSpacing(14)
        il.setContentsMargins(24, 20, 24, 20)

        # ── Vücut Bilgileri Kartı ──
        vucut = QGroupBox("📏  Vücut Bilgileri")
        vucut.setStyleSheet(kart_stil())
        vl = QVBoxLayout(vucut)
        vl.setSpacing(10)
        vl.setContentsMargins(14, 18, 14, 14)

        # Cinsiyet
        c_lbl = QLabel("Cinsiyet")
        c_lbl.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; font-weight: 600;")
        vl.addWidget(c_lbl)
        self.cinsiyet_combo = QComboBox()
        self.cinsiyet_combo.addItems(["Erkek", "Kadın"])
        self.cinsiyet_combo.setCurrentIndex(0 if self.profil["cinsiyet"] == "erkek" else 1)
        self.cinsiyet_combo.setFixedHeight(36)
        self.cinsiyet_combo.setStyleSheet(combo_stil())
        vl.addWidget(self.cinsiyet_combo)

        # Yaş / Boy / Kilo → yan yana
        say_layout = QHBoxLayout()
        say_layout.setSpacing(10)
        for lbl_t, attr, birim, val, mn, mx, tip in [
            ("Yaş",  "yas_spin",  "yıl",  self.profil["yas"],  10, 100, "int"),
            ("Boy",  "boy_spin",  "cm",   self.profil["boy"],  100, 250, "float"),
            ("Kilo", "kilo_spin", "kg",   self.profil["kilo"], 20, 300, "float"),
        ]:
            kutu = QWidget()
            kl2 = QVBoxLayout(kutu)
            kl2.setContentsMargins(0, 0, 0, 0)
            kl2.setSpacing(4)
            lb = QLabel(lbl_t)
            lb.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; font-weight: 600;")
            kl2.addWidget(lb)
            if tip == "int":
                sp = QSpinBox()
                sp.setRange(mn, mx)
                sp.setValue(int(val))
                sp.setSuffix(f" {birim}")
            else:
                sp = QDoubleSpinBox()
                sp.setRange(mn, mx)
                sp.setValue(float(val))
                sp.setSingleStep(0.5)
                sp.setSuffix(f" {birim}")
            sp.setFixedHeight(36)
            sp.setStyleSheet(spinbox_stil())
            setattr(self, attr, sp)
            kl2.addWidget(sp)
            say_layout.addWidget(kutu)
        vl.addLayout(say_layout)

        # Aktivite
        a_lbl = QLabel("Aktivite Seviyesi")
        a_lbl.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; font-weight: 600;")
        vl.addWidget(a_lbl)
        self.aktivite_combo = QComboBox()
        self.aktivite_combo.addItems([
            "Hareketsiz (masa başı, spor yok)",
            "Hafif aktif (haftada 1-3 gün)",
            "Orta aktif (haftada 3-5 gün)",
            "Aktif (haftada 6-7 gün)",
            "Çok aktif (günde 2x antrenman)",
        ])
        aktivite_map = {"hareketsiz": 0, "hafif": 1, "orta": 2, "aktif": 3, "cok_aktif": 4}
        self.aktivite_combo.setCurrentIndex(aktivite_map.get(self.profil["aktivite"], 2))
        self.aktivite_combo.setFixedHeight(36)
        self.aktivite_combo.setStyleSheet(combo_stil())
        vl.addWidget(self.aktivite_combo)

        # Öneri etiketi
        self.oneri_lbl = QLabel("")
        self.oneri_lbl.setAlignment(Qt.AlignCenter)
        self.oneri_lbl.setStyleSheet(
            f"background-color: {R('basarili_bg')}; color: {R('vurgu')}; "
            f"border-radius: 8px; font-size: 12px; font-weight: 600; padding: 8px;"
        )
        self.oneri_lbl.setVisible(False)
        vl.addWidget(self.oneri_lbl)

        # Hesapla & Uygula
        hesapla_btn = QPushButton("🔢  BMR Hesapla & Hedefe Uygula")
        hesapla_btn.setFixedHeight(40)
        hesapla_btn.setCursor(Qt.PointingHandCursor)
        hesapla_btn.setStyleSheet(yesil_btn(12))
        hesapla_btn.clicked.connect(self._hesapla)
        vl.addWidget(hesapla_btn)

        il.addWidget(vucut)

        # ── Tema Kartı ──
        tema_kart = QGroupBox("🎨  Tema")
        tema_kart.setStyleSheet(kart_stil())
        tl = QHBoxLayout(tema_kart)
        tl.setContentsMargins(14, 18, 14, 14)
        tl.setSpacing(12)

        self.koyu_btn = QPushButton("🌙  Koyu Tema")
        self.acik_btn = QPushButton("☀️  Açık Tema")
        for b in [self.koyu_btn, self.acik_btn]:
            b.setFixedHeight(38)
            b.setCursor(Qt.PointingHandCursor)
        self._tema_buton_guncelle()
        self.koyu_btn.clicked.connect(lambda: self._tema_degistir("koyu"))
        self.acik_btn.clicked.connect(lambda: self._tema_degistir("acik"))
        tl.addWidget(self.koyu_btn)
        tl.addWidget(self.acik_btn)
        il.addWidget(tema_kart)

        # ── Şifre Değiştirme Kartı ──
        sifre_kart = QGroupBox("🔒  Şifre Değiştir")
        sifre_kart.setStyleSheet(kart_stil())
        sl2 = QVBoxLayout(sifre_kart)
        sl2.setSpacing(8)
        sl2.setContentsMargins(14, 18, 14, 14)

        for lbl_t, attr, ph in [
            ("Mevcut Şifre",   "eski_sifre",  "mevcut şifrenizi girin"),
            ("Yeni Şifre",     "yeni_sifre",  "yeni şifrenizi girin"),
            ("Şifreyi Tekrar", "yeni_sifre2", "yeni şifrenizi tekrar girin"),
        ]:
            lb = QLabel(lbl_t)
            lb.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; font-weight: 600;")
            sl2.addWidget(lb)
            ed = QLineEdit()
            ed.setPlaceholderText(ph)
            ed.setEchoMode(QLineEdit.Password)
            ed.setFixedHeight(38)
            ed.setStyleSheet(giris_stil())
            setattr(self, attr, ed)
            sl2.addWidget(ed)

        self.sifre_msg = QLabel("")
        self.sifre_msg.setAlignment(Qt.AlignCenter)
        self.sifre_msg.setStyleSheet(f"font-size: 11px; min-height: 16px;")
        sl2.addWidget(self.sifre_msg)

        sifre_btn = QPushButton("🔑  Şifreyi Güncelle")
        sifre_btn.setFixedHeight(38)
        sifre_btn.setCursor(Qt.PointingHandCursor)
        sifre_btn.setStyleSheet(yesil_btn(12))
        sifre_btn.clicked.connect(self._sifre_degistir)
        sl2.addWidget(sifre_btn)
        il.addWidget(sifre_kart)

        il.addStretch()
        scroll.setWidget(ic)
        ana.addWidget(scroll)

    def _hesapla(self):
        cinsiyet_idx = self.cinsiyet_combo.currentIndex()
        cinsiyet = "erkek" if cinsiyet_idx == 0 else "kadin"
        yas    = self.yas_spin.value()
        boy    = self.boy_spin.value()
        kilo   = self.kilo_spin.value()
        aktivite_keys = ["hareketsiz", "hafif", "orta", "aktif", "cok_aktif"]
        aktivite = aktivite_keys[self.aktivite_combo.currentIndex()]

        tdee = bmr_hesapla(cinsiyet, yas, boy, kilo, aktivite)

        # Profili kaydet
        tema_mevcut = self.profil.get("tema", "koyu")
        self.db.profil_kaydet(self.kid, cinsiyet, yas, boy, kilo, aktivite, tema_mevcut)
        self.db.hedef_guncelle(self.kid, tdee)

        self.oneri_lbl.setText(f"✅  Günlük kalori hedefiniz {tdee} kcal olarak güncellendi!")
        self.oneri_lbl.setVisible(True)
        self.hedef_degisti_cb(tdee)

    def _tema_degistir(self, ad):
        tema_sec(ad)
        self.db.profil_kaydet(
            self.kid,
            "erkek" if self.cinsiyet_combo.currentIndex() == 0 else "kadin",
            self.yas_spin.value(),
            self.boy_spin.value(),
            self.kilo_spin.value(),
            ["hareketsiz","hafif","orta","aktif","cok_aktif"][self.aktivite_combo.currentIndex()],
            ad
        )
        # Ana pencereyi yeniden tema uygula
        app = QApplication.instance()
        if app:
            app.setStyleSheet(genel_stil())
        self.geri_cb(yenile=True)

    def _tema_buton_guncelle(self):
        aktif = _aktif_tema
        ak = (f"QPushButton {{ background-color: {R('vurgu')}; color: #0f1923; "
              f"border-radius: 10px; font-size: 12px; font-weight: 700; border: none; padding: 6px; }}")
        pa = gri_btn(12)
        self.koyu_btn.setStyleSheet(ak if aktif == "koyu" else pa)
        self.acik_btn.setStyleSheet(ak if aktif == "acik" else pa)

    def _sifre_degistir(self):
        eski  = self.eski_sifre.text()
        yeni  = self.yeni_sifre.text()
        yeni2 = self.yeni_sifre2.text()

        if not eski or not yeni or not yeni2:
            self._sifre_mesaj("⚠  Tüm alanları doldurun.", hata=True)
            return
        if yeni != yeni2:
            self._sifre_mesaj("⚠  Yeni şifreler eşleşmiyor.", hata=True)
            return
        if len(yeni) < 4:
            self._sifre_mesaj("⚠  Yeni şifre en az 4 karakter olmalı.", hata=True)
            return

        if self.db.sifre_degistir(self.kid, eski, yeni):
            self._sifre_mesaj("✅  Şifre başarıyla güncellendi.", hata=False)
            self.eski_sifre.clear()
            self.yeni_sifre.clear()
            self.yeni_sifre2.clear()
        else:
            self._sifre_mesaj("⚠  Mevcut şifre yanlış.", hata=True)

    def _sifre_mesaj(self, mesaj, hata):
        renk = R("tehlike") if hata else R("vurgu")
        self.sifre_msg.setStyleSheet(f"color: {renk}; font-size: 11px;")
        self.sifre_msg.setText(mesaj)


# ══════════════════════════════════════════════════════
#  ANA SAYFA
# ══════════════════════════════════════════════════════
class AnaSayfa(QWidget):
    def __init__(self, db, kullanici_id, kullanici_adi, cikis_cb, profil_cb):
        super().__init__()
        self.db = db
        self.kid = kullanici_id
        self.adi = kullanici_adi
        self.cikis_cb = cikis_cb
        self.profil_cb = profil_cb
        self.bugun = str(date.today())
        self.yiyecekler = []
        self.gunluk_hedef = self.db.hedef_getir(kullanici_id)
        self._olustur()
        self.kayitlari_yukle()

    def _olustur(self):
        ana = QVBoxLayout(self)
        ana.setSpacing(0)
        ana.setContentsMargins(0, 0, 0, 0)

        # ── Üst bar ──
        ust = QFrame()
        ust.setFixedHeight(54)
        ust.setStyleSheet(
            f"background-color: {R('bg_kart')}; border-bottom: 1px solid {R('sinir')};"
        )
        ul = QHBoxLayout(ust)
        ul.setContentsMargins(18, 0, 14, 0)
        ul.setSpacing(8)

        logo = QLabel("🥗  Kalori Takip")
        logo.setStyleSheet(
            f"color: {R('vurgu')}; font-size: 15px; font-weight: 800; letter-spacing: 1px;"
        )
        ul.addWidget(logo)
        ul.addStretch()

        tarih = QLabel(f"📅  {self.bugun}")
        tarih.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px;")
        ul.addWidget(tarih)

        ul.addSpacing(12)

        kullanici = QLabel(f"👤  {self.adi}")
        kullanici.setStyleSheet(f"color: {R('metin')}; font-size: 12px; font-weight: 600;")
        ul.addWidget(kullanici)

        ul.addSpacing(6)

        profil_btn = QPushButton("⚙  Profil")
        profil_btn.setFixedSize(76, 28)
        profil_btn.setCursor(Qt.PointingHandCursor)
        profil_btn.setStyleSheet(gri_btn(11))
        profil_btn.clicked.connect(self.profil_cb)
        ul.addWidget(profil_btn)

        cikis_btn = QPushButton("Çıkış")
        cikis_btn.setFixedSize(64, 28)
        cikis_btn.setCursor(Qt.PointingHandCursor)
        cikis_btn.setStyleSheet(kirmizi_btn(11))
        cikis_btn.clicked.connect(self.cikis_cb)
        ul.addWidget(cikis_btn)

        ana.addWidget(ust)

        # ── İçerik ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        ic = QWidget()
        ic.setStyleSheet("background: transparent;")
        il = QVBoxLayout(ic)
        il.setSpacing(14)
        il.setContentsMargins(24, 18, 24, 18)

        self._ozet_kart(il)

        alt = QHBoxLayout()
        alt.setSpacing(14)
        self._form_kart(alt)
        self._liste_kart(alt)
        il.addLayout(alt)

        self.durum_lbl = QLabel("")
        self.durum_lbl.setAlignment(Qt.AlignCenter)
        self.durum_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.durum_lbl.setFixedHeight(40)
        self.durum_lbl.setStyleSheet("border-radius: 10px;")
        il.addWidget(self.durum_lbl)

        il.addStretch()
        scroll.setWidget(ic)
        ana.addWidget(scroll)

    def _ozet_kart(self, layout):
        kart = QFrame()
        kart.setStyleSheet(
            f"background-color: {R('bg_kart')}; border: 1px solid {R('sinir')}; border-radius: 16px;"
        )
        kl = QVBoxLayout(kart)
        kl.setContentsMargins(20, 14, 20, 14)
        kl.setSpacing(8)

        ust = QHBoxLayout()
        baslik = QLabel("Günlük Özet")
        baslik.setStyleSheet(f"color: {R('metin')}; font-size: 14px; font-weight: 700;")
        ust.addWidget(baslik)
        ust.addStretch()

        h_lbl = QLabel("Hedef:")
        h_lbl.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 12px;")
        ust.addWidget(h_lbl)

        self.hedef_spin = QSpinBox()
        self.hedef_spin.setRange(500, 6000)
        self.hedef_spin.setValue(self.gunluk_hedef)
        self.hedef_spin.setSingleStep(50)
        self.hedef_spin.setFixedSize(120, 28)
        self.hedef_spin.setStyleSheet(spinbox_stil())
        self.hedef_spin.setSuffix(" kcal")
        self.hedef_spin.valueChanged.connect(self._hedef_degisti)
        ust.addWidget(self.hedef_spin)
        kl.addLayout(ust)

        self.ilerleme_lbl = QLabel(f"0 / {self.gunluk_hedef} kcal alındı")
        self.ilerleme_lbl.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 12px;")
        kl.addWidget(self.ilerleme_lbl)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFixedHeight(12)
        self.progress.setTextVisible(False)
        self._prog_yesil()
        kl.addWidget(self.progress)

        layout.addWidget(kart)

    def _form_kart(self, layout):
        kart = QGroupBox("➕  Yiyecek Ekle")
        kart.setStyleSheet(kart_stil())
        kart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        kl = QVBoxLayout(kart)
        kl.setSpacing(8)
        kl.setContentsMargins(14, 18, 14, 14)

        for lbl_t, attr, ph in [
            ("Yiyecek Adı", "isim_edit",   "Örn: Elma, Pilav, Tavuk..."),
            ("Kalori (kcal)", "kalori_edit", "Örn: 150"),
        ]:
            lb = QLabel(lbl_t)
            lb.setStyleSheet(f"color: {R('metin_soluk')}; font-size: 11px; font-weight: 600;")
            kl.addWidget(lb)
            ed = QLineEdit()
            ed.setPlaceholderText(ph)
            ed.setFixedHeight(36)
            ed.setStyleSheet(giris_stil())
            setattr(self, attr, ed)
            kl.addWidget(ed)

        self.kalori_edit.returnPressed.connect(self._ekle)

        btn = QPushButton("Ekle  ➕")
        btn.setFixedHeight(38)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(yesil_btn(12))
        btn.clicked.connect(self._ekle)
        kl.addWidget(btn)

        layout.addWidget(kart)

    def _liste_kart(self, layout):
        kart = QGroupBox("🍽  Bugün Yediklerim")
        kart.setStyleSheet(kart_stil())
        kart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        kl = QVBoxLayout(kart)
        kl.setSpacing(8)
        kl.setContentsMargins(14, 18, 14, 14)

        self.liste = QListWidget()
        self.liste.setStyleSheet(liste_stil())
        self.liste.setMinimumHeight(180)
        kl.addWidget(self.liste)

        sil = QPushButton("🗑  Seçili Öğeyi Sil")
        sil.setFixedHeight(36)
        sil.setCursor(Qt.PointingHandCursor)
        sil.setStyleSheet(kirmizi_btn(12))
        sil.clicked.connect(self._sil)
        kl.addWidget(sil)

        layout.addWidget(kart)

    # ── Mantık ──
    def kayitlari_yukle(self):
        self.yiyecekler.clear()
        self.liste.clear()
        for rid, isim, kal in self.db.gun_kayitlari(self.kid, self.bugun):
            self.yiyecekler.append((rid, isim, kal))
            self.liste.addItem(QListWidgetItem(f"  {isim}  —  {kal} kcal"))
        self._guncelle()

    def hedef_disaridan_guncelle(self, yeni):
        self.gunluk_hedef = yeni
        self.hedef_spin.setValue(yeni)
        self._guncelle()

    def _ekle(self):
        isim = self.isim_edit.text().strip()
        kal_str = self.kalori_edit.text().strip()
        if not isim:
            QMessageBox.warning(self, "Hata", "Lütfen yiyecek adı girin!")
            return
        try:
            kal = int(kal_str)
            if kal <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Hata", "Kalori pozitif bir tam sayı olmalıdır!")
            return
        rid = self.db.yiyecek_ekle(self.kid, isim, kal, self.bugun)
        self.yiyecekler.append((rid, isim, kal))
        self.liste.addItem(QListWidgetItem(f"  {isim}  —  {kal} kcal"))
        self.isim_edit.clear()
        self.kalori_edit.clear()
        self.isim_edit.setFocus()
        self._guncelle()

    def _sil(self):
        row = self.liste.currentRow()
        if row < 0:
            QMessageBox.information(self, "Bilgi", "Silmek için bir öğe seçin.")
            return
        self.db.yiyecek_sil(self.yiyecekler[row][0])
        self.liste.takeItem(row)
        del self.yiyecekler[row]
        self._guncelle()

    def _hedef_degisti(self):
        self.gunluk_hedef = self.hedef_spin.value()
        self.db.hedef_guncelle(self.kid, self.gunluk_hedef)
        self._guncelle()

    def _guncelle(self):
        toplam = sum(k for _, _, k in self.yiyecekler)
        hedef  = self.gunluk_hedef
        self.ilerleme_lbl.setText(f"{toplam} / {hedef} kcal alındı")
        yuzde = min(int(toplam / hedef * 100), 100) if hedef > 0 else 0
        self.progress.setValue(yuzde)

        if toplam == 0:
            self.durum_lbl.setText("")
            self.durum_lbl.setStyleSheet("")
            self._prog_yesil()
        elif toplam > hedef:
            self.durum_lbl.setText(f"  ⚠  Günlük hedefi {toplam - hedef} kcal aştınız!")
            self.durum_lbl.setStyleSheet(
                f"background-color: {R('hata_bg')}; color: {R('tehlike')}; border-radius: 10px;"
            )
            self._prog_kirmizi()
        else:
            self.durum_lbl.setText(f"  ✅  Harika! Kalan: {hedef - toplam} kcal")
            self.durum_lbl.setStyleSheet(
                f"background-color: {R('basarili_bg')}; color: {R('vurgu')}; border-radius: 10px;"
            )
            self._prog_yesil()

    def _prog_yesil(self):
        self.progress.setStyleSheet(
            f"QProgressBar {{ border: none; border-radius: 6px; background: {R('sinir')}; }}"
            f"QProgressBar::chunk {{ border-radius: 6px; background-color: {R('vurgu')}; }}"
        )

    def _prog_kirmizi(self):
        self.progress.setStyleSheet(
            f"QProgressBar {{ border: none; border-radius: 6px; background: {R('sinir')}; }}"
            f"QProgressBar::chunk {{ border-radius: 6px; background-color: {R('tehlike')}; }}"
        )


# ══════════════════════════════════════════════════════
#  ANA PENCERE
# ══════════════════════════════════════════════════════
class KaloriTakipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalori Takip")
        self.setMinimumSize(540, 480)
        self.resize(900, 620)

        self.db = Veritabani()
        self._aktif_kullanici = None   # (id, adi)
        self._ana_sayfa_ref   = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self._giris_goster()

    def _uygula_tema(self):
        self.setStyleSheet(genel_stil())

    # ── Sayfa geçişleri ──
    def _giris_goster(self):
        QTimer.singleShot(0, self._giris_goster_impl)

    def _giris_goster_impl(self):
        self._stack_temizle()
        tema_sec("koyu")          # Giriş sayfası her zaman koyu
        self._uygula_tema()
        w = GirisSayfasi(self.db, self._giris_basarili)
        self.stack.addWidget(w)
        self.stack.setCurrentWidget(w)

    def _giris_basarili(self, uid, adi):
        self._aktif_kullanici = (uid, adi)
        # Kayıtlı temayı yükle
        profil = self.db.profil_getir(uid)
        tema_sec(profil.get("tema", "koyu"))
        QTimer.singleShot(0, self._ana_goster_impl)

    def _ana_goster_impl(self):
        if not self._aktif_kullanici:
            return
        uid, adi = self._aktif_kullanici
        self._stack_temizle()
        self._uygula_tema()
        w = AnaSayfa(
            self.db, uid, adi,
            cikis_cb=self._giris_goster,
            profil_cb=self._profil_goster,
        )
        self._ana_sayfa_ref = w
        self.stack.addWidget(w)
        self.stack.setCurrentWidget(w)

    def _profil_goster(self):
        if not self._aktif_kullanici:
            return
        uid, adi = self._aktif_kullanici
        w = ProfilSayfasi(
            self.db, uid,
            geri_cb=self._profil_geri,
            hedef_degisti_cb=self._hedef_disaridan,
        )
        self.stack.addWidget(w)
        self.stack.setCurrentWidget(w)

    def _profil_geri(self, yenile=False):
        # Profil sayfasını kaldır (son eklenen)
        if self.stack.count() > 1:
            w = self.stack.widget(self.stack.count() - 1)
            self.stack.removeWidget(w)
            w.deleteLater()
        if yenile:
            # Tema değişmiş olabilir, ana sayfayı yeniden oluştur
            QTimer.singleShot(0, self._ana_goster_impl)
        else:
            self._uygula_tema()

    def _hedef_disaridan(self, yeni_hedef):
        if self._ana_sayfa_ref:
            self._ana_sayfa_ref.hedef_disaridan_guncelle(yeni_hedef)

    def _stack_temizle(self):
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()
        self._ana_sayfa_ref = None

    def closeEvent(self, event):
        self.db.baglanti_kapat()
        event.accept()


# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    p = QPalette()
    bg = QColor("#0f1923")
    p.setColor(QPalette.Window,          bg)
    p.setColor(QPalette.WindowText,      QColor("#e8f0fe"))
    p.setColor(QPalette.Base,            QColor("#1a2535"))
    p.setColor(QPalette.Text,            QColor("#e8f0fe"))
    p.setColor(QPalette.Button,          QColor("#1a2535"))
    p.setColor(QPalette.ButtonText,      QColor("#e8f0fe"))
    p.setColor(QPalette.Highlight,       QColor("#00d4a0"))
    p.setColor(QPalette.HighlightedText, QColor("#0f1923"))
    app.setPalette(p)

    pencere = KaloriTakipApp()
    pencere.show()
    sys.exit(app.exec_())