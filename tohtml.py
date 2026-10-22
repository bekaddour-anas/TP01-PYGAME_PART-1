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
                "module_name": row['module_name'],
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


def modules_to_html(data):
    html = [
        '<html><head><meta charset="utf-8">',
        '<style>',
        'body { font-family: Arial, sans-serif; margin: 20px; }',
        'table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }',
        'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
        'th { background-color: #f2f2f2; }',
        '</style>',
        '</head><body>',
        '<h1>Academic Modules Summary</h1>'
    ]

    for semester, unites in data.items():
        html.append(f"<h2>Semester {semester}</h2>")
        for unite, modules in unites.items():
            html.append(f"<h3>{unite}</h3>")
            html.append("<table>")
            html.append("<tr><th>Module Code</th><th>Title</th><th>Coef</th><th>Credit</th>"
                        "<th>TP%</th><th>TD%</th><th>Exam%</th></tr>")
            for info in modules:
                html.append("<tr>")
                html.append(f"<td>{info['module_name']}</td>")
                html.append(f"<td>{info['module_title']}</td>")
                html.append(f"<td>{info['coef']}</td>")
                html.append(f"<td>{info['credit']}</td>")
                html.append(f"<td>{info['percent_tp'] * 100:.0f}%</td>")
                html.append(f"<td>{info['percent_td'] * 100:.0f}%</td>")
                html.append(f"<td>{info['percent_exam'] * 100:.0f}%</td>")
                html.append("</tr>")
            html.append("</table>")  # Correctly closed inside the unit loop
        
        html.append("<hr>")

    html.append("</body></html>")
    return "\n".join(html)


# --------- Test ---------
if __name__ == "__main__":
    filename = "convas-gsi.csv"  # Updated file name
    result = csv_to_nested_dict(filename)
    
    # Generate HTML content
    html_content = modules_to_html(result)

    # Save to file
    output_filename = "modules.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file generated successfully: {output_filename}")