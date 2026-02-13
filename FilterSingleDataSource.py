#!/usr/bin/env python3
"""
FilterSingleDataSource.py

Interactive CLI tool to explore Publications from
site.data.single_data_source–style YAML.

Features:
- Interactive filters (category, year, date range, journal, publisher)
- User-friendly prompts
- YYYYMMDD date input supported
- Case-insensitive search
- Prints results to terminal
- Exports results to Excel
- Auto-installs dependencies if missing
"""

import sys
import subprocess

# -------------------------------------------------
# Auto-install required packages
# -------------------------------------------------
def ensure(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f" Installing missing dependency: {pkg}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

for p in ["yaml", "pandas", "openpyxl"]:
    ensure(p)

import yaml
import pandas as pd
from datetime import datetime
from pathlib import Path

# -------------------------------------------------
# Load YAML data
# -------------------------------------------------
DATA_FILE = Path("_data/single_data_source.yml")

if not DATA_FILE.exists():
    print(" _data/single_data_source.yml not found")
    sys.exit(1)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    raw_items = yaml.safe_load(f)

# -------------------------------------------------
# Extract publications only
# -------------------------------------------------
publications = []

for item in raw_items:
    if "Publication" in item:
        pub = item["Publication"].copy()
        pub["id"] = item.get("id")

        # Normalize categories
        pub["categories"] = pub.get("categories", [])

        publications.append(pub)

if not publications:
    print(" No publications found")
    sys.exit(1)

# -------------------------------------------------
# Helper functions
# -------------------------------------------------
from datetime import datetime, date

def parse_iso_date(value):
    if value is None:
        return None

    # Case 1: YAML already parsed it as date
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    # Case 2: string date
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None

    return None

def print_pub(pub):
    print("=" * 80)
    print(f"ID       : {pub.get('id')}")
    print(f"Title    : {pub.get('title')}")
    print(f"Authors  : {pub.get('authors')}")
    print(f"Venue    : {pub.get('journal')}")
    print(f"Date     : {pub.get('date')}")
    print(f"Type     : {pub.get('pubType')}")
    print(f"Category : {', '.join(pub.get('categories', []))}")

    if "links" in pub:
        for k, v in pub["links"].items():
            print(f"Link({k}): {v.get('url')}")

# -------------------------------------------------
# Interactive filter menu
# -------------------------------------------------
while True:
    print("\n PUBLICATION FILTERS")
    print("1. Category")
    print("2. Year")
    print("3. Date range (YYYYMMDD)")
    print("4. Journal")
    print("5. Publisher")
    print("6. Exit")

    choice = input("Choose filter (1–6): ").strip()

    filtered = publications

    # -------------------------
    # Category
    # -------------------------
    if choice == "1":
        cat = input("Enter category (RAS / XAI / IAP): ").strip().upper()
        filtered = [
            p for p in publications
            if cat in p.get("categories", [])
        ]

    # -------------------------
    # Year
    # -------------------------
    elif choice == "2":
        year = input("Enter year (e.g., 2022): ").strip()

        filtered = []
        for p in publications:
            d = p.get("date")
            if d:
                # YAML date → datetime.date
                if hasattr(d, "year") and str(d.year) == year:
                    filtered.append(p)
                #  string fallback
                elif isinstance(d, str) and d.startswith(year):
                    filtered.append(p)


    # -------------------------
    # Date range
    # -------------------------
    elif choice == "3":
        print("Enter dates in YYYYMMDD format")
        start_raw = input("From date: ").strip()
        end_raw = input("To date: ").strip()

        try:
            start = datetime.strptime(start_raw, "%Y%m%d").date()
            end = datetime.strptime(end_raw, "%Y%m%d").date()
        except ValueError:
            print(" Invalid date format")
            continue

        filtered = []
        for p in publications:
            d = p.get("date")

            if isinstance(d, date):
                if start <= d <= end:
                    filtered.append(p)

            elif isinstance(d, str):
                try:
                    d2 = datetime.strptime(d, "%Y-%m-%d").date()
                    if start <= d2 <= end:
                        filtered.append(p)
                except ValueError:
                    pass


    # -------------------------
    # Journal
    # -------------------------
    elif choice == "4":
        term = input("Journal contains: ").strip().lower()
        filtered = [
            p for p in publications
            if term in (p.get("journal", "").lower())
        ]

    # -------------------------
    # Publisher
    # -------------------------
    elif choice == "5":
        term = input("Publisher contains: ").strip().lower()
        filtered = [
            p for p in publications
            if term in (p.get("publisher", "").lower())
        ]

    elif choice == "6":
        print(" Exiting")
        break

    else:
        print(" Invalid option")
        continue

    # -------------------------------------------------
    # Display results
    # -------------------------------------------------
    print(f"\n Results found: {len(filtered)}\n")

    for pub in filtered:
        print_pub(pub)

    # -------------------------------------------------
    # Export to Excel
    # -------------------------------------------------
    if filtered:
        df = pd.json_normalize(filtered)

        # Sort safely by date
        if "date" in df.columns:
            df["date_sort"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.sort_values("date_sort", ascending=False)
            df = df.drop(columns=["date_sort"])

        out = "filtered_publications.xlsx"
        df.to_excel(out, index=False)
        print(f"\n Exported to {out}")
