import csv
import sys

COLUMNS = [
    'Fund Code',
    'Dept Number',
    'Appropriation Authority',
    'Appropriation Account',
    'Appropriation Account Description',
    'Recommendation',
    'Previous Year Revised',
    'Previous Year Appropriation',
    'Earlier Year Expenditures',
]


if __name__ == '__main__':
    """Check that totals for each group add up"""
    rows = [r for r in csv.DictReader(sys.stdin)]
    groups = []
    group = []
    for row in rows:
        if row['Appropriation Account Description'] == 'Appropriation Total*':
            group.append(row)
            groups.append(group)
            group = []
        elif '- Total' not in row['Appropriation Account Description']:
            group.append(row)

    for col in COLUMNS[5:]:
        for group in groups:
            rec_total = sum([int(r[col]) for r in group[:-1] if r[col]])
            if group[-1][col]:
                try:
                    assert rec_total == int(group[-1][col])
                except AssertionError:
                    group_id = ''.join([group[-1][c] for c in COLUMNS[:4]])
                    raise ValueError(
                        f'\nTotals do not add up for {group_id} {col}\n'
                        f'Sum is {rec_total}, total is {int(group[-1][col])}'
                    )
