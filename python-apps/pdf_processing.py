import subprocess
import camelot

# Path to the input scanned PDF
input_pdf = './scanned_document.pdf'

# Path to the output searchable PDF
output_pdf = './searchable_document.pdf'

# Convert the scanned PDF to a searchable PDF using OCRmyPDF
subprocess.run(['ocrmypdf', input_pdf, output_pdf])

# Extract tables from the searchable PDF using camelot-py
tables = camelot.read_pdf(output_pdf)

# Path to the output CSV file
output_csv = './table_data.csv'

# Save the table data in a CSV file
tables.export(output_csv, f='csv', compress=True)

print("Table data extracted and saved successfully!")