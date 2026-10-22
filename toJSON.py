import csv
import json

def csv_to_nested_dict(csv_file):
    # Nested dictionary format
    data = {
        "S1": {},
        "S2": {}
    }

    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            semester = row['semester']
            unite = row['unit']

            # Build module as dictionary
            module = {
                "module_name_": row['module_name'],
                "module_title": row['module_title'],
                "coef": int(row['coef']),
                "credit": int(row['credit']),
                "percent_tp": float(row['percent_tp']),
                "percent_td": float(row['percent_td']),
                "percent_exam": float(row['percent_exam'])
            }
            
            # Initialize a unit as a list if it doesn't exist yet
            if unite not in data[semester]:
                data[semester][unite] = []
            
            data[semester][unite].append(module)

    return data

# --------- Test ---------
if __name__ == "__main__":
    filename = "convas-gsi.csv"  # Make sure this matches your exact file name
    result = csv_to_nested_dict(filename)
    print(result)
    pretty_json = json.dumps(result, indent=4, ensure_ascii=False)
    print(pretty_json)