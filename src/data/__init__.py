from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

if __name__ == '__main__':
    print(type(DATA_DIR))
    print('**1', DATA_DIR)
    print('***2',DATA_DIR /'pytopia.json') #--> concatinating to Path object using / character
    print('****3',DATA_DIR / 'online.json')

