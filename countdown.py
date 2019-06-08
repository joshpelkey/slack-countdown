#!/usr/bin/python
from flask.ext.script import Manager
from flask import Flask
from datetime import datetime
import json
import os
import requests
import workdays

app = Flask(__name__)


manager = Manager(app)

"""Creates web app to be deployed on Heroku."""

SLACK_URL = os.environ.get('SLACK_URL')
if not SLACK_URL:
    print("Missing environment variable SLACK_URL")
    exit(1)

def days_from_christmas():
    """Calculates the number of days between the current date and the next 
    Christmas. Returns the string to displayed.
    """
    currentdate = datetime.now()
    christmas = datetime(datetime.today().year, 12, 25)
    if christmas < currentdate:
        christmas = date(datetime.today().year + 1, 12, 25)
    delta = christmas - currentdate
    days = delta.days
    if days == 1:
        return "%d day from the nearest Christmas" % days
    else:
        return "%d days from the nearest Christmas" % days


def days_from_date(strdate, business_days):
    """ Returns the number of days between strdate and today. Add one to date
    as date caclulate is relative to time
    """
    currentdate = datetime.today()
    futuredate = datetime.strptime(strdate, '%Y-%m-%d')
    if business_days:
        delta = workdays.networkdays(currentdate, futuredate)
    else:
        delta = (futuredate - currentdate).days + 1
    return delta

    
def events(strdate, event, business_days):
    """ Returns string to be displayed with the event mentioned. Sends an error
    if date is incorrect
    """
    days = days_from_date(strdate, business_days)
    day_qualifier = ""
    if business_days:
        day_qualifier = "business "
    assert (days >= -2), "Date needs to be in the future"
    if days == -1:
        return "%d %sday since %s" % (1, day_qualifier, event)
    elif days == -2:
        return "%d %sdays since %s" % (2, day_qualifier, event)
    elif days == 1:
        return "%d %sday until %s" % (days, day_qualifier, event)
    else:
        return "%d %sdays until %s" % (days, day_qualifier, event)


def date_only(strdate, business_days):
    """ Returns string to be displayed. Sends error message if date is
    in the past
    """
    days = days_from_date(strdate)
    day_qualifier = ""
    if business_days:
        day_qualifier = "business "
    assert (days >= -2), "Date needs to be in the future"
    futuredate = datetime.strptime(strdate, '%Y-%m-%d')
    if days == -1:
        return "%d %sday since %s" % (1, day_qualifier, futuredate.strftime("%d %B, %Y"))
    if days == -2:
        return "%d %sdays since %s" % (days, day_qualifier, futuredate.strftime("%d %B, %Y")) 
    if days == 1:
        return "%d %sday until %s" % (days, day_qualifier, futuredate.strftime("%d %B, %Y")) 
    else:
        return "%d %sdays until %s" % (days, day_qualifier, futuredate.strftime("%d %B, %Y"))
    


