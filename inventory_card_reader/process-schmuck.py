from processors.image_detector import ImageDetector
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
    parser.add_argument('--input-folder', help='Path to inventory cards to be processed', default=default_input_folder)
    parser.add_argument('--xml-output-folder', help='Directory to store the intermediate page XML output', default='./xml_output/')
    parser.add_argument('--pero_config', help='Path to config file for the PERO OCR engine', default=default_pero_conf)
    parser.add_argument('--region_config', help='File to define the regions of the inventory card', default=default_region_conf)
    parser.add_argument('--output_dir', help='Directory to store the structured data output', default='./output')

    return parser.parse_args()

def main(args):
    detector = ImageDetector()
    ocr_processor = PeroOCRProcessor(args.pero_config, args.input_folder, args.xml_output_folder)
    page_xml_processor = PageXMLParser(args.region_config, args.xml_output_folder)

    results = ocr_processor.parse_directory(args.input_folder)
    page_xml_processor.process(output_folder=args.output_dir)
    print('aye')



if __name__ == '__main__':
    load_dotenv()
    args = parse_args()
    main(args)