# Update docstring sesuai modul 12

"""Sistem Validasi Registrasi Mahasiswa (SOLID + Dependency Injection).

Modul Praktikum Pertemuan 12:
- Menambahkan docstring (Google Style)
- Mengganti print() dengan logging (INFO/WARNING)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

# Konfigurasi dasar logging (INFO ke atas akan tampil)
# Format: Waktu - Level - Nama Logger - Pesan
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

LOGGER = logging.getLogger("Registration")


@dataclass
class RegistrationData:
    """Menyimpan data registrasi mahasiswa.

    Attributes:
        name (str): Nama mahasiswa.
        sks_taken (int): Total SKS yang diambil.
        prerequisite_completed (bool): Status prasyarat (True jika terpenuhi).
    """

    name: str
    sks_taken: int
    prerequisite_completed: bool


class IValidationRule(ABC):
    """Interface untuk aturan validasi registrasi.

    Setiap aturan (rule) harus mengimplementasikan method `validate`
    yang mengembalikan True jika lolos, False jika gagal.

    Prinsip yang didukung:
        - DIP: RegistrationService bergantung pada abstraksi (IValidationRule),
          bukan implementasi konkret.
    """

    @abstractmethod
    def validate(self, data: RegistrationData) -> bool:
        """Memvalidasi data registrasi.

        Args:
            data (RegistrationData): Data registrasi yang akan divalidasi.

        Returns:
            bool: True jika valid, False jika tidak valid.
        """
        raise NotImplementedError


class SksLimitRule(IValidationRule):
    """Rule: memastikan SKS tidak melebihi batas maksimum."""

    def __init__(self, max_sks: int = 24) -> None:
        """Inisialisasi batas maksimum SKS.

        Args:
            max_sks (int): Batas maksimum SKS yang diizinkan.
        """
        self.max_sks = max_sks

    def validate(self, data: RegistrationData) -> bool:
        """Validasi SKS maksimum.

        Args:
            data (RegistrationData): Data registrasi mahasiswa.

        Returns:
            bool: True jika SKS <= max_sks, False jika melebihi.
        """
        if data.sks_taken > self.max_sks:
            LOGGER.warning(
                "[SksLimitRule] %s mengambil %s SKS (maks %s) -> GAGAL",
                data.name,
                data.sks_taken,
                self.max_sks,
            )
            return False

        LOGGER.info(
            "[SksLimitRule] %s mengambil %s SKS (maks %s) -> LOLOS",
            data.name,
            data.sks_taken,
            self.max_sks,
        )
        return True


class MinSksRule(IValidationRule):
    """Rule: memastikan SKS memenuhi batas minimum."""

    def __init__(self, min_sks: int = 12) -> None:
        """Inisialisasi batas minimum SKS.

        Args:
            min_sks (int): Batas minimum SKS yang wajib diambil.
        """
        self.min_sks = min_sks

    def validate(self, data: RegistrationData) -> bool:
        """Validasi SKS minimum.

        Args:
            data (RegistrationData): Data registrasi mahasiswa.

        Returns:
            bool: True jika SKS >= min_sks, False jika kurang.
        """
        if data.sks_taken < self.min_sks:
            LOGGER.warning(
                "[MinSksRule] %s mengambil %s SKS (min %s) -> GAGAL",
                data.name,
                data.sks_taken,
                self.min_sks,
            )
            return False

        LOGGER.info(
            "[MinSksRule] %s mengambil %s SKS (min %s) -> LOLOS",
            data.name,
            data.sks_taken,
            self.min_sks,
        )
        return True


class PrerequisiteRule(IValidationRule):
    """Rule: memastikan prasyarat mata kuliah terpenuhi."""

    def validate(self, data: RegistrationData) -> bool:
        """Validasi prasyarat.

        Args:
            data (RegistrationData): Data registrasi mahasiswa.

        Returns:
            bool: True jika prasyarat terpenuhi, False jika belum.
        """
        if not data.prerequisite_completed:
            LOGGER.warning(
                "[PrerequisiteRule] %s prasyarat belum terpenuhi -> GAGAL",
                data.name,
            )
            return False

        LOGGER.info("[PrerequisiteRule] %s prasyarat terpenuhi -> LOLOS", data.name)
        return True


class RegistrationService:
    """Service untuk menjalankan validasi registrasi menggunakan DI.

    RegistrationService menerima daftar rule (dependency) dari luar (DI),
    sehingga mudah menambah/mengurangi rule tanpa mengubah kode service.

    Args:
        rules (List[IValidationRule]): Daftar rule yang akan dijalankan.
    """

    def __init__(self, rules: List[IValidationRule]) -> None:
        """Inisialisasi RegistrationService.

        Args:
            rules (List[IValidationRule]): Rule validasi yang digunakan.
        """
        self.rules = rules

    def run_validation(self, data: RegistrationData) -> bool:
        """Menjalankan semua rule untuk satu data mahasiswa.

        Args:
            data (RegistrationData): Data registrasi mahasiswa yang diuji.

        Returns:
            bool: True jika semua rule lolos (registrasi disetujui),
            False jika ada rule yang gagal (registrasi ditolak).
        """
        LOGGER.info("=== Mulai validasi registrasi untuk %s ===", data.name)

        for rule in self.rules:
            if not rule.validate(data):
                LOGGER.warning("Registrasi %s DITOLAK.", data.name)
                return False

        LOGGER.info("Registrasi %s DISETUJUI.", data.name)
        return True


def main() -> None:
    """Menjalankan demo pengujian untuk beberapa mahasiswa."""
    LOGGER.info("=== PERTEMUAN 12: DOCSTRING + LOGGING + DI ===")

    rules: List[IValidationRule] = [
        MinSksRule(min_sks=12),
        SksLimitRule(max_sks=24),
        PrerequisiteRule(),
    ]
    service = RegistrationService(rules)

    # 1. Data valid
    service.run_validation(RegistrationData(name="Andi", sks_taken=20, prerequisite_completed=True))

    # 2. SKS kebanyakan
    service.run_validation(RegistrationData(name="Budi", sks_taken=28, prerequisite_completed=True))

    # 3. Prasyarat belum terpenuhi
    service.run_validation(RegistrationData(name="Cici", sks_taken=18, prerequisite_completed=False))

    # 4. SKS terlalu sedikit (untuk menunjukkan MinSksRule)
    service.run_validation(RegistrationData(name="Dodi", sks_taken=9, prerequisite_completed=True))


if __name__ == "__main__":
    main()
