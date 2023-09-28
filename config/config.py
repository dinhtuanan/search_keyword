# coding: utf-8
"""
アプリ設定情報


"""
# 標準ライブラリ
import os
import sys
import configparser
import types
from threading import Lock


class SingletonConfig(type):
    """
    Configのインスタンスを一つにするクラス
    """
    _instance = None
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Config(metaclass=SingletonConfig):
    # *****************************************************************************************************************
    # 公開クラス変数
    # *****************************************************************************************************************

    # *****************************************************************************************************************
    # 内部クルス変数
    # *****************************************************************************************************************
    __CONFIG_FILES = {
        # 公開設定情報
        'config': 'config.ini',
    }

    # 初期化処理
    def __init__(self):
        """
        Calling::
            obj.Config()

        Args::

        Returns::
            None

        Raises::
            None
        """
        if getattr(sys, 'frozen', False):
            current_dir = os.path.dirname(os.path.abspath(sys.executable))
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_dir,
                                       Config.__CONFIG_FILES['config'])

        self.__config = self.__read_config_file(config_file)

    @staticmethod
    def __read_config_file(config_file_path) -> dict:
        """
        Args:
            config_file_path (str)  : 設定ファイルパス

        Returns:
            config (dict)       : アプリ設定情報

        """
        print("config_file_path = {}".format(config_file_path))
        assert (os.path.exists(config_file_path))

        config = configparser.ConfigParser()
        config.optionxform = str  # 大文字と小文字を区別するため
        config.read(config_file_path, encoding="utf-8")

        return dict(config)

    @staticmethod
    def __convert_type(config_info):
        """
        設定情報
        Args:
            config_info (section):設定情報

        Returns:
            result_info (dict)
        """
        result_info = dict()

        for key, value in config_info.items():
            try:
                result_info[key] = eval(value)

                if isinstance(eval(value), types.BuiltinFunctionType):
                    result_info[key] = value

            except (NameError, TypeError, SyntaxError):
                result_info[key] = value

        return result_info

    # *****************************************************************************************************************
    # 公開関数
    # *****************************************************************************************************************
    
    def get_search_keyword_config(self) -> dict:
        """
        Get search file config
        """
        try:
            res = self.__convert_type(self.__config['SEARCH_KEYWORD'])
        except KeyError:
            res = None
        return res

