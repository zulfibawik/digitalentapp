# digitalentappython

Latihan proyek Python dan Data Science.

Sesuai `CLAUDE.md`, stack ini adalah **Python 3 + MySQL** di dalam Docker Compose. Fokus utama
fitur adalah **membuka terminal di dalam container Docker** dan melakukan operasi data
pada tabel `statistik`.

---

## Stack

| Komponen | Versi   | Keterangan                          |
| -------- | ------- | ----------------------------------- |
| Python   | 3.11    | `python:3.11-slim`                  |
| MySQL    | 8.4     | `mysql:8.4`                         |
| Docker   | 28+     | Docker Desktop / Docker Engine      |
| Compose  | v2      | `docker compose` (bukan `docker-compose`) |
| Tools    | -       | `nano`, `default-mysql-client`, `curl` |

Tidak ada web server / nginx di stack ini karena fokus utama adalah terminal di container.

---

## Struktur Folder

```
digitalentappython/
├── CLAUDE.md                  # Instruksi proyek
├── Dockerfile                 # Image Python 3.11 + tools
├── docker-compose.yml         # 2 service: python + db
├── requirements.txt           # mysql-connector-python
├── .env.example               # Template env
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py              # Baca env var
│   ├── db.py                  # Helper koneksi MySQL
│   └── statistik.py           # Script CLI bengkel sederhana
├── sql/
│   └── init_statistik.sql     # CREATE TABLE + sample data
└── README.md                  # File ini
```

---

## Port

Stack ini menggunakan port host yang **tidak bentrok** dengan stack lain di mesin ini:

| Service | Host Port     | Container Port | Keterangan           |
| ------- | ------------- | -------------- | -------------------- |
| MySQL   | `127.0.0.1:3311` | `3306`         | Akses dari host      |

Tidak ada port web — aplikasi dijalankan lewat terminal di dalam container.

---

## Cara Menjalankan

### 1. Build & jalankan container

```bash
cd /Users/zhulfibajra/Documents/Aplikasi/digitalentappython
docker compose build
docker compose up -d
```

Tunggu beberapa detik sampai MySQL selesai inisialisasi (healthcheck pass).

### 2. Masuk terminal di dalam container Python

```bash
docker compose exec python bash
```

Sesuai CLAUDE.md ("hanya membuka terminal di dalam container docker"), semua
pekerjaan dilakukan dari dalam container ini.

### 3. (Opsional) Tes koneksi MySQL dari dalam container

```bash
mysql -h db -u digitalenta -pdigitalenta_pass digitalenta_db -e "SELECT * FROM statistik;"
```

### 4. Jalankan aplikasi latihan

```bash
cd /workspace
python app/statistik.py
```

Akan muncul menu:

```
Menu:
  1) Lihat semua data
  2) Tambah data
  3) Ringkasan per kategori
  0) Keluar
Pilih [0-3]:
```

---

## Tabel `statistik`

TABEL normal sederhana (sesuai CLAUDE.md aturan database):

| Kolom     | Tipe           | Keterangan                  |
| --------- | -------------- | --------------------------- |
| `id`      | INT PK AI      | Primary key auto increment  |
| `kategori`| VARCHAR(50)    | Nama kategori               |
| `nilai`   | DECIMAL(10,2)  | Nilai numerik               |
| `tanggal` | DATE           | Tanggal entri               |

Sample data sudah terisi otomatis dari `sql/init_statistik.sql` saat container
MySQL pertama kali jalan.

---

## Cara Menunjukkan Aplikasi (sesuai CLAUDE.md)

1. **Jalankan stack**: `docker compose up -d`
2. **Masuk terminal container**: `docker compose exec python bash`
3. **Tampilkan data**:
   ```bash
   python app/statistik.py
   # pilih menu 1 -> lihat semua data
   ```
4. **Tambah data baru**:
   ```bash
   # pilih menu 2 -> masukkan kategori, nilai, tanggal
   ```
5. **Lihat ringkasan**:
   ```bash
   # pilih menu 3 -> total, rata-rata, jumlah per kategori
   ```
6. **Verifikasi langsung di MySQL**:
   ```bash
   mysql -h db -u digitalenta -pdigitalenta_pass digitalenta_db -e "SELECT * FROM statistik;"
   ```

---

## Perintah Berguna

```bash
# Lihat status container
docker compose ps

# Lihat log
docker compose logs -f
docker compose logs -f db

# Hentikan container (data MySQL tetap tersimpan di volume)
docker compose down

# Hentikan + hapus volume (reset total)
docker compose down -v
```

---

## Catatan

- Ikuti aturan CLAUDE.md: **tidak menambah fitur di luar kebutuhan bengkel sederhana**.
- Port host sengaja dipilih `3311` agar tidak bentrok dengan stack MySQL lain
  (`3306`, `3310`).
- Source code di-mount sebagai volume, jadi perubahan file `.py`/`sql` di host
  langsung terbaca di container **tanpa rebuild**.
