import datetime
class env():
    PRODUCTION = "production"
    TEST = "test"
    MEMORY = "in-memory"

class cache_time():
    ONE_HOUR = 3600
    HALF_HOUR = 1800
    END_CURRENT_DAY = ((24 - datetime.datetime.now().hour) * 60 * 60) - (datetime.datetime.now().minute * 60)

class regex_pattern():
    NON_WORDS="\s|\W|\d"
    LAT_LNG="^-?\d{2}.\d{5,15}$"

class msgs():
    USER_NOT_FOUND="Error to add place, user not found."

