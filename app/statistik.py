# app/statistik.py
# Script CLI bengkel sederhana untuk tabel statistik
# Sesuai CLAUDE.md: "Jangan menambah fitur di luar kebutuhan bengkel sederhana"
# Fitur: tambah data, lihat semua, ringkasan per kategori

from datetime import date
from app.db import fetch_all, execute
from app.config import Config


def tampilkan_semua():
    """Tampilkan semua data statistik dalam format tabel."""
    rows = fetch_all(
        "SELECT id, kategori, nilai, tanggal FROM statistik ORDER BY tanggal DESC, id DESC"
    )
    if not rows:
        print("\n[Tidak ada data di tabel statistik]\n")
        return
    print("\n=== Semua Data Statistik ===")
    print(f"{'ID':<5}{'Kategori':<18}{'Nilai':>12}   {'Tanggal':<12}")
    print("-" * 50)
    for r in rows:
        print(
            f"{r['id']:<5}{r['kategori']:<18}{float(r['nilai']):>12.2f}   "
            f"{r['tanggal'].isoformat():<12}"
        )
    print(f"\nTotal: {len(rows)} baris\n")


def tambah_data():
    """Tambah satu baris data statistik (input interaktif)."""
    print("\n=== Tambah Data Statistik ===")
    kategori = input("Kategori  : ").strip()
    if not kategori:
        print("[Kategori tidak boleh kosong]\n")
        return
    try:
        nilai = float(input("Nilai     : ").strip())
    except ValueError:
        print("[Nilai harus angka]\n")
        return
    tgl_input = input("Tanggal (YYYY-MM-DD, kosongkan untuk hari ini): ").strip()
    if not tgl_input:
        tgl = date.today().isoformat()
    else:
        tgl = tgl_input

    try:
        execute(
            "INSERT INTO statistik (kategori, nilai, tanggal) VALUES (%s, %s, %s)",
            (kategori, nilai, tgl),
        )
        print(f"[OK] Data tersimpan: {kategori} / {nilai} / {tgl}\n")
    except Exception as e:
        print(f"[ERROR] Gagal tambah data: {e}\n")


def ringkasan_per_kategori():
    """Hitung total, rata-rata, jumlah data per kategori."""
    rows = fetch_all(
        """
        SELECT kategori,
               COUNT(*)   AS jumlah,
               SUM(nilai)  AS total,
               AVG(nilai)  AS rata_rata
        FROM statistik
        GROUP BY kategori
        ORDER BY kategori
        """
    )
    if not rows:
        print("\n[Tidak ada data untuk diringkas]\n")
        return
    print("\n=== Ringkasan per Kategori ===")
    print(f"{'Kategori':<18}{'Jumlah':>8}{'Total':>14}{'Rata-rata':>14}")
    print("-" * 54)
    for r in rows:
        total = float(r["total"]) if r["total"] is not None else 0.0
        rata = float(r["rata_rata"]) if r["rata_rata"] is not None else 0.0
        print(
            f"{r['kategori']:<18}{r['jumlah']:>8}{total:>14.2f}{rata:>14.2f}"
        )
    print()


def main():
    print(f"\nConfig: {Config.show()}")
    print("=== digitalentappython - Latihan Python & Data Science ===")
    while True:
        print("Menu:")
        print("  1) Lihat semua data")
        print("  2) Tambah data")
        print("  3) Ringkasan per kategori")
        print("  0) Keluar")
        pilihan = input("Pilih [0-3]: ").strip()
        if pilihan == "1":
            tampilkan_semua()
        elif pilihan == "2":
            tambah_data()
        elif pilihan == "3":
            ringkasan_per_kategori()
        elif pilihan == "0":
            print("Bye.\n")
            break
        else:
            print("[Pilihan tidak dikenal]\n")


if __name__ == "__main__":
    main()
