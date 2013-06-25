import csv, numpy, re,operator
from datetime import datetime
from dateutil import relativedelta
from scipy import stats
import matplotlib.pyplot as plt
import math

#read_file = "3-15-13.csv"
read_file = "Corrected-3-15-13.csv"

stories = []
current_year_month_day = 2013,03,14

def convert_date(mmddyy):
    if mmddyy =='':
        return ''
    # mm-dd-yy to yyyy,mm,dd
    year = mmddyy[-2:]
    if int(year) < 90:
        year = '20'+year
    else:
        year = '19' + year
        if int(year)>2020:
            print "BLARG"
            print mmddyy

    month = mmddyy[:2]
    if month[1] =="-":
        month ='0'+month[0]
        day = mmddyy[2:4]
    else:
        day = mmddyy[3:5]
    if day[1] =="-":
        day = '0'+day[0]
    a = datetime(int(year),int(month),int(day))
    if a ==None or a =='':
        print "datetime returned none"
        print mmddyy
    else:
        return a

def string_to_int(x): 
    try:
        return int(x.replace(",",""))
    except ValueError:
        pass

def unix_date_to_american_date(unix_date):
    if unix_date =='':
        return ''
    else:
        return str(unix_date.month)+'-'+str(unix_date.day)+'-'+str(unix_date.year)

ratings_list = []
favorites_list = []
reviews_list = []
oneshots_list = []

class story:
    global ratings_list
    global favorites_list
    global reviews_list
    global oneshots_list

    def __init__(self,(rating, updated, favorites, staringchars, chapters,complete,collected_info,genre,desc,language,author,url,follows,title,reviews,published,words)):
        self.rating=rating
        ratings_list.append(rating)
        self.updated = convert_date(updated)
        if favorites == '': favorites = 0
        self.favorites = int(favorites)
        favorites_list.append(self.favorites)
        if staringchars =='':
            staringchars = 'Unspecified'
        self.staringchars = staringchars
        self.chapters = chapters
        if complete == "True": self.complete = True 
        else: self.complete = False
        self.collected_info = collected_info
        self.genre = genre
        self.desc = desc
        self.language = language
        self.author = author
        self.url = url
        if follows =='': follows = 0
        self.follows = int(follows)
        self.title = title
        if reviews == '': reviews = 0
        self.reviews = int(reviews)
        reviews_list.append(self.reviews)
        self.published = convert_date(published)
        self.words = map (string_to_int, words.split('"'))[0]
        #self.words = words

        # determine if fanfiction has been abandoned
        was_updated = False
        if self.complete ==True:
            # not abandoned
            self.abandoned = 0
        else:
            if self.updated:
                compare_to = self.updated
                was_updated = True
            else:
                compare_to = self.published
            delta = relativedelta.relativedelta(compare_to,datetime(*current_year_month_day))
            if abs(delta.years) > 1 or abs(delta.months) > 6:
                if was_updated:
                    # abandoned
                    self.abandoned = 1
                else:
                    # abandoned, never updated
                    self.abandoned = 2
            else:
                # probably not abandoned
                self.abandoned = 3

        # determine if it's a oneshot
        if self.complete == True and self.updated == None or self.updated =='':
            self.oneshot = True
#            oneshots_list.append(self)
        else:
            self.oneshot = False



with open(read_file, 'rb') as csvfile:
#with open('additional.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    # skip header
    next(csvfile)
    for row in reader:
        if len(row)<2:
            print "passing row"
            pass
        else:
            stories.append(story(row))        

changed_stories = 0
new_stories = []
for Story in stories:
#If the data was split up incorrectly, parse each field individually. This increases the chance of some errors, such as if there were a character named 'published: ', but it more flexibly handles presence and absence of data than the way in which the data was initially split
    if Story.collected_info!= None and len(Story.collected_info)>0 and (Story.published == None or Story.published.year > 2020 or Story.published.year < 1980 or Story.staringchars=="Complete"):
        try:
            new_story_follows = re.search('- Follows: ([0-9])+',Story.collected_info).group(1)
        except:
            new_story_follows = 0
