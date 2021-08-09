import datetime
class env():
    PRODUCTION = "production"
    TEST = "test"

class cache_time():
    ONE_HOUR = 3600
    END_CURRENT_DAY = ((24 - datetime.datetime.now().hour) * 60 * 60) - (datetime.datetime.now().minute * 60)

class regex_pattern():
    NON_WORDS="\s|\W|\d"


