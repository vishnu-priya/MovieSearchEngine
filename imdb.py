from BeautifulSoup import BeautifulSoup
import re, urllib2, pdb;

url = 'http://imdb.com'
movieList = open('Movies/TVSeries.txt', 'w')
def get_response(url, mveUrl):
    try:
        if url == 'None':
            url = '/'
        urlFull = 'http://www.imdb.com'+url
        respdata = urllib2.urlopen(urlFull).read()
        if respdata is not None:
            print urlFull
            soupdata = BeautifulSoup(respdata)
            print soupdata.html.head.title.string
            aData = soupdata.findAll('a', href=True)
            excludeList = ['TV - IMDb']
            if not any(str in soupdata.html.head.title.string for str in excludeList):
                if 'title' in urlFull:
                    parse_data(soupdata, soupdata.html.head.title.string, urlFull)
                    movieList.write(soupdata.html.head.title.string.encode('utf8'))
                for a in aData:
                    refString = a['href']
                    vetoList = ['videoplayer', 'showtimes', 'gallery', 'name', 'character', 'feature', 'video', 'help', 'privacy', 'privacy_change', 'registration', 'academymuseum', 'a2z', 'updates', 'trivia', 'mediaviewer', 'plotsummary', 'criticreviews', 'media', 'officialsites', 'fullcredits', 'releaseinfo', 'badge', 'list', 'buy-at-amazon', 'movieconnections', 'reviews', 'alternateversions', 'business', 'crazycredits', 'goofs', 'quotes', 'advertising', 'pressroom', 'companycredits', 'company', 'externalsites', 'soundtrack', 'soundtrack', 'keywords', 'maindetails', 'synopsis', 'taglines', 'literature', 'technical', 'locations', 'mpaa', 'news', 'swiki', 'parentalguide', 'tt_shop', 'awards', 'faq', 'boxoffice', 'ratings', 'recommendations', 'tvgrid', 'trailers']
                    if not any(str in refString for str in vetoList):
                        if refString.split('?')[0] not in mveUrl:
                            mveUrl.append(a['href'].split('?')[0])
                return mveUrl
    except urllib2.URLError as err:
        print err.reason , urlFull

def parse_data(respdata, fileName, movieUrl):
    h4Details = respdata.findAll('h4')
    movieDetails = {}
    movieDetails['url'] = movieUrl
    movieDetails['ratings'] = respdata.findAll('div', class_='titlePageSprite star-box-giga-star').string
    for h4 in h4Details:
        if h4.attrs != []:
            if h4['class'] == 'inline':
                if len(h4.parent) >= 2:
                    values = h4.parent.findAll('a')
                    if len(values) > 1:
                        movieDetails[h4.string] = []
                        for val in values:
                            if val.span:
                                movieDetails[h4.string].append(val.span.string)
                            else:
                                movieDetails[h4.string].append(val.string)
                    else:
                        if len(values) != 0:
                            if h4.string == 'Release Date:':
                                movieDetails[h4.string] = h4.parent.findAll(text=True)[2]
                            elif h4.string == 'Also Known As:':
                                movieDetails[h4.string] = h4.parent.findAll(text=True)[2]
                            elif values[0].span:
                                movieDetails[h4.string] = values[0].span.string
                            else:
                                movieDetails[h4.string] = values[0].string
    if respdata.findChildren('table', attrs={'class': 'cast_list'}):
        cast = respdata.findChildren('table', attrs={'class': 'cast_list'})[0].findChildren('tr')
        movieDetails['Cast'] = []
        if len(cast) > 0:
            for s in cast:
                castDetails = {}
                if s.attrs != []:
                    if s['class'] == 'odd' or s['class'] == 'even':
                        tds = s.findChildren('td')
                        for td in tds:
                            if td['class'] == 'primary_photo':
                                for a in td.a.img.attrs:
                                    if a[0] == 'src':
                                        castDetails[td['class']] = td.a.img['src']
                            elif td['class'] == 'itemprop':
                                castDetails['Actor'] = td.a.span.string
                            elif td['class'] == 'character':
                                if td.div.a:
                                    castDetails[td['class']] = td.div.a.string
                                else:
                                    castDetails[td['class']] = td.div.string
                    movieDetails['Cast'].append(castDetails)
    if respdata.find('div', attrs={'id':'titleStoryLine'}):
        story = respdata.find('div', attrs={'id':'titleStoryLine'})
        if story.div.p:
            movieDetails[story.h2] = story.div.p.find(text=True)
    if respdata.findAll('img', attrs={'itemprop': 'image'}):
        img = respdata.findAll('img', attrs={'itemprop': 'image'})
        if img[0]['src']:
            movieDetails['poster'] = img[0]['src']
    if respdata.find('a', attrs={'itemprop': 'trailer'}):
        video = respdata.find('a', attrs={'itemprop': 'trailer'})
        if video is not None:
            movieDetails['trailer'] = url + video['href']
    fileName = fileName.replace('/', '')
    f = open('Movies/'+fileName.encode('utf8')+'.txt', 'w')
    f.write(str(movieDetails))
    return

def fetch_response():
    mveUrl = []
    first = ' '
    mveUrl.append(first)
    for m in mveUrl:
        get_response(m, mveUrl)

fetch_response()
