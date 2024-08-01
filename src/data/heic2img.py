import pillow_heif
from PIL import Image
from pathlib import Path

def heic2img(heic_path: Path, output_extension: str ='jpeg', output_path: Path = None):
    """
    Convert HEIC image to jpeg or png
    """
    try:
        # Ensure the output extension is valid
        if output_extension not in ['png', 'jpeg']:
            raise ValueError("Unsupported output extension. Please use 'png' or 'jpeg'.")

        # Check if the input file exists and is a file
        heic_path = Path(heic_path)
        if not heic_path.exists() or not heic_path.is_file():
            raise FileNotFoundError(f"The file {heic_path} does not exist or is not a file.")
        
        # Read the HEIC file
        heif_file = pillow_heif.read_heif(heic_path)
        
        # Convert HEIC to image
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )

        # Determine the output file path
        if not output_path:
            output_path = heic_path.with_suffix(f'.{output_extension}')
        else:
            output_path = Path(output_path)
        
        # Save image
        image.save(output_path, format=output_extension.upper())
        print(f"Image saved as {output_path}")
        return output_path

    except FileNotFoundError as fnf:
        print(fnf)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    script_path = Path(__file__).resolve()
    root_path = script_path.parents[2]
    data_path = root_path / 'data/raw/SharkEggs/BlondeRay/dry'
    test_file = next(data_path.iterdir())
    heic2img(test_file, "png", test_file.parent / "_test.png")