def post(out, days_left):
    """ Posts a request to the slack webhook. Payload can be customized
    so the message in slack is customized. The variable out is the text 
    to be displayed.
    """    
    if days_left:
           
        images = [#1
                  "", 
                  #2
                  "", 
                  #3
                  "", 
                  #4
                  "", 
                  #5
                  "", 
                  #6
                  "", 
                  #7
                  "", 
                  #8
                  "", 
                  #9
                  "", 
                  #10
                  "", 
                  #11
                  "", 
                  #12
                  "", 
                  #13
                  "", 
                  #14
                  "", 
                  #15
                  "", 
                  #16
                  "", 
                  #17
                  "", 
                  #18
                  "", 
                  #19
                  "", 
                  #20
                  "", 
                  #21
                  "", 
                  #22
                  "", 
                  #23
                  "", 
                  #24
                  "", 
                  #25
                  "", 
                  #26
                  "", 
                  #27
                  "", 
                  #28
                  "", 
                  #29
                  "", 
                  #30
                  "", 
                  #31
                  "", 
                  #32
                  "", 
                  #33
                  "", 
                  #34
                  "", 
                  #35
                  "", 
                  #36
                  "", 
                  #37
                  "", 
                  #38
                  "", 
                  #39
                  "", 
                  #40
                  "", 
                  #41
                  "", 
                  #42
                  "", 
                  #43
                  "", 
                  #44
                  "", 
                  #45
                  "", 
                  #46
                  "", 
                  #47
                  "", 
                  #48
                  "", 
                  #49
                  "",
                  #50
                  "", 
                  #51
                  "", 
                  #52
                  "", 
                  #53
                  "", 
                  #54
                  "", 
                  #55
                  "", 
                  #56
                  "", 
                  #57
                  "", 
                  #58
                  "", 
                  #59
                  "",
                  #60
                  "", 
                  #61
                  "", 
                  #62
                  "", 
                  #63
                  "", 
                  #64
                  "", 
                  #65
                  "", 
                  #66
                  "", 
                  #67
                  "", 
                  #68
                  "", 
                  #69
                  "",
                  #70
                  "", 
                  #71
                  "", 
                  #72
                  "",
                  #73
                  "https://clemsonpaws.com/wp-content/uploads/2016/07/Tremayne-Anchrum.jpg", 
                  #74
                  "https://bloximages.newyork1.vip.townnews.com/postandcourier.com/content/tncms/assets/v3/editorial/3/1e/31e09354-eb31-11e7-91a4-dfcab8482f44/5a43e22e7907d.image.jpg?resize=1200%2C1329", 
                  #75
                  "https://images2.minutemediacdn.com/image/upload/c_fill,w_912,h_516,f_auto,q_auto,g_auto/shape/cover/sport/cfp-national-championship-5bdde43404bc97a939000008.jpg", 
                  #76
                  "https://usattci.files.wordpress.com/2017/01/sean-pollard.jpg?w=1000&h=600&crop=1", 
                  #77
                  "https://nbccollegefootballtalk.files.wordpress.com/2019/01/gettyimages-1067333440-e1548777834805.jpg?w=610&h=343&crop=1", 
                  #78
                  "https://c8.alamy.com/comp/F87R19/clemson-offensive-lineman-eric-mac-lain-78-during-the-acc-college-F87R19.jpg", 
                  #79
                  "https://i3.tigernet.com/stories/18/football/carman_jackson_handsup_800-479.jpg", 
                  #80
                  "https://bloximages.newyork1.vip.townnews.com/postandcourier.com/content/tncms/assets/v3/editorial/8/89/8890b512-9019-11e7-9574-73a4610b6a14/59ab0e23c1250.image.jpg?resize=400%2C287", 
                  #81
                  "https://editorial01.shutterstock.com/wm-preview-1500/7688279eq/dd2198ba/playoff-fiesta-bowl-football-glendale-usa-shutterstock-editorial-7688279eq.jpg", 
                  #82
                  "https://c8.alamy.com/comp/R09NWR/clemson-south-carolina-usa-03rd-nov-2018-clemson-tigers-wide-receiver-will-brown-82-before-the-ncaa-college-football-game-between-louisville-and-clemson-on-saturday-november-3-2018-at-memorial-stadium-in-clemson-sc-jacob-kupfermancsm-credit-cal-sport-mediaalamy-live-news-R09NWR.jpg", 
                  #83
                  "https://lh6.googleusercontent.com/-nzZLAbeSkJI/UIgjZwvm6qI/AAAAAAABT1E/hJbp3YIwl6c/s1600/TNT_7222.jpg", 
                  #84
                  "", 
                  #85
                  "", 
                  #86
                  "", 
                  #87
                  "", 
                  #88
                  "", 
                  #89
                  "", 
                  #90
                  "", 
                  #91
                  "", 
                  #92
                  "", 
                  #93
                  "", 
                  #94
                  "", 
                  #95
                  "", 
                  #96
                  "", 
                  #97
                  "", 
                  #98
                  "",
                  #99
                  ""
                 ]
        
        img_url = images[days_left - 1]
                  
        payload = {
            "attachments": [
                {   
                    "title": "COUNTDOWN!",
                    "text": out,
                    "color": "#F66733",
                    "image_url": img_url
                }
            ]
        }
    else:
        payload = {
            "attachments": [
                {   
                    "title": "COUNTDOWN!",
                    "text": out,
                    "color": "#F66733"
                }
            ]
        }
    
    r = requests.post(SLACK_URL, data=json.dumps(payload))


def post_error():
    """Sends error message in Slack to alert the user
    about the incorrect date argument
    """
    
    payload = {
        "attachments": [
            {
                "title": "Error",
                "text": ("Date entered must be in the future. "
                        "\n Go to the <https://heroku.com|Heroku Scheduler> for you app and edit"
                        " the command"),
                        "color": "#525162"
            }
        ]
    }
    
    r = requests.post(SLACK_URL, data=json.dumps(payload))
 

@manager.option("-d", "--deadline", dest="date",
                      help="Specify the deadline in ISO format: yyyy-mm-dd", 
                      metavar="DEADLINE")
@manager.option("-e", "--event", dest="event", 
                      help="Name of the deadline event",metavar="EVENT")
@manager.option("-b", "--business-days", dest="business_days", action="store_true", 
                      help="Give the count of business days only")
def deadline(date, event, business_days):
    """ Method takes two optional arguments. Displays in slack channel
    the number of days till the event. If no arguments are given,
    the number of days till Christmas is displayed.
    """    
    try:
        result = ""
        if date:
            if event:
                result = events(date, event, business_days)
            else:
                result = date_only(date, business_days)
        else:
            result = days_from_christmas()
    except:
        post_error()
    else:
        days_left = days_from_date(date, business_days)
        if days_left > 0 and days_left < 100:
            post(result, days_left)
        else:
            post(result)
        


@manager.command
def initiate():
    payload = { "text": "App is now connected to your Slack Channel."}
    r = requests.post(SLACK_URL, data=json.dumps(payload))
    
    

    
if __name__ == "__main__":
    manager.run()


