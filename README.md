# SharkEggs

*Authors: E. Hirst, J. Hirst, and G. Ruck*

## Project Structure

This project is structured to facilitate the development of machine learning models for classifying image data, along with code for data processing and augmentation. The chosen structure ensures modularity, maintainability, and ease of collaboration among team members.

### Directory Layout

- **data/**: This directory holds all the image data ignored in remote.
  - `raw/`: Contains the original folder of all data
  - `processed/`: Contains processed image combined from raw and augmented (no longer HEIC files)
  - `augmented/`: Contains augmented images with same structure as raw
  - `README.md`: Provides documentation about the data structure and image files.

- **src/**: This directory contains all the source code for the project.
  - `data/`: Contains scripts for data processing and augmentation.
    - `data_processing.py`: Functions to for data preprocessing
	- `others.py` : Write any other files
  - `models/`: Contains scripts for defining, training, and evaluating models.
    - `model.py`: Contains the architecture of the models.
    - `train.py`: Script for training the models.
    - `evaluate.py`: Script for evaluating the trained models.
  - `config/`: Contains configuration files for the project.
    - `config.yaml`: Stores configuration settings for data processing, model training, etc.
  - `notebooks/`: Contains Jupyter notebooks for data exploration and experimentation.

- **tests/**: This directory contains unit tests to ensure the reliability of your scripts.
  - `test_data_processing.py`: Tests for data processing functions.
  - `test_data_augmentation.py`: Tests for data augmentation functions.
  - `test_model.py`: Tests for model definitions.
  - `test_train.py`: Tests for the training process.
  
 - **models/**: This directory contains pretrained models downloaded for use in this project

- **.gitignore**: Specifies files and directories to ignore / untracked.

- **requirements.txt**: Lists all Python package dependencies for the project.

- **environment.yml**: Necessary environment installation for SharkEggs clone.

- **README.md**: This overview.