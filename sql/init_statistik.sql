-- init_statistik.sql
-- Tabel normal sederhana sesuai CLAUDE.md: aturan database
-- Auto-eksekusi saat container MySQL pertama kali jalan

USE digitalenta_db;

-- Drop tabel jika sudah ada (untuk re-init bersih)
DROP TABLE IF EXISTS statistik;

-- Buat tabel statistik
CREATE TABLE statistik (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kategori VARCHAR(50) NOT NULL,
    nilai DECIMAL(10,2) NOT NULL,
    tanggal DATE NOT NULL,
    INDEX idx_kategori (kategori),
    INDEX idx_tanggal (tanggal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample data untuk latihan
INSERT INTO statistik (kategori, nilai, tanggal) VALUES
    ('nilai_siswa',    85.50, '2026-01-10'),
    ('nilai_siswa',    90.00, '2026-01-11'),
    ('nilai_siswa',    78.25, '2026-01-12'),
    ('penjualan',     1500.00, '2026-01-10'),
    ('penjualan',     2300.50, '2026-01-11'),
    ('penjualan',     1800.75, '2026-01-12'),
    ('kehadiran',      95.00, '2026-01-10'),
    ('kehadiran',      88.50, '2026-01-11'),
    ('kehadiran',      92.00, '2026-01-12'),
    ('kunjungan_web', 1200.00, '2026-01-10'),
    ('kunjungan_web', 1450.50, '2026-01-11');
