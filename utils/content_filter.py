import re

def filter_emoji(raw_str):
    """[filter emoji in tweet content]
    Args:
        raw_str ([str]): [origin tweet content]
    Returns:
        [str]: [tweet content after filter emoji]
    """
    restr = ''
    try:
        res = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        res = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return res.sub(restr, raw_str)



def count(heat_data):
    """[change "K" to 1000 to count nums of heat data(reply,retweet,like)]
    Args:
        heat_data ([str]): [raw heat data]
    Returns:
        [int]: [nums of heat data]
    """
    if heat_data != "":
        if 'K' in heat_data:
            if "," in heat_data:
                heat_data = heat_data.replace(',','')  #remove ","
            heat_data = heat_data.replace('K','')  # change "K" to 1000
            num = int(float(heat_data) * 1000)
        elif "万" in heat_data:
            if "," in heat_data:
                heat_data = heat_data.replace(',','')  #remove ","
            heat_data = heat_data.replace('万','')  # change "万" to 10000
            num = int(float(heat_data) * 10000)
        elif "千" in heat_data:
            if "," in heat_data:
                heat_data = heat_data.replace(',','')  #remove ","
            heat_data = heat_data.replace('千','')  # change "万" to 10000
            num = int(float(heat_data) * 1000)
        elif "," in heat_data:
            heat_data = heat_data.replace(',','')  #remove ","
            num = int(heat_data) #remove ","
        else:
            num = int(heat_data)
    else:
        num = 0
    return num                                     # if num of heat data(reply,retweet,like) is zero, return 0


