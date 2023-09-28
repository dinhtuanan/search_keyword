# 標準ライブラリ
import os
from datetime import datetime

# 外部ライブラリ
import glob
import pandas as pd

# 内部ライブラリ
from config.config import Config


class KeywordSearch():
    """
    Find specified keywords in files
    """
    def __init__(self) -> None:
        self._keyword_search_config = Config().get_search_keyword_config()
        self._input_folder = self._keyword_search_config['INPUT_FOLDER_PATH']
        self._result_folder = self._keyword_search_config['RESULT_FOLDER_PATH']
        os.makedirs(self._result_folder, exist_ok=True)
        self._result_file_path = os.path.join(self._result_folder, 'result.csv')
        
    def run(self):
        """
        Find all specify keywords in files
        """
        
        # search accepted extensions files
        files = self._get_accepted_files()
        
        # search keywords in files
        self._search_keywords_in_files(files)
        
        
    #######################################
    # private method
    #######################################
    def _get_accepted_files(self):
        """
        Find all file satisfy accepted extensions in input folder
        """
        accepted_extensions = self._keyword_search_config['ACCEPTED_EXTENSIONS']
        files = glob.glob(os.path.join(self._input_folder, '**/*'), recursive=True)
        print(files)
        accepted_files = [file for file in files if os.path.isfile(file) and file.endswith(tuple(accepted_extensions))]
        
        return accepted_files
    
    def _search_keywords_in_files(self, files: list):
        """
        Find lines contain keywords in files
        """
        for file in files:
            with open(file, 'r') as f:
                lines = f.readlines()
                
            # search keywords in lines
            result = self._search_keywords_in_lines(lines, file)
            
            # write result to csv file
            self._write_result_to_csv(result)
        
        
    def _search_keywords_in_lines(self, lines: list, file: str):
        """
        Find lines contain keywords in lines and lines number contain keywords
        """
        file_name = os.path.basename(file)
        keywords = self._keyword_search_config['KEYWORDS']
        result = []
        
        for line_number, line in enumerate(lines, start=1):
            is_found = False
            joined_keyword = ''
            for keyword in keywords:
                # lower keyword and line
                if keyword.lower() in line.lower():
                    is_found = True
                    joined_keyword = ','.join([joined_keyword, keyword])
            if is_found:
                result.append([file_name, line_number, "".join(line.split('\n')), joined_keyword])
        return result
    
    def _write_result_to_csv(self, result: list):
        """
        Write result to csv file
        """
        df = pd.DataFrame(result, columns=['file_name', 'line_number', 'line', 'keyword'])
        # check if df is empty
        if df.empty:
            return
        # add one empty line
        df = pd.concat([df, pd.DataFrame([['', '', '', '']], columns=['file_name', 'line_number', 'line', 'keyword'])])
        df = pd.concat([df, pd.DataFrame([['', '', '', '']], columns=['file_name', 'line_number', 'line', 'keyword'])])
        df.to_csv(self._result_file_path, mode='a', header=True, index=False)
            
if __name__ == '__main__':
    keyword_search = KeywordSearch()
    keyword_search.run()
    