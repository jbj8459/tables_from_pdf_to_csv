import pandas as pd
import camelot
import os
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Extract tables from just one PDF file."
    )
    parser.add_argument(
        "--pdf", "-p",
        type = str,
        required = True,
        help = "Path to the PDF file"
    )
    parser.add_argument(
        "--output", "-o",
        type = str,
        default = os.getcwd(),
        help = "Output directory for the CSV files"
    )
    parser.add_argument(
        "--start", "-s",
        type = str,
        default = "1",
        help = "Pages to extract tables from (default: 1)"
    )
    parser.add_argument(
        "--end", "-e",
        type = str,
        default = "end",
        help = "Pages to extract tables to (default: end)"
    )
    parser.add_argument(
        "--style", "-st",
        choices = ["stream", "lattice"],
        default = "stream",
        help = "Table extraction style (default: stream) (lattice for tables with lines)"
    )
    args = parser.parse_args()
    pdf_path = args.pdf
    output_dir = args.output
    page_range = args.start + "-" + args.end
    if not os.path.exists(output_dir):
        print("Output directory does not exist. Creating it...")
        os.makedirs(output_dir)
        
    # Read the PDF file and converts to a list of tables
    try:
        print(f"Reading PDF file: {pdf_path}")
        tables = camelot.read_pdf(pdf_path, pages=page_range, flavor=args.style)
    except:
        print(f"Error reading PDF file: {pdf_path}")
        return
    for i, table in enumerate(tables):
        # Convert the table to a DataFrame
        df = table.df
        # Save the DataFrame to a CSV file
        csv_path = os.path.join(output_dir, f"table_{i+1}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Table {i+1} saved to {csv_path}")
        
if __name__ == "__main__":
    main()