
import csv
import os
import sys

def clean_csv(filename):
    if not os.path.isfile(filename):
        print("Error: File not found!")
        return

    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("Error: CSV file is empty!")
                return

            headers = [h.strip() if h else "" for h in reader.fieldnames]
            rows = []

            for row in reader:
                cleaned = {}
                for key, value in row.items():
                    if key is not None:
                        cleaned[key.strip()] = (
                            value.strip() if value else ""
                        )
                rows.append(cleaned)

        unique_rows = []
        seen = set()

        for row in rows:
            key = tuple(row.get(h, "") for h in headers)
            if key not in seen:
                seen.add(key)
                unique_rows.append(row)

        output = "cleaned_" + os.path.basename(filename)

        with open(output, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(unique_rows)

        print("\nCSV cleaning completed!")
        print("Original rows:", len(rows))
        print("Cleaned rows:", len(unique_rows))
        print("Duplicates removed:", len(rows) - len(unique_rows))
        print("Output file:", output)

    except (OSError, UnicodeError, csv.Error) as error:
        print("Could not process file:", error)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter CSV filename: ").strip()

    clean_csv(filename)
