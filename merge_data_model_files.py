#!/usr/bin/env python3

import json
import os
import fnmatch
from argparse import ArgumentParser


def main(args):
    # input parameters
    metrics_stubs = args.metrics_data
    participant_stubs = args.participant_data
    aggregation_stubs = args.aggregation_data
    output_dir = args.output

    # Assuring the output directory does exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data_model_file = []

    data_model_file = join_json_files(participant_stubs, data_model_file, "*.json")
    data_model_file = join_json_files(metrics_stubs, data_model_file, "*.json")
    data_model_file = join_json_files(aggregation_stubs, data_model_file, "*.json")

    # write the merged data model file to json output
    output_file = os.path.join(output_dir, "data_model_file.json")
    with open(output_file, 'w') as f:
        json.dump(data_model_file, f, sort_keys=True, indent=4, separators=(',', ': '))


def join_json_files(files, data_model_file, file_extension):
    for abs_result_file in files:
        if fnmatch.fnmatch(abs_result_file, file_extension) and os.path.isfile(abs_result_file):
            with open(abs_result_file, mode='r', encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict):
                    data_model_file.append(content)
                else:
                    data_model_file.extend(content)
    return data_model_file


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--participant_data", nargs='*', required=True,
                        help="file(s) that contains the participant json stub (generated by validation step)")
    parser.add_argument("-m", "--metrics_data", nargs='*',
                        help="dir where the data for the assessment metrics are stored", required=True)
    parser.add_argument("-a", "--aggregation_data", nargs='*', required=True,
                        help="files containing the benchmark stubs")
    parser.add_argument("-o", "--output", required=True,
                        help="output directory where the minimal dataset JSON file will be written")

    args = parser.parse_args()

    main(args)