from pero_ocr.user_scripts.parse_folder import get_device, PageParser, Computator, create_dir_if_not_exists
from configparser import ConfigParser
import os


class PeroOCRProcessor:
    def __init__(self, config_path, input_image_path, output_xml_path, device_name="gpu"):
        config = ConfigParser()
        config.read(config_path)

        self.device = get_device(device_name)
        self.output_xml_path = output_xml_path

        page_parser = PageParser(config,config_path=os.path.dirname(config_path), device=self.device)
        create_dir_if_not_exists(output_xml_path)
        self.computator = Computator(page_parser, input_image_path=input_image_path, input_xml_path=None, input_logit_path=None, 
                                     output_render_path=None, output_logit_path=None, output_alto_path=None, output_xml_path=output_xml_path,
                                     output_line_path=None)

    def parse_directory(self, image_directory, skip_processed_files=True):
        image_exts = ['.jpg', '.jpeg'] 
        images_to_process = [fn for fn in os.listdir(image_directory) if os.path.splitext(fn)[1] in image_exts]
        if skip_processed_files:
            processed_ids = [os.path.splitext(img_id)[0] for img_id in os.listdir(self.output_xml_path)]
            images_to_process = [fn for fn in images_to_process if os.path.splitext(fn)[0] not in processed_ids]
            print(f'Skipping {len(os.listdir(image_directory)) - len(images_to_process)} already processed images.')
        images_to_process = sorted(images_to_process)
        ids_to_process = [os.path.splitext(os.path.basename(fn))[0] for fn in images_to_process]

        results = []
        for index, (file_id, image_file_name) in enumerate(zip(ids_to_process, images_to_process)):
            results.append(self.computator(image_file_name, file_id, index, len(ids_to_process)))

        return results
        