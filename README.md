## Tạo môi trường anaconda
1. conda create -n searchKeyword python=3.9
2. pip install -r requirements.txt

## I/F抽出実行
1. Change the contents of config\config.ini for the target input folder.
2. Run python keyword_search.py
3. Store the results in the result folder.

## Test
1. cd test
1. python test_keyword_search.py TestKeywordSearch.test_run