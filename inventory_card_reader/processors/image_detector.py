from ultralytics import YOLO
import os

class YoloImageDetector:
    def __init__(self,weights, chunk_size=50, device='cuda:0'):
        self.model = YOLO(weights)
        self.chunk_size=chunk_size
        self.device = device

    def _batch(self, iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:ndx+n]

    def parse_directory(self, input_dir):
        image_exts = ['.jpg', '.jpeg'] 
        images_to_process = [f'{input_dir}/{fn}' for fn in os.listdir(input_dir) if os.path.splitext(fn)[1] in image_exts]
        n_chunks = len(images_to_process) // self.chunk_size + 1
        i = 1
        for img_chunk in self._batch(images_to_process, self.chunk_size):
            print(f'Detecting images in chunk {i}/{n_chunks}..')
            self.model.predict(img_chunk, save_crop=True, device=self.device, save_dir='yolo_out',project='yolo_out')
            i+=1




