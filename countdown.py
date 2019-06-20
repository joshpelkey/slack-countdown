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
    


def post(out, days_left=None):
    """ Posts a request to the slack webhook. Payload can be customized
    so the message in slack is customized. The variable out is the text 
    to be displayed.
    """    
    if days_left >= 0 and days_left < 100:
           
        images = [#0
                  "https://thumbs.gfycat.com/DevotedChubbyAmericansaddlebred-small.gif",
                  #1
                  "https://imageproxy.themaven.net/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fmaven-user-photos%2Ftexans%2Fgm-report%2FuMJXRw0oik2QbMktJSeE8A%2FK_eVJ930H0yGWKqZbBhpFA",
                  #2
                  "https://2cic.nyc3.cdn.digitaloceanspaces.com/t/stories/17/football/fields_mark_wf-479.jpg",
                  #3
                  "https://a4.espncdn.com/combiner/i?img=%2Fphoto%2F2019%2F0403%2Fr523837_1296x729_16%2D9.jpg",
                  #4
                  "https://cdn.vox-cdn.com/thumbor/ybAV3_EUnC4NHfZCjy3WNJ7CMRw=/0x0:2344x2990/1200x800/filters:focal(885x1384:1259x1758)/cdn.vox-cdn.com/uploads/chorus_image/image/52675689/usa_today_9801210.0.jpg",
                  #5
                  "https://imagesvc.timeincapp.com/v3/fan/image?url=https://rubbingtherock.com/wp-content/uploads/getty-images/2017/07/1052631268.jpeg&",
                  #6
                  "https://clemsontigers.com/wp-content/uploads/2015/09/AACJNTEHJQWCJNJ.20150908213636.jpg",
                  #7
                  "https://i.ytimg.com/vi/UzYuopje09w/hqdefault.jpg",
                  #8
                  "https://usatftw.files.wordpress.com/2019/01/gty-1079274016-e1546922077648.jpg?w=1000&h=600&crop=1",
                  #9
                  "https://clemsonpaws.com/wp-content/uploads/2018/06/Travis-Etienne.jpg",
                  #10
                  "https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fcdn-s3.si.com%2Fs3fs-public%2Fsi%2Fdam%2Fassets%2F13%2F03%2F20%2F130320111523-tajh-boyd-top-single-image-cut.jpg&w=1000&q=70",
                  #11
                  "https://www.nfldraftdiamonds.com/wp-content/uploads/2019/05/isaiah-simmons.jpg",
                  #12
                  "https://usattci.files.wordpress.com/2017/09/kvon-wallace.jpg?w=1000&h=600&crop=1",
                  #13
                  "https://usattci.files.wordpress.com/2019/01/hunter-renfrow.jpg?w=1000&h=600&crop=1",
                  #14
                  "https://www.gannett-cdn.com/presto/2018/09/01/PGRE/c3558a36-a175-4877-8fcb-6b3907065f64-uscpcent02-71plsdfz5up19n9jpkho_original.jpg?crop=2399,1343,x0,y0&width=3200&height=1680&fit=bounds",
                  #15
                  "https://c8.alamy.com/comp/RB973T/san-jose-ca-07th-jan-2019-clemson-tigers-linebacker-jake-venables-15-with-championship-belt-after-the-alabama-vs-clemson-national-championship-bay-area-game-at-levis-stadium-on-monday-santa-clara-california-usa-07th-jan-2019-photo-by-jevone-moore-credit-csmalamy-live-news-RB973T.jpg",
                  #16
                  "https://a57.foxnews.com/media2.foxnews.com/BrightCove/694940094001/2019/01/08/931/524/694940094001_5987127458001_5987117374001-vs.jpg?ve=1&tl=1",
                  #17
                  "https://usattci.files.wordpress.com/2017/04/cornell-powell.jpg?w=1000&h=600&crop=1",
                  #18
                  "https://fwzeqk07ei-flywheel.netdna-ssl.com/wp-content/uploads/2019/01/T.J.Chase11.DT_-768x512.jpg",
                  #19
                  "https://www.gannett-cdn.com/presto/2018/10/07/PGRE/8c1e72b5-880d-43b2-becf-6a404cc60b8e-WF_CU_1571.jpg?crop=1799,1012,x0,y33&width=3200&height=1680&fit=bounds",
                  #20
                  "https://bloximages.newyork1.vip.townnews.com/scnow.com/content/tncms/assets/v3/editorial/1/98/198ad1be-664a-11e2-9a2f-0019bb30f31a/51016d2a7d995.image.jpg?resize=400%2C266",
                  #21
                  "https://media.gettyimages.com/photos/kyler-mcmichael-of-the-clemson-tigers-in-action-during-the-game-the-picture-id1062809560",
                  #22
                  "https://www.thestate.com/latest-news/ahhnkg/picture221160070/alternates/FREE_1140/11.03.18.will.swinney.2%20(1).JPG",
                  #23
                  "https://i.ytimg.com/vi/nDMs1jGifGc/maxresdefault.jpg",
                  #24
                  "https://www.gannett-cdn.com/presto/2018/12/30/PGRE/0aa745b3-b81c-4f52-9f1a-cd2800f923a3-_Cotton_Bowl_003919.jpg?crop=2399,1355,x0,y540&width=3200&height=1680&fit=bounds",
                  #25
                  "https://www.star-telegram.com/latest-news/4i6oj8/picture224001590/alternates/FREE_1140/J.C.Chalk.CA.jpg",
                  #26
                  "https://i.ebayimg.com/images/g/TAAAAOSwX99ZmjmF/s-l300.jpg",
                  #27
                  "https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fcdn-s3.si.com%2Fs3fs-public%2Fstyles%2Fmarquee_large_2x%2Fpublic%2F2018%2F12%2F11%2Fcj_fuller_died_of_blood_clot_in_lung.jpg%3Fitok%3DtRZIc4W0&w=1000&q=70",
                  #28
                  "https://clemsontigers.com/wp-content/uploads/2013/08/DASDODSVIOHXDVG.20130816190911.jpg",
                  #29
                  "https://usattci.files.wordpress.com/2018/09/b-t-potter.jpg?w=243&h=300",
                  #30
                  "https://usattci.files.wordpress.com/2017/06/jalen-williams.jpg?w=1000&h=600&crop=1",
                  #31
                  "https://editorial01.shutterstock.com/wm-preview-1500/9877378e/bafdf977/ncaa-football-clemson-vs-texas-a-m-college-station-usa-shutterstock-editorial-9877378e.jpg",
                  #32
                  "http://www3.pictures.zimbio.com/gi/Andy+Teasdall+PlayStation+Fiesta+Bowl+Ohio+KUGrUzm1rbul.jpg",
                  #33
                  "https://usattci.files.wordpress.com/2018/07/j-d-davis.jpg?w=1000&h=600&crop=1",
                  #34
                  "https://steelcityblitz.com/wp-content/uploads/2019/04/Joseph.jpg",
                  #35
                  "https://www.gastongazette.com/storyimage/NC/20180719/SPORTS/180718030/AR/0/AR-180718030.jpg",
                  #36
                  "https://c8.alamy.com/comp/RCBE80/arlington-tx-usa-29th-dec-2018-clemson-linebacker-judah-davis-36-in-action-at-the-ncaa-football-cotton-bowl-between-the-clemson-tigers-and-the-notre-dame-fighting-irish-at-att-stadium-in-arlington-tx-absolute-complete-photographer-company-credit-joe-calomenimarinmediaorgcal-sport-media-credit-csmalamy-live-news-RCBE80.jpg",
                  #37
                  "https://media.gettyimages.com/photos/kantrell-brown-of-the-clemson-tigers-runs-downfield-on-kick-coverage-picture-id129591761",
                  #38
                  "https://bloximages.newyork1.vip.townnews.com/postandcourier.com/content/tncms/assets/v3/editorial/3/4a/34a8ffc5-7136-544e-ab36-98f781483a81/59ab315053934.image.jpg?crop=1401%2C856%2C0%2C17&resize=400%2C244&order=crop%2Cresize",
                  #39
                  "http://www3.pictures.zimbio.com/gi/Chandler+Catanzaro+Chick+fil+Bowl+LSU+v+Clemson+mcqlin-l0fhl.jpg",
                  #40
                  "http://www4.pictures.zimbio.com/gi/Darrell+Smith+Clemson+v+North+Carolina+State+1O6rtSMtes4l.jpg",
                  #41
                  "https://bloximages.newyork1.vip.townnews.com/scnow.com/content/tncms/assets/v3/editorial/1/ab/1abefec8-088f-11e9-9a49-87c85314a368/5c22a68969aef.image.jpg",
                  #42
                  "https://usatdraftwire.files.wordpress.com/2018/04/usatsi_9691161.jpg?w=1000&h=600&crop=1",
                  #43
                  "https://c8.alamy.com/comp/RCBD3D/arlington-tx-usa-29th-dec-2018-clemson-defensive-tackle-chad-smith-43-in-action-at-the-ncaa-football-cotton-bowl-between-the-clemson-tigers-and-the-notre-dame-fighting-irish-at-att-stadium-in-arlington-tx-absolute-complete-photographer-company-credit-joe-calomenimarinmediaorgcal-sport-media-credit-csmalamy-live-news-RCBD3D.jpg",
                  #44
                  "https://2cic.nyc3.cdn.digitaloceanspaces.com/t/stories/18/football/pinckney_nyles_gt_800-479.jpg",
                  #45
                  "https://media.gettyimages.com/photos/clemson-tigers-defensive-end-chris-register-prepares-to-make-the-play-picture-id1047740352",
                  #46
                  "https://sites.google.com/a/g.clemson.edu/cmricha/_/rsrc/1415071790708/home/photo.JPG?height=400&width=271",
                  #47
                  "https://f5s009media.blob.core.windows.net/photos/0032984-bekx-1280x720.jpg",
                  #48
                  "https://usattci.files.wordpress.com/2017/07/will-spiers.jpg?w=1000&h=600&crop=1",
                  #49
                  "https://cdn.vox-cdn.com/thumbor/l3x2XTnUBd1GwYD8GkWcCy2bYgo=/0x0:5472x3648/1200x800/filters:focal(2299x1387:3173x2261)/cdn.vox-cdn.com/uploads/chorus_image/image/61001379/usa_today_9835932.0.jpg",
                  #50
                  "https://usattci.files.wordpress.com/2018/06/justin-falcinelli.jpg?w=1000&h=600&crop=1",
                  #51
                  "https://usattci.files.wordpress.com/2017/02/taylor-hearn-natty.jpg?w=1000&h=600&crop=1",
                  #52
                  "https://c8.alamy.com/comp/RCBD1N/arlington-tx-usa-29th-dec-2018-clemson-player-austin-spence-52-in-action-at-the-ncaa-football-cotton-bowl-between-the-clemson-tigers-and-the-notre-dame-fighting-irish-at-att-stadium-in-arlington-tx-absolute-complete-photographer-company-credit-joe-calomenimarinmediaorgcal-sport-media-credit-csmalamy-live-news-RCBD1N.jpg",
                  #53
                  "https://editorial01.shutterstock.com/wm-preview-1500/9629348n/cba4ffd7/ncaa-football-clemson-spring-game-clemson-usa-shutterstock-editorial-9629348n.jpg",
                  #54
                  "https://c8.alamy.com/comp/K3G5TW/clemson-defensive-end-logan-rudolph-54-during-the-ncaa-college-football-K3G5TW.jpg",
                  #55
                  "https://usattci.files.wordpress.com/2017/03/tyrone-crowder.jpg?w=1000&h=600&crop=1",
                  #56
                  "https://clemsontigers.com/wp-content/uploads/2016/10/MMKSXFNULCPYMBB.20161011182420.jpg",
                  #57
                  "https://usattci.files.wordpress.com/2019/01/tre-lamar-1.jpg?w=1000&h=600&crop=1",
                  #58
                  "https://c8.alamy.com/comp/PXBRNH/clemson-tigers-defensive-tackle-jordan-williams-59-during-the-ncaa-college-football-game-between-nc-state-and-clemson-on-saturday-october-20-2018-at-memorial-stadium-in-clemson-sc-jacob-kupfermancsm-PXBRNH.jpg",
                  #59
                  "https://usattci.files.wordpress.com/2019/02/gage-cervenka-1.jpg?w=1000&h=600&crop=1",
                  #60
                  "https://media.gettyimages.com/photos/jesse-pickens-of-the-clemson-tigers-rests-betweeen-plays-during-a-picture-id53567178",
                  #61
                  "https://lh3.googleusercontent.com/-v3BouxrDaYo/UKU9tICl2eI/AAAAAAAAotI/sJsanS4pAZc/s800/DSC_0187.jpg",
                  #62
                  "https://s3media.247sports.com/Uploads/Assets/761/640/8640761.jpg",
                  #63
                  "https://cdn.vox-cdn.com/thumbor/ok4sldLBDn6Y3GG4I0esGskHJMQ=/0x0:1926x2780/1200x800/filters:focal(532x727:840x1035)/cdn.vox-cdn.com/uploads/chorus_image/image/53634513/usa_today_9288226.0.jpg",
                  #64
                  "https://clemsonpaws.com/wp-content/uploads/2017/07/Pat-Godfrey.jpg",
                  #65
                  "https://pbs.twimg.com/profile_images/1116946681306730496/6T7xngOa_400x400.jpg",
                  #66
                  "http://www.soconsports.com/pics31/1024/HQ/HQPPHOFVIWADLXP.20100805163708.jpg", 
                  #67
                  "https://usattci.files.wordpress.com/2019/01/albert-huggins.jpg?w=1000&h=600&crop=1", 
                  #68
                  "https://farm4.static.flickr.com/3837/15381327526_32a0b40355_b.jpg", 
                  #69
                  "https://clemsontigers.com/wp-content/uploads/2016/10/ZSQJAXFUCQNROJT.20161028153755.jpg",
                  #70
                  "https://www.gannett-cdn.com/presto/2019/01/07/PNDN/4b18afc0-38b9-4c1e-b3cd-469cd0cb723a-USATSI_10456727.jpg?width=534&height=712&fit=bounds&auto=webp", 
                  #71
                  "https://media.gettyimages.com/photos/clemson-tigers-long-snapper-jack-maddox-warms-up-before-the-college-picture-id900524032", 
                  #72
                  "https://ssl.c.photoshelter.com/img-get/I0000nELU1j6d4us/s/880/880/CFS-DKS-110917402.jpg",
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
        
        img_url = images[days_left]
                  
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
        if days_left >= 0 and days_left < 100:
            post(result, days_left)
        else:
            post(result)
        


@manager.command
def initiate():
    payload = { "text": "App is now connected to your Slack Channel."}
    r = requests.post(SLACK_URL, data=json.dumps(payload))
    
    

    
if __name__ == "__main__":
    manager.run()


