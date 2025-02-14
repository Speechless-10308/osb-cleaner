import argparse
import os

from osb_parse import OsuStoryboard

# get mapset directory
parser = argparse.ArgumentParser(description='Detector')
parser.add_argument('--mapset-dir', type=str, help='Mapset directory')

def main():
    args = parser.parse_args()
    mapset_dir: str = args.mapset_dir
    mapset_dir = mapset_dir.strip('"')
    osb_filepath = None
    try:
        os.listdir(mapset_dir)
        for root, dirs, files in os.walk(mapset_dir):
            for file in files:
                if file.endswith('.osb'):
                    osb_filepath = os.path.join(root, file)
    except FileNotFoundError:
        print('Mapset directory not found, check the path and try again.')
        return
    
    if osb_filepath is None:
        print('No .osb file found in the mapset directory.')
        return
    else:
        osb_file = OsuStoryboard(mapset_dir ,osb_filepath)
        unused_file = osb_file.detect_unused_file(mapset_dir)
        print(f'Unused files Count: {unused_file.__len__()}')
        print('Not completely sure if those files unused(if there any bugs). It is recommended to check it also with Mapset Verifier.')
        
        while True:
            
            print('1. Show unused files')
            print('2. Delete unused files')
            print('3. Exit')
            user_input = input('Please enter your choice: ')
            if user_input == '1':
                for file in unused_file:
                    print(file)
            elif user_input == '2':
                for file in unused_file:
                    os.remove(os.path.join(mapset_dir, file))
                    print(f'{file} has been deleted.')
            elif user_input == '3':
                break
            else:
                print('Invalid input, please try again.')

if __name__ == '__main__':
    main()