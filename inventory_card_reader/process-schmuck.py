from processors.image_detector import YoloImageDetector
from processors.page_xml_parser import PageXMLParser
from processors.pero_ocr_processor import PeroOCRProcessor
import argparse
import os
from dotenv import load_dotenv


def parse_args():
    parser = argparse.ArgumentParser()
    default_input_folder = os.getenv('INPUT_FOLDER')
    default_pero_conf = os.getenv('PERO_CONFIG')
    default_region_conf = os.getenv('REGION_CONFIG')
    default_detection_weights = os.getenv('YOLO_WEIGHTS')
    parser.add_argument('--input-folder', help='Path to inventory cards to be processed', default=default_input_folder)
    parser.add_argument('--xml-output-folder', help='Directory to store the inPageXMLParsertermediate page XML output', default='output/xml/')
    parser.add_argument('--pero-config', help='Path to config file for the PERO OCR engine', default=default_pero_conf)
    parser.add_argument('--region-config', help='File to define the regions of the inventory card', default=default_region_conf)
    parser.add_argument('--output-dir', help='Directory to store the structured data output', default='./output')
    parser.add_argument('--detection-weights', help='Checkpoint for the photo detector', default=default_detection_weights)

    return parser.parse_args()

def main(args):
    header_filters = ['Vers.-Wert:','Vers.-Wert:;']
    file_skip_markers = ['Verso', 'verso', 'Zusatz', 'zusatz']
    detector = YoloImageDetector(args.detection_weights)
    ocr_processor = PeroOCRProcessor(args.pero_config, args.input_folder, args.xml_output_folder)
    page_xml_processor = PageXMLParser(args.region_config, args.xml_output_folder,
                                       custom_header_filters=header_filters,
                                       file_skip_markers=file_skip_markers)

    results = ocr_processor.parse_directory(args.input_folder)
    detector.parse_directory(args.input_folder)
    page_xml_processor.process(output_folder=args.output_dir)
    print(f'Extracted images and information saved to {args.output_dir}')



if __name__ == '__main__':
    load_dotenv()
    args = parse_args()
    main(args)