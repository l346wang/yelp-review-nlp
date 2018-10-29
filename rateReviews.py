from pymongo import MongoClient
import pymongo
from config import MONGO_DB_ADDRESS
from constants import SYMBOLS_REGEX

import statistics
import nltk
import starWordCount
import collections

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
yelp_database = client['yelp']
words_hit_count_collection = yelp_database['words_hit_count']
processed_reviews_collection = yelp_database['processed_reviews']

star_word_count_dict = starWordCount.count_word_of_each_star()
# print(star_word_count_dict)


def add_to_wd(wd, w, k):
    w_string = w[k]
    if w_string in wd:
        wd[w_string].append(w)
    else:
        wd[w_string] = [w]


def rate_review(text):
    tokens = nltk.word_tokenize(text)
    result = words_hit_count_collection.find({
        'word': {
            "$in": tokens
        }
    })
    word_dict = dict()
    for doc in result:
        add_to_wd(word_dict, doc, 'word')
    word_predict_rate = dict()
    # build word count
    for word, list_of_stars in word_dict.items():
        word_predict_rate[word] = dict()
        for doc in list_of_stars:
            star = doc['stars']
            word_count = doc['count']
            total_words = star_word_count_dict[star]['total_words']
            word_predict_rate[word][star] = total_words / word_count

    word_guess_dict = dict()

    for word in word_predict_rate:
        sum = 0
        word_star_score = word_predict_rate[word]
        score_list = []
        for star in word_star_score:
            score = word_star_score[star]
            score_list.append(score)
            sum += score
        if len(score_list) == 1:
            # if only one matches, set the match to that one
            word_guess_dict[word] = list(word_star_score.keys())[0]
            continue
        # print(word)
        # print(score_list)
        # print(statistics.stdev(score_list))
        standard_deviation = statistics.stdev(score_list)
        k = 100
        # if standard_deviation < k, ignore the word
        if standard_deviation < k:
            continue
        # print(word)
        # print(score_list)
        # print(statistics.stdev(score_list))
        the_key_of_min_score = min(word_star_score, key=word_star_score.get)
        word_guess_dict[word] = the_key_of_min_score
    # print('------------------')

    counter = collections.Counter(word_guess_dict.values())
    max_star = max(counter, key=counter.get)
    probability = counter[max_star] / len(word_guess_dict)
    print(counter)
    print('predicted star: ' + str(max_star))
    sure_probability = probability / 0.3 - 1
    print('sure_probability: ' + str(sure_probability))
    return max_star


def rate_reviews():
    n = 100
    result = processed_reviews_collection.aggregate([
        {
            '$sample':
                {
                    'size':  n,
                },
        }
    ])
    correct_cases = 0

    for doc in result:
        print('stars: ' + str(doc['stars']))
        predicted_star = rate_review(doc['text'])
        if predicted_star == doc['stars']:
            correct_cases += 1
        print('--------------')
    print('correct cases: ' + str(correct_cases))


if __name__ == '__main__':
    rate_reviews()
    # result = words_hit_count_collection.find_one({
    #     'word': 'wonderful',
    # })
    # print(result)
