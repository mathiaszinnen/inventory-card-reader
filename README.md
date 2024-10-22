# Inventory Card Reader
This repository contains code to read, process, and integrate data from inventory cards. Currently it uses (pero-ocr)[https://github.com/DCGM/pero-ocr] for text recognition. 

## Installation
1. Install the package from pip using `pip install inventory-card-reader`
2. Or clone the repository and do your thing

## Prepare config files
- Create a config yaml file with the following keys:
```
xml_output_folder: <<temporary directory to store intermediate xml files>>
region_config: <<path to region config json>>
yolo_weights: <<path to trained yolo model to detect figures>>
output_dir: <<directory to store the resulting csv and extracted images>>
``` 
- Create a region config json file where the inventory card regions are defined. This file is expected to have the following structure:
```
{
    "regions": 
        <<key1>>: [x1,y1,x2,y2]
        <<key2>>: [x1,y1,x2,y2]
        <<...>>: [...]
}
```
Where key define the column names to be extracted and x1,y1,x2,y2 denote the relative coordinates of the region where the values for the respective columns can be found in the inventory card. (x1,y1) denote the coordinates of the top left corner of the region, and x2,y2 the bottom right. 

For example:
```
{
    "regions": {
        "Gegenstand": [0.047,0,1,0.077],
        "Inv. Nr.": [0.047,0.077,0.275,0.135],
    }
}
```
- Download the pero ocr model weights provided by the pero developers (here)[https://nextcloud.fit.vutbr.cz/s/NtAbHTNkZFpapdJ], unzip the file and store the .pt and .pt.cpu files in the pero_resources folder
- Start the extraction by invoking `read_inventory_cards <<config>> <<input_folder>>` where `<<config>>` is the path to the config yaml file described above and `<<input folder>>` the path to a directory of scanned jpgs of inventory cards to be processed.

## Contributing
I'm happy to receive feedback and code contributions. Feel free to open issues or create pull requests.