#            print "follows not specified"
        try:
            new_story_rating = re.search('Rated: (\w\+*\-*)',Story.collected_info).group(1)
        except:
            new_story_rating = ''
#            print "rating not specified"
        try:
            new_story_language = re.search('Rated: \w\+*\-* - (\w+)',Story.collected_info).group(1)
        except:
            new_story_language = ''
#            print "Language not specified"

        try:
            new_story_genre = re.search('\w+ - (\w+/*\w*) - Chapters:',Story.collected_info).group(1)
        except:
            new_story_genre = ''
#            print "Genre not specified"
        try:
            new_story_chapters = re.search('Chapters: ([0-9]+)',Story.collected_info).group(1)
        except:
            # assume if chapters aren't specified that they equal 1
            new_story_chapters = 1
#            print "Chapter count not specified"
        try:
            new_story_words = re.search('Words: ([0-9]+)',Story.collected_info).group(1)
        except:
            new_story_words = ''
#            print "Word count not specified?"
        try:
            new_story_reviews = re.search('Reviews: ([0-9]+)',Story.collected_info).group(1)
        except:
            new_story_reviews = 0
#            print "Story not reviewed?"
        try:
            new_story_favs = re.search('Favs: ([0-9]+)',Story.collected_info).group(1)
        except:
            new_story_favs = 0
#            print "Story not favorited?"
        try:
            new_story_published = re.search('- Published: ([0-9]+\-[0-9]+\-[0-9]+)',Story.collected_info).group(1)
            # deal with the story that was supposedly published in '69
#            if new_story_published[-2:]=='69':
 #               new_story_published = ''
        except:
#            print "Publishing date not specified?"
            new_story_published = ''
        if re.search('- Complete',Story.collected_info):
            new_story_complete = 'Complete'
        else:
            new_story_complete = 'False'

        try:
            new_story_updated = re.search ('- Updated: ([0-9]+\-[0-9]+\-[0-9]+)',Story.collected_info).group(1)
        except:
            new_story_updated = ''
        try: 
            new_story_staringchars = re.search('- Published: [0-9]+\-[0-9]+\-[0-9]+ - (.*)',Story.collected_info).group(1)
            if new_story_staringchars == "Complete']":
                new_story_staringchars = ''
        except:
            print "Can this happen?"
            print Story.collected_info
            new_story_staringchars = ''
    
        new_story = story((new_story_rating,new_story_updated,new_story_favs,new_story_staringchars,new_story_chapters,new_story_complete,Story.collected_info,new_story_genre,Story.desc,new_story_language,Story.author,Story.url,new_story_follows,Story.title,new_story_reviews,new_story_published,new_story_words))

        changed_stories +=1
        new_stories.append(new_story)
    else:
        if Story.collected_info!= None or len(Story.collected_info)>2:
            new_stories.append(Story)
stories = new_stories
with open('Corrected-3-15-13.csv', 'wb') as newcsvfile:
#with open('additional.csv', 'rb') as csvfile:
    writer = csv.writer(newcsvfile, delimiter=",", quotechar='"')
    # write header
    writer.writerow(["rating","updated","favorites","staringchars","chapters","complete","collected_info","genre","desc","language","author","url","follows","title","reviews","published","words"])

    for story in stories:
        writer.writerow([story.rating, unix_date_to_american_date(story.updated),story.favorites,story.staringchars,story.chapters,story.complete,story.collected_info,story.genre,story.desc,story.language,story.author,story.url,story.follows,story.title,story.reviews,unix_date_to_american_date(story.published),story.words])


completed_sum=0
maybealive_sum = 0
abandoned_sum = 0
abandonedneverupdated_sum = 0
abandoned_length = []
for Story in stories:
    if Story.complete ==True:
        completed_sum +=1
    elif Story.abandoned ==1:
        abandoned_sum +=1
        abandoned_length.append(Story.words)
    elif Story.abandoned ==2:
        abandonedneverupdated_sum +=1
    elif Story.abandoned ==3:
        maybealive_sum +=1


