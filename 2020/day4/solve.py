from pathlib import Path
import re

input_file = 'input.txt'
# prepare data
raw_input = Path(input_file).read_text().splitlines()
# parse into list of dicts
passports = [{}]
for line in raw_input:
    # new entry with empty line
    if len(line) == 0:
        passports.append({})
    else:
        passports[-1].update({e.split(':')[0]: e.split(':')[1] for e in line.split()})

# count the valid passes
required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def chk_date_str(date, min, max):
    return len(date) == 4 and date.isdigit() and min <= int(date) <= max

hgt_pattern = re.compile('(\d{3})cm|(\d{2})in$')
validators = {'byr': lambda x: chk_date_str(x, 1920, 2002),
              'iyr': lambda x: chk_date_str(x, 2010, 2020),
              'eyr': lambda x: chk_date_str(x, 2020, 2030),
              'hgt': lambda x: bool(hgt_pattern.match(x)) and }
n_valid = 0
for p in passports:
    chk_fields = [1 if k in required_fields else 0 for k in p]
    if sum(chk_fields) == len(required_fields):
        n_valid += 1

print(n_valid)

