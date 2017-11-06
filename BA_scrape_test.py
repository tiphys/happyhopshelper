#Beer advocate scrape test

# For parsing the HTML we get from beeradvocate.com
from html.parser import HTMLParser

# HTTP requests for talking to beeradvocate
import requests

# The beeradvocate.com search query
url = 'http://beeradvocate.com/search/?q='
beer = 'Kentucky Brunch Brand Stout' #test beer name
request = url + beer

# Pull from the site the search reqults
r = requests.get(request)

# r.text now contains a stupid amount of html
# Find the dang search query in the return html in the most
# ghetto way possible
linkLoc = r.text.find('<ul><li><a href="/beer/profile')
endLoc = r.text.find('><b>', linkLoc)
openQuote = r.text.find('"', linkLoc) + 1
closeQuote = r.text.find('"', openQuote)
print(linkLoc, " ", endLoc, " ", openQuote, " ", closeQuote)
print(r.text[openQuote:closeQuote])

url = 'http://beeradvocate.com' + r.text[openQuote:closeQuote]
rbeer = requests.get(url)

# Class that defines a beer
class beerDefinition:
    def __init__(self,
                 name,
                 breweryName,
                 breweryState,
                 breweryCountry,
                 style,
                 abv,
                 description,
                 descriptionAuth,
                 baRanking,
                 baReviews,
                 baRatings,
                 psDev,
                 pDev):
        self.name = name
        self.breweryName = breweryName
        self.breweryState = breweryState
        self.breweryCountry =breweryCountry
        self.style = style
        self.abv = abv
        self.description = description
        self.descriptionAuth = descriptionAuth
        self.baRanking = baRanking
        self.baReviews = baReviews
        self.baRatings = baRatings
        self.psDev = psDev
        self.pDev = pDev

    def toString(self):
        print('Beer name = ', self.name)
        print('Brewery name = ', self.breweryName)
        print('Brewery state = ', self.breweryState)
        print('Bewery country = ', self.breweryCountry)
        print('Beer style = ', self.style)
        print('Beer ABV = ', self.abv)
        print('Beer description = ', self.description)
        print('Description author = ', self.descriptionAuth)
        print('BA ranking = ', self.baRanking)
        print('Number of BA reviews = ', self.baReviews)
        print('Number of BA ratings = ', self.baRatings)
        print('Beer psDev = ', self.psDev)
        print('Beer pDev = ', self.pDev)
        return ''

#print(r.text)
#with open('beerinfo.txt', 'w') as text_file:
#    text_file.write(rbeer.text)

#rbeer is our beer page
# Beer info starts at a string like this: <b>BEER INFO</b>
beerInfoLoc = rbeer.text.find('<b>BEER INFO</b>')
currentPointer = beerInfoLoc

# The brewery line is next looks like: <a href="/beer/profile/23222/"><b>Toppling Goliath Brewing Company</b></a>
breweryLocStart = rbeer.text.find('a href="/beer/profile/"', currentPointer)
breweryNameStart = rbeer.text.find('><b>', beerInfoLoc + 1) + 4
breweryNameStop = rbeer.text.find('</b>', breweryNameStart)
breweryName = rbeer.text[breweryNameStart:breweryNameStop].strip()
currentPointer = breweryNameStop

# Next should be the brewery location like: <br><a href="/place/directory/9/US/IA/">Iowa</a>, <a href="/place/directory/9/US/">United States</a><br><a href="http://tgbrews.com" target="_blank">tgbrews.com</a>		<br><br>
breweryLocState = rbeer.text.find('/place/directory/', currentPointer)
breweryLocStateStart = rbeer.text.find('">', breweryLocState) + 2
breweryLocStateStop = rbeer.text.find('</a>', breweryLocStateStart)
breweryState = rbeer.text[breweryLocStateStart:breweryLocStateStop].strip()
currentPointer = breweryLocStateStop

# Next is the country like: <a href="/place/directory/9/US/">United States</a><br>
breweryLocCountry = rbeer.text.find('<a href="/place/directory', currentPointer)
breweryLocCountryStart = rbeer.text.find('">', breweryLocCountry) + 2
breweryLocCountryStop = rbeer.text.find('</a>', breweryLocCountryStart)
breweryCountry = rbeer.text[breweryLocCountryStart:breweryLocCountryStop].strip()
currentPointer = breweryLocCountryStop

# Next is other garbage like URL that we probably don't care about

