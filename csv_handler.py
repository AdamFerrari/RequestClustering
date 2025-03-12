import csv
from typing import List, Dict

class CSVHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.rows = []

    def read_rows(self) -> List[Dict]:
        """Read and validate CSV file, returning list of row dictionaries."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # Validate header
                header = next(reader, None)
                if not header or len(header) != 3:
                    raise ValueError("CSV must have exactly 3 columns: id, title, description")

                # Normalize header names
                expected_headers = ['id', 'title', 'description']
                header = [h.lower().strip() for h in header]
                
                if header != expected_headers:
                    raise ValueError(f"CSV headers must be: {', '.join(expected_headers)}")

                # Read and validate rows
                for row_num, row in enumerate(reader, start=2):
                    if len(row) != 3:
                        raise ValueError(f"Row {row_num} has incorrect number of columns")
                    
                    if not row[0].strip():
                        raise ValueError(f"Row {row_num} has empty ID")

                    self.rows.append({
                        'id': row[0].strip(),
                        'title': row[1].strip(),
                        'description': row[2].strip()
                    })

                if not self.rows:
                    raise ValueError("CSV file is empty")

                return self.rows

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")
        except csv.Error as e:
            raise ValueError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
