import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1KOCWnVTb0fPb0EQgyDhAbk8TJPs1Q9LhbsfeEc2fLVxa2ncBT6AfIWdpnwjbhan9lmix0iR2yxyvMEfRaMl0oyrzLjykizMRlt5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:Maks13245612@localhost:3306/food_ordering_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False