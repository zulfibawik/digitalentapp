# app/config.py
# Helper baca konfigurasi dari environment variable
# Sesuai docker-compose.yml bagian environment service python

import os


class Config:
    """Konfigurasi koneksi MySQL dari environment variable."""

    DB_HOST = os.environ.get("DB_HOST", "db")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_USER = os.environ.get("DB_USER", "digitalenta")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "digitalenta_pass")
    DB_NAME = os.environ.get("DB_NAME", "digitalenta_db")

    @classmethod
    def show(cls):
        """Tampilkan konfigurasi saat ini (untuk debugging)."""
        return (
            f"DB_HOST={cls.DB_HOST}, DB_PORT={cls.DB_PORT}, "
            f"DB_USER={cls.DB_USER}, DB_NAME={cls.DB_NAME}"
        )
