import sys
if "C:\\Users\\Asronic\\MehrdadDir\\Telegram-statistics" not in sys.path:
    sys.path.append("C:\\Users\\Asronic\\MehrdadDir\\Telegram-statistics")

import json
from pathlib import Path
from typing import Union

import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from src.data import DATA_DIR  # in the __init__ file in the data folder
from wordcloud import WordCloud
from loguru import logger


class ChatStatistics:
    """
    Generate chat statistics from a  Telegram group chat jason file
    """


    def __init__(self, chat_json: Union[str, Path]): # For code readability--> chat_json is a str or an object of type Path
        """_summary_

        Args:
            chat_json (Union[str, Path]): Path to telegram json file 
        """
        
        # load chat data 
        logger.info(f"Loading chat data from {chat_json} ")

        with open(chat_json, encoding='utf8') as f:
            self.chat_data =json.load(f)

        self.normalizer = Normalizer()

        # load stopwords 
        logger.info(f"Loading chat data from {DATA_DIR/'stopwords_Farsi.tx'}")

        with open(DATA_DIR / 'stopwords_Farsi.txt', encoding='utf8') as file:
            self.stopwords = file.readlines() # -->  type:list
            self.stopwords = list(map(str.strip, self.stopwords)) # --> Deleting \n at the end of stopwords
            self.stopwords = list(map(self.normalizer.normalize, self.stopwords))

    def generate_word_cloud(self, output_dir,
                            width: int = 1000,
                            height: int = 1000,
                            max_font_size: int = 250):

        # generate text content
        logger.info("Loading text conten ...")
        
        text_content = ''
        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda token: token not in self.stopwords, tokens))# --> removing stopwords
                filterd_msg = " ".join(tokens) # --> reconstructing messages after removing stopwords 
                text_content += f" {filterd_msg}"

        # normalize, reshape for final wordcloud
        logger.info("Generating word cloud ...")

        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)

        #generate wordcloud object
        word_cloud = WordCloud(
            font_path= str(DATA_DIR / 'BHoma.ttf'), 
            background_color='white',
            max_font_size=max_font_size,
            width=width,
            height=height,
             ).generate(text_content)

        logger.info(f"Saving word cloud to \"{output_dir}\"")

        word_cloud.to_file(str(Path(output_dir) / 'wordcloud.png')) # --> output_dir should be of type Path because we used /
                

if __name__ == '__main__':
    chat_stats = ChatStatistics(chat_json=(DATA_DIR / 'online.json'))
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)
    print('!!!Done!!!')
