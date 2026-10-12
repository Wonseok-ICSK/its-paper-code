# Write a subsampled CSV by keeping alternating rows.
# Input/output paths and recording selections are local research settings.
import csv

def remove_odd_rows(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for i, row in enumerate(reader, start=1):
            if i % 2 == 0:  # 짝수 행만 유지
                writer.writerow(row)

# 사용 예시
input_filename = 'chart/results.csv'
output_filename = 'chart/data.csv'
remove_odd_rows(input_filename, output_filename)