import csv
import sys

COLUMNS = [
    'Fund Code',
    'Dept Number',
    'Appropriation Authority',
    'Description',
    'Previous Year Grant',
    'Anticipated Grant',
    'Carryover',
    'Year Total',
]


if __name__ == '__main__':
    """Check that totals for each group add up"""
    rows = [r for r in csv.DictReader(sys.stdin)]
    groups = []
    group = []
    for row in rows:
        if 'Total' in row['Description']:
            group.append(row)
            groups.append(group)
            group = []
        else:
            group.append(row)

    for col in COLUMNS[4:]:
        for group in groups:
            rec_total = sum([int(r[col]) for r in group[:-1] if r[col]])
            if len(group[:-1]) == 0:
                continue
            if group[-1][col]:
                try:
                    assert rec_total == int(group[-1][col])
                except AssertionError:
                    group_id = ''.join([group[-1][c] for c in COLUMNS[:3]])
                    raise ValueError(
                        f'\nTotals do not add up for {group_id} {col}\n'
                        f'Sum is {rec_total}, total is {int(group[-1][col])}'
                    )
