from processors.image_detector import YoloImageDetector
from processors.page_xml_parser import PageXMLParser
from processors.pero_ocr_processor import PeroOCRProcessor
import argparse
import yaml

def parse_yaml_config(args):
    with open(args.config, 'r') as f:
        config_data = yaml.safe_load(f)
        for k,v in config_data.items():
            setattr(args, k, v)
    return args


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='Path to the config yaml file.')
    parser.add_argument('input_folder', help='Path to the folder which containts the inventory card scans to be processed')

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit()
    args = parse_yaml_config(args)

    return args

def main(args):
    pero_config_path = 'pero_resources/config_cpu.ini'
    detector = YoloImageDetector(args.yolo_weights)
    ocr_processor = PeroOCRProcessor(pero_config_path, args.input_folder, args.xml_output_folder)
    page_xml_processor = PageXMLParser(args.region_config, args.xml_output_folder,
                                       custom_header_filters=args.header_filters,
                                       file_skip_markers=args.file_skip_markers)

    results = ocr_processor.parse_directory(args.input_folder)
    detector.parse_directory(args.input_folder)
    page_xml_processor.process(output_folder=args.output_dir)
    print(f'Extracted images and information saved to {args.output_dir}')



if __name__ == '__main__':
    args = parse_args()
    main(args)