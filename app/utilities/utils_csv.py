"""Utilties related with working with csv I/O operations."""
import os 
import csv 

def write_to_csv(file_path: str, header: list, *args):
    """
    Write data to a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        header (list): The header row for the CSV file.
        *args: Variable number of arguments representing the data rows.

    Note:
        The CSV file is opened in append mode.

    """
    with open(file_path, mode="a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        if os.path.getsize(filename=file_path) == 0:
            csv_writer.writerow(header)
        csv_writer.writerow(args)
