import pandas as pd

def filter_csv(input_csv_file, output_csv_file):
    # Read the CSV file
    df = pd.read_csv(input_csv_file)
    
    # Get all columns that match "Custom field (Customer)"
    customer_columns = [col for col in df.columns if "Custom field (Customer)" in col]
    
    # Filter rows where:
    # 1. Issue Type is "Feature"
    # 2. At least one Customer field is non-empty
    mask_issue_type = df["Issue Type"] == "Feature"
    mask_customer = df[customer_columns].notna().any(axis=1)
    filtered_df = df[mask_issue_type & mask_customer]
    
    # Keep only the specified columns
    columns_to_keep = ["Issue key", "Summary", "Description"]
    final_df = filtered_df[columns_to_keep]
    
    # Write to new CSV file
    final_df.to_csv(output_csv_file, index=False)

if __name__ == "__main__":
    input_file = "input.csv"
    output_file = "filtered_output.csv"
    
    try:
        filter_csv(input_file, output_file)
        print(f"Successfully filtered {input_file} to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
