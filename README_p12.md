# Praktikum Pertemuan 12 — Dokumentasi, Logging, dan Git

Proyek ini adalah **Sistem Validasi Registrasi Mahasiswa** yang sudah direfactor menggunakan prinsip **SOLID**
dan **Dependency Injection (DI)**, lalu ditambahkan:

- **Docstring (Google Style)** untuk dokumentasi inline
- **Logging** (`INFO` dan `WARNING`) sebagai pengganti `print()`
- **Git commit history** yang rapi (minimal 3 commit)

## Cara Menjalankan

Pastikan Python sudah terinstall, lalu jalankan:

```bash
python after_refactor_p12.py
```

## Output yang Diharapkan (Logging)

Program akan menampilkan log seperti:

- `INFO` saat validasi berjalan dan saat rule lulus
- `WARNING` saat rule gagal dan registrasi ditolak

## Struktur File (contoh)

- `after_refactor_p12.py` → versi refactor + docstring + logging
- `before_refactor.py` → versi sebelum refactor (dari pertemuan sebelumnya)
- `README.md` → dokumentasi singkat proyek
