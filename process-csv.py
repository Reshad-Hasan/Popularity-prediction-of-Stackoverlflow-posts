# main file for processing the initial data-set
import csv
from process_post import feature
import control


class post:
    item = dict((i, 0) for i in control.post_columns)

    def __init__(self, item):
        self.item = item
        obj = feature(item)
        self.exFeatures = obj.get_features()

    def get_features(self):
        return self.exFeatures


if __name__ == '__main__':
    count = 0
    with open(control.processed_data_path, mode='w', encoding=control.ENCODING) as write_file:
        writer = csv.DictWriter(write_file, fieldnames=control.feature_keys)
        writer.writeheader()
        with open(control.csv_reading_path, mode='r', encoding=control.ENCODING) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            # each questions is processed and then written to processed data file
            for row in csv_reader:
                postObj = post(row)
                exFeatures = postObj.get_features()
                writer.writerow(exFeatures)
                line_count += 1
                print(line_count)
    print(count)
