import csv

def update_dict(dict, key, val):
  if not key in dict:
    dict[key] = val

def dict_val_to_list(dictionary):
  return [dictionary[key] for key in dictionary]

### adopted from Sorelle Friedler's code
def get_list_of_dicts(filename):
  with open(filename) as f:
    f_csv = csv.DictReader(f)
    return [row for row in f_csv]

def get_headers(filename):
  with open(filename) as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
  return headers

def write_csv_dicts(filename, headers, rows_list_of_dicts):
  with open(filename,'w') as f:
    f_csv = csv.DictWriter(f, headers, extrasaction='ignore')
    f_csv.writeheader()
    f_csv.writerows(rows_list_of_dicts)

def write_csv(filename, headers, rows_list_of_lists):
  with open(filename,'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows_list_of_lists)
