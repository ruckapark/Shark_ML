from pathlib import Path

if __name__ == "__main__":

    
    root = Path(__file__).parents[2]
    data_root = root / 'data/processed/SharkEggs'
    print(data_root)

    # Loop through all subdirectories
    for subdir in data_root.iterdir():
        if subdir.is_dir():  # Check if it's a directory
            print(f"\nDirectory: {subdir.name}")
            for condition_dir in ['dry', 'wet']:
                condition_path = subdir / condition_dir
                if condition_path.exists() and condition_path.is_dir():
                    # Count the number of files in the 'dry' and 'wet' subdirectories
                    num_files = len(list(condition_path.glob('*')))
                    print(f"{subdir} - {condition_dir}: {num_files} files")