# Next is the style looks like: <b>Style:</b> <a href="/beer/style/157/"><b>American Double / Imperial Stout</b></a>
# note the '/' presumably they'll always split styles like this
beerStyleSection = rbeer.text.find('<a href="/beer/style', currentPointer)
beerStyleStart = rbeer.text.find('><b>', beerStyleSection) + 4
beerStyleStop = rbeer.text.find('</b>', beerStyleStart)
beerStyle = rbeer.text[beerStyleStart:beerStyleStop].strip()
currentPointer = beerStyleStop

# Next is the alcohol by volume like: <b>Alcohol by volume (ABV):</b> 12.00%
beerABVSection = rbeer.text.find('(ABV)', currentPointer);
beerABVStart = rbeer.text.find('</b>', beerABVSection) + 5
beerABVStop = rbeer.text.find('%', beerABVStart)
beerABV = rbeer.text[beerABVStart:beerABVStop].strip()
currentPointer = beerABVStop

# Now is the free-form notes / commercial description.  It's after a <br> tag after <b>Notes / Commercial Description:</b> and is ented with another <br> tag
beerDescSection = rbeer.text.find('Notes / Commercial Description', currentPointer)
beerDescStart = rbeer.text.find('<br>', beerDescSection) + 4
beerDescStop = rbeer.text.find('<br>', beerDescStart)
beerDesc = rbeer.text[beerDescStart:beerDescStop].strip()
currentPointer = beerDescStop

# Immediately following that is the author's username like: <br><br>Added by siradmiralnelson on 02-26-2012<br>
# (the first <br> is the <br> that ends the description section
beerAuthorStart = rbeer.text.find('Added by ', currentPointer) + 9
beerAuthorStop = rbeer.text.find(' on ', beerAuthorStart)
beerAuthorUsername = rbeer.text[beerAuthorStart:beerAuthorStop].strip()
currentPointer = beerAuthorStop;

# Now we move onto the beer stats section
# First one is ranking which is a two line entry like: <dt>Ranking:</dt>\n<dd>#1</dd>
beerStatsSection = rbeer.text.find('<b>BEER STATS</b>', currentPointer)
beerRankingStart = rbeer.text.find('<dd>#', beerStatsSection) + 5
beerRankingStop = rbeer.text.find('</dd>', beerRankingStart)
beerAdvocateRank = rbeer.text[beerRankingStart:beerRankingStop].strip()
currentPointer = beerRankingStop

# Next is the number of reviews looks like: <dd><span class="ba-reviews">126</span></dd>
beerNumReviewsStart = rbeer.text.find('-reviews">', currentPointer) + 10
beerNumReviewsStop = rbeer.text.find('</span>', beerNumReviewsStart)
beerNumReviews = rbeer.text[beerNumReviewsStart:beerNumReviewsStop].strip()
currentPointer = beerNumReviewsStop

# Next is the number of ratings looks like: <dd><span class="ba-ratings">647</span></dd>
beerNumRatingsStart = rbeer.text.find('-ratings">', currentPointer) + 10
beerNumRatingsStop = rbeer.text.find('</span>', beerNumRatingsStart)
beerNumRatings = rbeer.text[beerNumRatingsStart:beerNumRatingsStop].strip()
currentPointer = beerNumRatingsStop

# Next is the psDev like: <!--<br>psDev: 6.4%-->
beerpsDevStart = rbeer.text.find('psDev:', currentPointer) + 6
beerpsDevStop = rbeer.text.find('%', beerpsDevStart)
beerpsDev = rbeer.text[beerpsDevStart:beerpsDevStop].strip()
currentPointer = beerpsDevStop

# Next is the psDev value: <dd><span class="ba-pdev"> (on a new line) (why oh why is it on a new line?)
# (it's also indented like 7 times)
beerpDevStart = rbeer.text.find('-pdev">', currentPointer) + 7
beerpDevStop = rbeer.text.find('%', beerpDevStart)
beerpDev = rbeer.text[beerpDevStart:beerpDevStop].strip()
currentPointer = beerpDevStop

# Next are the comments which is just a shitton of text starting with <div id="rating_fullview"><div id="rating_fullview_container"
# and ending with <div style="font-size:1em; padding:4px; text-align:right; white-space:nowrap; overflow:hidden;">
# There are also multiple pages that will have to be somehow scraped

beerDef = beerDefinition(beer,
                         breweryName,
                         breweryState,
                         breweryCountry,
                         beerStyle,
                         beerABV,
                         beerDesc,
                         beerAuthorUsername,
                         beerAdvocateRank,
                         beerNumReviews,
                         beerNumRatings,
                         beerpsDev,
                         beerpDev)

print(beerDef.toString())
