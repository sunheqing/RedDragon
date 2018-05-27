#coding=utf-8
from SPARK import RecommendationEngine
from pyspark import SparkContext, SparkConf

TOTAL_USERS = 0
TOTAL_MOVIES = 0
RECOMMEND_NUMS = 5
DEBUG = True
def run_recommond(ID):
    conf = SparkConf().setAppName("recommond")
    sc = SparkContext(conf=conf)
    dataset_path = r'D:\app\python\RedDragon\recommend\dataset\data_model'
    RE = RecommendationEngine(sc, dataset_path)
    top_ratings = RE.get_top_ratings(user_id=ID, movies_count=10)
    try:
        sc.stop()
    except:
        pass
    return top_ratings


#print run_recommond(33)