print changed_stories, " stories changed because the initial way of structuring their data didn't work because these stories are missing data in a way I didn't predict."

# remove all stories from 2013 because it would be screwy to include an extra few monthes from one year 
pre_2013_stories = []
for story in stories:
    if story.published !=None and story.published !='' and story.published.year <2013:
        pre_2013_stories.append(story)
excluded_stories = len(stories)-len(pre_2013_stories)
print str(excluded_stories), " fanfictions from 2013 (or after) excluded from analysis."
stories = pre_2013_stories

print "Completed: ", 100*(float(completed_sum)/len(stories))
print "Percent Abandoned ", 100*(float(abandoned_sum)/(completed_sum+abandoned_sum+abandonedneverupdated_sum))
print "Average Length of Abandoned ", numpy.mean(abandoned_length)
print "Standard deviation of Abandoned length ", numpy.std(abandoned_length)

print "Pearsonr correlation between number of favorites and number of reviews: ", round(stats.pearsonr(reviews_list, favorites_list)[0],3)


oneshots_words = []
oneshots_reviews = []
oneshots_favorites = []

for story in stories:
    if story.oneshot == True:
        oneshots_list.append(story)
ignored_ff = 0        
for story in oneshots_list:
    # skip over fanfictions that don't specify words, reviews, or favorites, only 19 fanfictions are that way
    if story.words!='' and story.words!=None and story.reviews !='' and story.reviews !=None and story.favorites!='' and story.favorites !=None:
        oneshots_words.append(story.words)
        oneshots_reviews.append(story.reviews)
        oneshots_favorites.append(story.favorites)
    else: ignored_ff+=1

print "These statistics ignore" , str(ignored_ff), " fanfictions because they were missing either length,  # reviews, or # favorites data."
print "Pearsonr correlation between length and number of reviews for oneshots: ", round(stats.pearsonr(oneshots_words, oneshots_reviews)[0],3)
print "Pearsonr correlation between length and number of favorites for oneshots: ", round(stats.pearsonr(oneshots_words, oneshots_favorites)[0],3)

#Calculate the correlation between publishing year, month, and day and the number of fictions published and the amount of reviews, favorites, and follows they got.

publishing_dates_and_amounts = []
#publishing_dates_and_amounts.append(list((stories[0].published,0,0,0,0)))
staring_chars_and_amounts = []
#staring_chars_and_amounts.append(list((stories[0].staringchars.split(' & ')[0],0,0,0,0)))
staring_chars_groups_and_amounts = []
#staring_chars_groups_and_amounts.append(list((set(stories[0].staringchars.split(' & ')),0,0,0,0)))
checked_dates = []
checked_chars = []
checked_chars_groups = []



# creates a list of ((yyyy,mm,dd), amount published on that date, reviews,favorites,follows those stories got)
for story in stories:
    if story.published not in checked_dates:
        publishing_dates_and_amounts.append(list((story.published,1, story.reviews, story.favorites, story.follows)))
        checked_dates.append(story.published)
    else:
        index_counter = checked_dates.index(story.published)
        publishing_dates_and_amounts[index_counter][1]+=1
        publishing_dates_and_amounts[index_counter][2]+=story.reviews
        publishing_dates_and_amounts[index_counter][3]+=story.favorites
        publishing_dates_and_amounts[index_counter][4]+=story.follows

    fscs = set(story.staringchars.split(' & '))
    scs = list(map(str.strip,fscs))
    
    if scs not in checked_chars_groups:
        staring_chars_groups_and_amounts.append(list((scs,1, story.reviews, story.favorites, story.follows)))
        checked_chars_groups.append(scs)
    else:
        index_counter = checked_chars_groups.index(scs)
        staring_chars_groups_and_amounts[index_counter][1]+=1
        staring_chars_groups_and_amounts[index_counter][2]+=story.reviews
        staring_chars_groups_and_amounts[index_counter][3]+=story.favorites
        staring_chars_groups_and_amounts[index_counter][4]+=story.follows

    for sc in scs:
        if sc not in checked_chars:
            staring_chars_and_amounts.append(list((sc,1, story.reviews, story.favorites, story.follows)))
            checked_chars.append(sc)
        else:
            index_counter = checked_chars.index(sc)
            staring_chars_and_amounts[index_counter][1]+=1
            staring_chars_and_amounts[index_counter][2]+=story.reviews
            staring_chars_and_amounts[index_counter][3]+=story.favorites
            staring_chars_and_amounts[index_counter][4]+=story.follows

