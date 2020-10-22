import csv
import re
import sys

COLUMNS = [
    "Fund Code",
    "Dept Number",
    "Appropriation Authority",
    "Appropriation Account",
    "Appropriation Account Description",
    "Recommendation",
    "Previous Year Revised",
    "Previous Year Appropriation",
    "Earlier Year Expenditures",
]


def clean_numbers(row_cols):
    return [re.sub(r"[\$,]", "", c) for c in row_cols]


def process_page(auth, page):
    fund = page[0][0].split(" ")[0]
    dept = page[1][0].split(" ")[0]
    if page[2][0].startswith("("):
        auth = page[2][0].split("/")[-1][:-1]
    if page[3][0].startswith("("):
        auth = page[3][0].split("/")[-1][:-1]
    page_rows = []
    is_appropriations = False
    for row in page[2:]:
        if row[0].startswith("("):
            auth = row[0].split("/")[-1][:-1]
        elif row[0] == "Appropriations":
            is_appropriations = True
        elif row[0].startswith("Positio"):
            is_appropriations = False
        if not is_appropriations:
            continue
        starts_num = re.match(r"^\d", row[0])
        if starts_num or row[0] == "Appropriation Total*":
            if starts_num:
                appr_split = row[0].split(" ")
                appr_cols = [appr_split[0], " ".join(appr_split[1:])]
                if appr_cols[1].startswith("- "):
                    continue
                row_items = [fund, dept, auth] + appr_cols + clean_numbers(row[1:])
            else:
                row_items = [fund, dept, auth, ""] + clean_numbers(row)
            row_dict = dict(zip(COLUMNS, row_items))
            for c in COLUMNS[5:]:
                if not row_dict.get(c):
                    row_dict[c] = ""
                    continue
                row_val = row_dict[c]
                if re.match(r"\(\d+\)", row_dict.get(c, "")):
                    # Remove parentheses for negative values
                    row_val = f"-{row_val[1:-1]}"
                row_dict[c] = int(row_val)
            page_rows.append(row_dict)
    return auth, page_rows


if __name__ == "__main__":
    rows = [r for r in csv.reader(sys.stdin)]
    year_str = sys.argv[1]
    line_items = []
    page = []
    auth = ""
    for row in rows:
        if len(row) == 0:
            continue
        elif row[0].startswith("("):
            auth = row[0].split("/")[-1][:-1]
            page.append(row)
        elif row[1].startswith("Page "):
            auth, page_rows = process_page(auth, page)
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
