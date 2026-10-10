# 🧮 MathPractice - Panduan Penggunaan (Manual Book)

**MathPractice** adalah aplikasi interaktif berbasis Python & Kivy yang dirancang untuk membantu anak-anak dan siswa melatih serta meningkatkan kemampuan berhitung matematika dasar hingga tingkat menengah secara menyenangkan.

---

## 📋 Daftar Isi
1. [Fitur Utama](#-fitur-utama)
2. [Persyaratan Sistem & Instalasi](#-persyaratan-sistem--instalasi)
3. [Cara Menjalankan Aplikasi](#-cara-menjalankan-aplikasi)
4. [Panduan Penggunaan Aplikasi](#-panduan-penggunaan-aplikasi)
   - [1. Halaman Login](#1-halaman-login)
   - [2. Halaman Utama (Home)](#2-halaman-utama-home)
   - [3. Pemilihan Operasi Matematika](#3-pemilihan-operasi-matematika)
   - [4. Pemilihan Tingkat Kesulitan (Level)](#4-pemilihan-tingkat-kesulitan-level)
   - [5. Pengerjaan Kuis](#5-pengerjaan-kuis)
   - [6. Halaman Hasil & Selebrasi](#6-halaman-hasil--selebrasi)
   - [7. Riwayat Skor](#7-riwayat-skor)
5. [Struktur Database & Penyimpanan](#-struktur-database--penyimpanan)
6. [Struktur Proyek](#-struktur-proyek)

---

## ✨ Fitur Utama

- **6 Operasi Matematika Lengkap:**
  - ➕ Pertambahan
  - ➖ Pengurangan
  - ✖️ Perkalian
  - ➗ Pembagian
  - 🔢 Perpangkatan ($x^2$ dan $x^3$)
  - 📐 Akar Kuadrat ($\sqrt{x}$) & Akar Kubik ($\sqrt[3]{x}$)
- **Sistem Level Kesulitan Adaptif:**
  - Operasi Dasar: Level A (Mudah: 1–9), Level B (Sedang: 10–50), Level C (Tantangan: 60–100).
  - Pangkat & Akar: Pangkat/Akar Kuadrat & Kubik.
- **Riwayat Skor Lokal (SQLite):** Menyimpan riwayat latihan beserta nama pengguna, skor, jenis operasi, dan tingkat kesulitan. Fitur tekan lama (*long press*) untuk menghapus riwayat.
- **Audio & Efek Partikel Selebrasi:** Efek suara kemenangan sintetis (WAV) dan animasi *confetti* jika berhasil mencapai skor $\ge 80$.
- **Desain Responsif & Ceria:** Antarmuka modern dengan warna yang menarik bagi anak-anak.

---

## 💻 Persyaratan Sistem & Instalasi

### Prasyarat
- **Python:** Versi 3.8 atau lebih baru.
- **Sistem Operasi:** Windows / macOS / Linux.

### Instalasi Dependensi
Buka terminal/command prompt, lalu install pustaka **Kivy** dengan perintah berikut:

```bash
pip install kivy
```

*(Catatan: Aplikasi ini menggunakan modul standar Python seperti `sqlite3`, `wave`, `struct`, dan `math`, sehingga tidak membutuhkan dependensi external tambahan selain Kivy).*

---

## 🚀 Cara Menjalankan Aplikasi

1. Pastikan kedua file utama diletakkan dalam satu direktori yang sama:
   - `main.py` (Logika backend dan GUI)
   - `mathpractice.kv` (Desain antarmuka/layout)
2. Jalankan perintah berikut melalui terminal/command prompt:

```bash
python main.py
```

### Membuat Aplikasi Android (APK)

Proyek ini dikonfigurasi untuk dibuild langsung di GitHub Codespaces. Tidak perlu memasang Ubuntu, Linux, WSL, atau VM terpisah.

1. Buka repository ini di Codespaces. Jika Codespaces meminta rebuild container setelah perubahan konfigurasi, pilih **Rebuild Container**.
2. Di terminal Codespaces, jalankan setup satu kali untuk memasang paket build Android:

```bash
bash .devcontainer/setup-android.sh
```

3. Bangun APK debug:

```bash
bash scripts/build_android.sh
```

Build pertama kali mengunduh Android SDK/NDK dan mengompilasi Kivy serta library native. Prosesnya dapat berlangsung lama. Setelah sukses, APK tersedia di `bin/` dan dapat diunduh dari Explorer Codespaces, lalu dipindahkan ke ponsel Android untuk dipasang.

Build versi 0.4 menggunakan application ID `id.gabriela.mathpracticeapp` dan hanya menyertakan ABI `arm64-v8a`, sesuai target OPPO CPH2185. Label aplikasi tetap **MathPractice**. Buka APK yang baru diunduh melalui aplikasi **Files** Android dan izinkan pemasangan dari sumber tersebut bila diminta.

Jika installer menampilkan **App not installed** pada APK versi 0.4, pastikan nama file berakhir `-0.4-arm64-v8a-debug.apk`. Jika aplikasi sudah terpasang tetapi langsung menutup setelah splash screen, sambungkan perangkat ke komputer dengan Android Debug Bridge (ADB), lalu ambil error runtime:

```bash
adb logcat -c
adb shell monkey -p id.gabriela.mathpracticeapp 1
adb logcat -d -v brief AndroidRuntime:E python:E PythonActivity:E '*:S'
```

Kirim baris `FATAL EXCEPTION`, `Traceback`, atau `ImportError` yang muncul untuk diagnosis lanjutan. Tidak perlu menghapus folder build atau mengulang setup paket untuk mengambil log.

---

## 📖 Panduan Penggunaan Aplikasi

### 1. Halaman Login
- Saat pertama kali membuka aplikasi, Anda akan disambut oleh halaman **MATH FUN**.
- Ketikkan nama atau nama panggilan Anda pada kolom *"Ketik Nama Kamu..."*.
- Tekan tombol **MULAI MAIN** atau tekan tombol `Enter` pada keyboard.

### 2. Halaman Utama (Home)
Setelah masuk, Anda akan diarahkan ke Menu Utama. Tersedia 3 opsi:
- **PILIH GAME:** Melanjutkan ke menu pemilihan operasi matematika.
- **RIWAYAT SKOR:** Melihat rekam jejak hasil kuis yang telah dikerjakan sebelumnya.
- **Keluar:** Kembali ke halaman Login untuk mengganti pengguna.

### 3. Pemilihan Operasi Matematika
Pilih salah satu dari 6 mode perhitungan yang ingin dilatih:
1. **Perkalian** ($\times$)
2. **Pembagian** ($\div$)
3. **Pertambahan** ($+$)
4. **Pengurangan** ($-$)
5. **Perpangkatan** ($x^2 / x^3$)
6. **Akar** ($\sqrt{} / \sqrt[3]{}$)

### 4. Pemilihan Tingkat Kesulitan (Level)
Setiap operasi menyediakan pilihan tingkat sesuai kebutuhan:
- **Operasi Dasar (+, −, ×, ÷):**
  - **Level A (Mudah):** Rentang angka 1 – 9.
  - **Level B (Sedang):** Rentang angka 10 – 50.
  - **Level C (Tantangan):** Rentang angka 60 – 100.
- **Perpangkatan & Akar:**
  - **Pangkat 2 / Akar Kuadrat ($\sqrt{}$)**
  - **Pangkat 3 / Akar Kubik ($\sqrt[3]{}$)**

### 5. Pengerjaan Kuis
- **Jumlah Soal:** Setiap sesi kuis terdiri dari **10 soal acak**.
- **Sistem Skor:** Setiap jawaban benar mendapat nilai **+10 point** (Maksimal skor = 100).
- **Cara Menjawab:**
  1. Masukkan angka jawaban pada kolom input di tengah layar.
  2. Tekan tombol **JAWAB** atau tekan `Enter`.
  3. Aplikasi akan memberikan umpan balik (*Benar* / *Kurang tepat*).
  4. Soal berikutnya akan otomatis muncul secara bergantian.
- Tekan tombol **Batal** di sudut kanan atas jika ingin membatalkan kuis dan kembali ke menu operasi.

### 6. Halaman Hasil & Selebrasi
Setelah menyelesaikan 10 soal:
- Skor akhir Anda akan ditampilkan.
- **Pesan Apresiasi:**
  - Skor **100**: *SEMPURNA! Kamu Genius Matematika!*
  - Skor **80 – 90**: *HEBAT! Sedikit lagi dapat nilai sempurna!*
  - Skor **60 – 70**: *KERJA BAGUS! Terus berlatih ya!*
  - Skor **< 60**: *JANGAN MENYERAH! Coba lagi yuk!*
- **Selebrasi:** Jika skor $\ge 80$, efek suara arpeggio ceria dan animasi *confetti* partikel warna-warni akan aktif.
- Pilihan navigasi: **COBA LAGI** (mengulang kuis) atau **MENU UTAMA**.

### 7. Riwayat Skor
- Menampilkan daftar 50 riwayat pengerjaan kuis terakhir (Nama, Skor, Jenis Operasi).
- **Hapus Riwayat:** Tekan dan tahan (*long press* / tahan klik mouse selama 0.7 detik) pada baris riwayat yang ingin dihapus, lalu konfirmasi opsi hapus pada popup yang muncul.

---

## 🗄️ Struktur Database & Penyimpanan

Aplikasi menggunakan database bawaan **SQLite3** bernama `history.db` yang dibuat di direktori data privat aplikasi saat pertama kali dijalankan. Direktori privat ini dapat ditulis oleh aplikasi Android dan riwayat tetap tersimpan di antara sesi.

**Tabel `quiz_history`:**
| Kolom | Tipe Data | Keterangan |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto Increment) |
| `username` | TEXT | Nama pemain |
| `score` | INTEGER | Skor akhir (0 – 100) |
| `operation` | TEXT | Operasi matematika yang dipilih |
| `level` | TEXT | Tingkat kesulitan |
| `timestamp` | DATETIME | Waktu pengerjaan kuis |

---

## 📁 Struktur Proyek

```text
mathpractice/
├── main.py          # File utama kode Python (Logika & Database)
├── mathpractice.kv  # File konfigurasi desain UI Kivy
└── history.db       # Database SQLite (dibuat otomatis di direktori data aplikasi)
```