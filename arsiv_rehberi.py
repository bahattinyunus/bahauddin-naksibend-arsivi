#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Şah-ı Nakşibend Dijital Arşiv Rehberi (CLI)
Kullanım:
  python arsiv_rehberi.py                -> Genel özet ve Günün Hikmeti
  python arsiv_rehberi.py --kelimat      -> 11 Kelimât-ı Kudsiyye listesi
  python arsiv_rehberi.py --yedi-pir     -> Buhara'nın Yedi Pîri (Pîr-i Heftgâne)
  python arsiv_rehberi.py --hikmet       -> Hikmetli sözlerinden seçmeler
  python arsiv_rehberi.py --ara <kelime> -> Arşivdeki tüm Markdown dosyalarında arama yapar
"""

import argparse
import json
import os
import random
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "kulliyat.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def print_banner():
    print("=" * 76)
    print(" 📜 ŞAH-I NAKŞİBEND MUHAMMED BAHAÜDDİN EL-BUHÂRÎ DİJİTAL KÜLLİYATI")
    print("    Kasr-ı Ârifân • Buhârâ-yı Şerîf (718/1318 – 791/1389)")
    print("=" * 76)


def show_summary(data):
    print_banner()
    meta = data["metadata"]
    print(f"\n👑 İsim ve Unvanlar : {meta['subject']}")
    print(f"   Lakapları        : {', '.join(meta['titles'])}")
    print(f"   Doğumu           : {meta['birth']['hijri']} ({meta['birth']['miladi']}) - {meta['birth']['place']}")
    print(f"   Vuslatı          : {meta['death']['hijri']} ({meta['death']['miladi']}) - {meta['death']['place']}")
    print("\n⚖️  İki Temel Gönül Düsturu:")
    for idx, p in enumerate(meta["core_principles"], 1):
        print(f"   {idx}. {p}")
    hikmet = random.choice(data["hikmetli_sozler"])
    print(f"\n💎 Günün Hikmeti:\n   \"{hikmet}\"\n")


def show_kelimat(data):
    print_banner()
    print("\n🏛️  KELİMÂT-I KUDSİYYE (11 TEMEL PRENSİP):\n")
    for item in data["kelimat_i_kudsiyye"]:
        print(f"  {item['no']:2d}. {item['name']} ({item['persian']}) — [{item['founder']}]")
        print(f"      {item['meaning']}\n")


def show_yedi_pir(data):
    print_banner()
    print("\n🕌 BUHARA'NIN YEDİ PÎRİ (PÎR-İ HEFTGÂNE):\n")
    for item in data["buhara_yedi_pir"]:
        print(f"  {item['order']}. Pîr: {item['name']} (v. {item['death']})")
        print(f"     Belde: {item['location']} | Meslek: {item['profession']}\n")


def show_hikmetler(data):
    print_banner()
    print("\n💎 HİKMETLİ SÖZLERİ VE İRŞADLARI:\n")
    for idx, soz in enumerate(data["hikmetli_sozler"], 1):
        print(f"  {idx:2d}. \"{soz}\"")
    print()


def search_archive(query):
    print_banner()
    print(f"\n🔍 '{query}' için arşivde arama sonuçları:\n")
    q_lower = query.lower()
    matches = 0
    for root, _, files in os.walk(BASE_DIR):
        if ".git" in root:
            continue
        for file in sorted(files):
            if file.endswith(".md"):
                path = Path(root) / file
                rel_path = path.relative_to(BASE_DIR)
                try:
                    lines = path.read_text(encoding="utf-8").splitlines()
                    for line_no, line in enumerate(lines, 1):
                        if q_lower in line.lower():
                            matches += 1
                            print(f"  📄 {rel_path}:{line_no} -> {line.strip()[:100]}")
                except Exception:
                    pass
    if matches == 0:
        print("  Sonuç bulunamadı.")
    else:
        print(f"\nToplam {matches} eşleşme bulundu.\n")


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Şah-ı Nakşibend Dijital Arşiv Rehberi")
    parser.add_argument("--kelimat", action="store_true", help="11 Kelimât-ı Kudsiyye'yi listeler")
    parser.add_argument("--yedi-pir", action="store_true", help="Buhara'nın Yedi Pîri'ni listeler")
    parser.add_argument("--hikmet", action="store_true", help="Hikmetli sözlerini listeler")
    parser.add_argument("--ara", type=str, metavar="KELİME", help="Arşiv dosyalarında kelime arar")
    args = parser.parse_args()

    data = load_data()
    if args.kelimat:
        show_kelimat(data)
    elif args.yedi_pir:
        show_yedi_pir(data)
    elif args.hikmet:
        show_hikmetler(data)
    elif args.ara:
        search_archive(args.ara)
    else:
        show_summary(data)


if __name__ == "__main__":
    main()