# remove data from when publishing dates weren't specified
for date in publishing_dates_and_amounts:
    if date[0] =='' or date[0] == None:
        print str(date[1])+" publishing dates not specified."
        publishing_dates_and_amounts.remove(date)
        break


#Determine if having certain characters be the starring characters is particularly popular with authors (judging by the number of fan fictions published) and with readers (judging by the number of reviews, follows, and favorites). Do this for both individual characters and for groups of characters. 

def make_by_time_unit(publishing_dates_and_amounts, date_unit=None):
    skip = False
    #timeunits_and_amounts.append(list((getattr(stories[0].published,date_unit),0,0,0,0)))
    
    index_counter = -1
    checked_dates = []
    timeunits_and_amounts = []

    for date in publishing_dates_and_amounts:
        if date_unit !=None:
            x_label = getattr(date[0],date_unit)
        else:
            x_label = date[0]
        if x_label not in checked_dates:
            timeunits_and_amounts.append(list((x_label,date[1],date[2],date[3],date[4])))
            checked_dates.append(x_label)
        else:
            index = checked_dates.index(x_label)
            timeunits_and_amounts[index][1]+=date[1]
            timeunits_and_amounts[index][2]+=date[2]
            timeunits_and_amounts[index][3]+=date[3]
            timeunits_and_amounts[index][4]+=date[4]
    
    return timeunits_and_amounts

