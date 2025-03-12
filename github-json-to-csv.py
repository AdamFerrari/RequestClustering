import json
import csv

def json_to_csv(input_json_file, output_csv_file):
    # Read JSON file
    with open(input_json_file, 'r') as json_file:
        data = json.load(json_file)
    
    # Specify the fields we want to keep
    fields_to_keep = ['id', 'title', 'body']
    
    # Write to CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields_to_keep)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for item in data:
            # Create a new dict with only the fields we want
            filtered_item = {field: item.get(field, '') for field in fields_to_keep}
            writer.writerow(filtered_item)

if __name__ == "__main__":
    input_file = "issues.json"
    output_file = "issues.csv"
    
    try:
        json_to_csv(input_file, output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
