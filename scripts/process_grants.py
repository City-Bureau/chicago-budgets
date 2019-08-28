import csv
import re
import sys

COLUMNS = [
    "Fund Code",
    "Dept Number",
    "Appropriation Authority",
    "Description",
    "Previous Year Grant",
    "Anticipated Grant",
    "Carryover",
    "Year Total",
]


def clean_numbers(row_cols):
    return [re.sub(r"[\$,\(\)]", "", c) for c in row_cols]


def process_page(dept, page):
    page_rows = []
    auth = ""
    fund = ""
    desc = ""
    for row in page[2:]:
        if "Total" in row[0]:
            desc = row[0]
        elif re.match(r"[\d\w]{3} -", row[0]):
            dept = row[0].split(" - ")[0]
            continue
        elif re.match(r".*[\d\w]{4}:.*", row[0]):
            split_row = row[0].split(":")
            if len(split_row) >= 3:
                fund, auth, desc = row[0].split(":")[:3]
            else:
                auth, desc = row[0].split(":")[:2]
            fund = fund.replace("*", "")
        else:
            continue
        row_items = [fund, dept, auth, desc] + clean_numbers(row[1:])
        row_dict = dict(zip(COLUMNS, row_items))
        for c in COLUMNS[4:]:
            row_dict[c] = int(row_dict[c]) if row_dict[c] else ""
        page_rows.append(row_dict)
    return dept, page_rows


if __name__ == "__main__":
    rows = [r for r in csv.reader(sys.stdin)]
    year_str = sys.argv[1]
    line_items = []
    page = []
    dept = ""
    for row in rows:
        if len(row) == 0:
            continue
        elif re.match(r"[\d\w]{3} -", row[0]):
            dept = row[0].split(" - ")[0]
            page.append(row)
        elif row[0].startswith("Page "):
            dept, page_rows = process_page(dept, page)
            line_items.extend(page_rows)
            page = []
        else:
            page.append(row)
    line_items = [{**line_item, "Year": year_str} for line_item in line_items]
    writer = csv.DictWriter(
        sys.stdout, fieldnames=["Year"] + COLUMNS, quoting=csv.QUOTE_NONNUMERIC
    )
    writer.writeheader()
    writer.writerows(line_items)