def plot_data (timeunits_and_amounts,x_axis_label,string_x_labels=False,limit=None):
    size = 37,21
    enlarge = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel ("Number of fanfictions published")
    ax.set_xlabel (x_axis_label)
    if limit !=None:
        sortedlist = timeunits_and_amounts
        sortedlist = sorted(sortedlist,key=operator.itemgetter(1),reverse=True)[:limit]
    else:
        sortedlist = timeunits_and_amounts
    x = [timeunit[0] for timeunit in sortedlist]
    y =  [freq[1] for freq in sortedlist]
    if string_x_labels == False:
        rot = 0
        xticks= x
    else:
        x = [i for i in range(len(sortedlist))]
        rot = 90
        enlarge = True
        xticks = zip(*sortedlist)[0]
    if enlarge:
        fig.subplots_adjust(bottom=0.3)
    plt.xticks(x,xticks,rotation=rot)
    plt.bar(x,y,.5)
    plt.title("Number of Fanfictions Published vs  "+x_axis_label)
    plt.show()

    fig = plt.figure()
    if enlarge:
        fig.subplots_adjust(bottom=0.3)
    ax = fig.add_subplot(111)
    ax.set_ylabel ("Average number of reviews per fanfiction")
    ax.set_xlabel (x_axis_label)

    if limit !=None:
        sortedlist = timeunits_and_amounts
        sortedlist = sorted(sortedlist,key=lambda x_y_groupings: x_y_groupings[2]/float(x_y_groupings[1]),reverse=True)[:limit]
    else:
        sortedlist = timeunits_and_amounts
    y = []
    x = [timeunit[0] for timeunit in sortedlist]
    for reviews in sortedlist:
        try:
            y.append(float(reviews[2])/reviews[1] )
        except:
            y.append(0)
    if string_x_labels == False:
        xticks= x

    else:
        x = [i for i in range(len(sortedlist))]
        enlarge = True
        xticks = zip(*sortedlist)[0]
    plt.xticks(x,xticks,rotation=rot)
    plt.bar(x,y,.5)
    plt.title("Average Number of Reviews vs "+x_axis_label)
    plt.show()

    fig = plt.figure()
    if enlarge:
        fig.subplots_adjust(bottom=0.3)
    ax = fig.add_subplot(111)
    ax.set_ylabel ("Average number of favorites per fanfiction")
    ax.set_xlabel (x_axis_label)

    if limit !=None:
        sortedlist = timeunits_and_amounts
        sortedlist = sorted(sortedlist,reverse = True,key=lambda x_y_groupings: x_y_groupings[3]/float(x_y_groupings[1]))[:limit]
    else:
        sortedlist = timeunits_and_amounts
    x = [timeunit[0] for timeunit in sortedlist]
    y = []

    for favorites in sortedlist:
        try: 
            y.append(float(favorites[3])/favorites[1])
        except:
            y.append(0)
    if string_x_labels == False:
        xticks= x
    else:
        x = [i for i in range(len(sortedlist))]
        enlarge = True
        xticks = zip(*sortedlist)[0]

    plt.xticks(x,xticks,rotation=rot)
    plt.bar(x,y,.5)
    plt.title("Average Number of Favorites Gained vs "+x_axis_label)
    plt.show()
    fig = plt.figure()
    if enlarge:
        fig.subplots_adjust(bottom=0.3)
    ax = fig.add_subplot(111)
    ax.set_ylabel ("Average number of follows per fanfiction")
    ax.set_xlabel (x_axis_label)
    y = []
    if limit !=None:
        sortedlist = timeunits_and_amounts
        sortedlist = sorted(sortedlist,reverse = True,key=lambda x_y_groupings: x_y_groupings[4]/float(x_y_groupings[1]))[:limit]
    else:
        sortedlist = timeunits_and_amounts
    x = [timeunit[0] for timeunit in sortedlist]
    for follows in sortedlist:
        try:
            y.append(float(follows[4])/follows[1])
        except:
            y.append(0)
    if string_x_labels == False:
        xticks= x

    else:
        x = [i for i in range(len(sortedlist))]
        enlarge = True
        xticks = zip(*sortedlist)[0]
    
    plt.xticks(x,xticks,rotation=rot)
    plt.bar(x,y,.5)
    plt.title("Average Number of Follows Gained vs "+x_axis_label)
    plt.show()


plot_data(make_by_time_unit(publishing_dates_and_amounts,"year"),"Year Published")
plot_data(make_by_time_unit(publishing_dates_and_amounts,"month"),"Month Published")
plot_data(make_by_time_unit(publishing_dates_and_amounts,"day"),"Day Published")
mbtu = make_by_time_unit(staring_chars_and_amounts)
plot_data(mbtu,"Staring Character Included",list(zip(*mbtu)[0]),20)
new_mbtu = []
for story in mbtu:
    # Remove all sets of characters that occur less than 5 times
    if story[1]>100:
        new_mbtu.append(story)
try:
    plot_data(new_mbtu,"Staring Character Included Pruned",list(zip(*new_mbtu)[0]),20)
except:
    print "not enough stories to prune characters"
    pass

mbtu = make_by_time_unit(staring_chars_groups_and_amounts)
plot_data(mbtu,"Staring Characters",list(zip(*mbtu)[0]),20)
new_mbtu = []
for story in mbtu:
    # Remove all sets of characters that occur less than 5 times
    if story[1]>100:
        new_mbtu.append(story)

plot_data(new_mbtu,"Staring Characters Pruned",list(zip(*new_mbtu)[0]),20)




    
#    return time_freq_graph,time_reviews_graph,time_favorites_graph,time_follows_graph
    

    # don't forget to judge favorites/follows/reviews by publishing date
    # create total for each day
    # generate total for each month then for each year
