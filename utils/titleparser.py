import re
from datetime import datetime
from dateutil.parser import parse
from utils.printing import Logger
log = Logger()

def search(title):

    trashTitle = (
        'RARBG', 'COM', '\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', '\d{2,4}K', '\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4',
        'KLEENEX', 'SD', 'H264', 'repack', '1500k', '500k', '1000k', 'rq', 'NEW', 'APT', '[TK]', 'TK', 'hd\d{3,4}p',
        '1500', '1000', 'SD', 'MP4-KT', 'MP4-KTR', 'SEXORS', 'MKV', 'DIVX', 'AVI', 'M4V', 'MP2', 'WEBM', 'MR4', '-GUSH',
        '[TK]', '.rq', '-rq', ' rq', ' Unknown -', 'Unknown', '\ss\s', '\bi\.'
    )

    title = re.sub(r'\W', ' ', title)
    for trash in trashTitle:
        title = re.sub(r'\b%s\b' % trash, '', title, flags=re.IGNORECASE)
    title = ' '.join(title.split())
    searchSiteID = 0
    fullsitename = ""
    searchTitle = ""
    searchDate = ""
    #log.info(f"Parsing: {title}")
    searchSettings = getSearchSettings(title)
    searchSiteID = searchSettings[0]
    fullsitename = searchSettings[1]
    searchTitle = searchSettings[2]
    searchDate = searchSettings[3]
    # Debug
    #print(f"Parsed. Site: {fullsitename}\n             {searchTitle}\n",end="")
    if searchDate:
        print(f"Release date parsed: {searchDate}")

    return searchSiteID, fullsitename, searchTitle, searchDate

def getSearchBaseURL(siteID):
    searchSites = siteValues()
    return searchSites[siteID][2]

def getSearchSearchURL(siteID):
    searchSites = siteValues()
    return searchSites[siteID][3]


def getSearchFilter(siteID):
    searchSites = siteValues()
    return searchSites[siteID][0]


def getSearchSiteName(siteID):
    searchSites = siteValues()
    return searchSites[siteID][1]

def siteValues():

    searchSites = [None] * 902 # one higher than the array below

    searchSites[0] = ("BlackedRaw", "BlackedRaw", "https://www.blackedraw.com", "https://www.blackedraw.com/api")
    searchSites[1] = ("Blacked", "Blacked", "https://www.blacked.com", "https://www.blacked.com/api")
    searchSites[2] = ("Brazzers", "Brazzers", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[5] = ("My Friends Hot Mom", "My Friends Hot Mom", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[6] = ("My First Sex Teacher", "My First Sex Teacher", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[7] = ("Seduced By A Cougar", "Seduced By A Cougar", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[8] = ("My Daughters Hot Friend", "My Daughters Hot Friend", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[9] = ("My Wife is My Pornstar", "My Wife is My Pornstar", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[10] = ("Tonights Girlfriend Classic", "Tonights Girlfriend Classic", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[11] = ("Wives on Vacation", "Wives on Vacation", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[12] = ("My Sisters Hot Friend", "My Sisters Hot Friend", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[13] = ("Naughty Weddings", "Naughty Weddings", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[14] = ("Dirty Wives Club", "Dirty Wives Club", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[15] = ("My Dads Hot Girlfriend", "My Dads Hot Girlfriend", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[16] = ("My Girl Loves Anal", "My Girl Loves Anal", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[17] = ("Lesbian Girl on Girl", "Lesbian Girl on Girl", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[18] = ("Naughty Office", "Naughty Office", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[19] = ("I have a Wife", "I have a Wife", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[20] = ("Naughty Bookworms", "Naughty Bookworms", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[21] = ("Housewife 1 on 1", "Housewife 1 on 1", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[22] = ("My Wifes Hot Friend", "My Wifes Hot Friend", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[23] = ("Latin Adultery", "Latin Adultery", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[24] = ("Ass Masterpiece", "Ass Masterpiece", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[25] = ("2 Chicks Same Time", "2 Chicks Same Time", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[26] = ("My Friends Hot Girl", "My Friends Hot Girl", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[27] = ("Neighbor Affair", "Neighbor Affair", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[28] = ("My Girlfriends Busty Friend", "My Girlfriends Busty Friend", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[29] = ("Naughty Athletics", "Naughty Athletics", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[30] = ("My Naughty Massage", "My Naughty Massage", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[31] = ("Fast Times", "Fast Times", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[32] = ("The Passenger", "The Passenger", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[33] = ("Milf Sugar Babes Classic", "Milf Sugar Babes Classic", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[34] = ("Perfect Fucking Strangers Classic", "Perfect Fucking Strangers Classic", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[35] = ("Asian 1 on 1", "Asian 1 on 1", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[36] = ("American Daydreams", "American Daydreams", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[37] = ("SoCal Coeds", "SoCal Coeds", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[38] = ("Naughty Country Girls", "Naughty Country Girls", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[39] = ("Diary of a Milf", "Diary of a Milf", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[40] = ("Naughty Rich Girls", "Naughty Rich Girls", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[41] = ("My Naughty Latin Maid", "My Naughty Latin Maid", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[42] = ("Naughty America", "Naughty America", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[43] = ("Diary of a Nanny", "Diary of a Nanny", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[44] = ("Naughty Flipside", "Naughty Flipside", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[45] = ("Live Party Girl", "Live Party Girl", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[46] = ("Live Naughty Student", "Live Naughty Student", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[47] = ("Live Naughty Secretary", "Live Naughty Secretary", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[48] = ("Live Gym Cam", "Live Gym Cam", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[49] = ("Live Naughty Teacher", "Live Naughty Teacher", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[50] = ("Live Naughty Milf", "Live Naughty Milf", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[51] = ("Live Naughty Nurse", "Live Naughty Nurse", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[52] = ("Vixen", "Vixen", "http://www.vixen.com", "http://www.vixen.com/api")
    searchSites[53] = ("Girlsway", "Girlsway", "https://www.girlsway.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[54] = ("Moms in Control", "Moms in Control", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[55] = ("Pornstars Like It Big", "Pornstars Like It Big", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[56] = ("Big Tits at Work", "Big Tits at Work", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[57] = ("Big Tits at School", "Big Tits at School", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[58] = ("Baby Got Boobs", "Baby Got Boobs", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[59] = ("Real Wife Stories", "Real Wife Stories", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[60] = ("Teens Like It Big", "Teens Like It Big", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[61] = ("ZZ Series", "ZZ Series", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[62] = ("Mommy Got Boobs", "Mommy Got Boobs", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[63] = ("Milfs Like It Big", "Milfs Like It Big", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[64] = ("Big Tits in Uniform", "Big Tits in Uniform", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[65] = ("Doctor Adventures", "Doctor Adventures", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[66] = ("BrazzersExxtra", "Exxtra", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[67] = ("Big Tits in Sports", "Big Tits in Sports", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[68] = ("Big Butts like it big", "Big Butts like it big", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[69] = ("Big Wet Butts", "Big Wet Butts", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[70] = ("Dirty Masseur", "Dirty Masseur", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[71] = ("Hot and Mean", "Hot and Mean", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[72] = ("Shes Gonna Squirt", "Shes Gonna Squirt", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[73] = ("Asses In Public", "Asses In Public", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[74] = ("Busty Z", "Busty Z", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[75] = ("Busty and Real", "Busty and Real", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[76] = ("Hot Chicks Big Asses", "Hot Chicks Big Asses", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[77] = ("CFNM Clothed Female Male Nude", "CFNM Clothed Female Male Nude", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[78] = ("Teens Like It Black", "Teens Like It Black", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[79] = ("Racks and Blacks", "Racks and Blacks", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[80] = ("Butts and Blacks", "Butts and Blacks", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[82] = ("X Art", "X-Art", "http://www.x-art.com", "http://www.x-art.com/search/")
    searchSites[83] = ("Bang Bros", "Bang Bros", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[84] = ("Ass Parade", "Ass Parade", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[85] = ("AvaSpice", "AvaSpice", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[86] = ("Back Room Facials", "Back Room Facials", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[87] = ("Backroom MILF", "Backroom MILF", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[88] = ("Ball Honeys", "Ball Honeys", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[89] = ("Bang Bus", "Bang Bus", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[90] = ("Bang Casting", "Bang Casting", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[91] = ("Bang POV", "Bang POV", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[92] = ("Bang Tryouts", "Bang Tryouts", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[93] = ("BangBros 18", "BangBros 18", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[94] = ("BangBros Angels", "BangBros Angels", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[95] = ("Bangbros Clips", "Bangbros Clips", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[96] = ("BangBros Remastered", "BangBros Remastered", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[97] = ("Big Mouthfuls", "Big Mouthfuls", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[98] = ("Big Tit Cream Pie", "Big Tit Cream Pie", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[99] = ("Big Tits Round Asses", "Big Tits Round Asses", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[100] = ("BlowJob Fridays", "BlowJob Fridays", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[101] = ("Blowjob Ninjas", "Blowjob Ninjas", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[102] = ("Boob Squad", "Boob Squad", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[103] = ("Brown Bunnies", "Brown Bunnies", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[104] = ("Can He Score", "Can He Score", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[105] = ("Bang Casting", "Bang Casting", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[106] = ("Chongas", "Chongas", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[107] = ("Colombia Fuck Fest", "Colombia Fuck Fest", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[108] = ("Dirty World Tour", "Dirty World Tour", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[109] = ("Dorm Invasion", "Dorm Invasion", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[110] = ("Facial Fest", "Facial Fest", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[111] = ("Fuck Team Five", "Fuck Team Five", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[112] = ("Glory Hole Loads", "Glory Hole Loads", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[113] = ("Latina Rampage", "Latina Rampage", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[114] = ("Living With Anna", "Living With Anna", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[115] = ("Magical Feet", "Magical Feet", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[116] = ("MILF Lessons", "MILF Lessons", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[117] = ("Milf Soup", "Milf Soup", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[118] = ("MomIsHorny", "MomIsHorny", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[119] = ("Monsters of Cock", "Monsters of Cock", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[120] = ("Mr CamelToe", "Mr CamelToe", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[121] = ("Mr Anal", "Mr Anal", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[122] = ("My Dirty Maid", "My Dirty Maid", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[123] = ("My Life In Brazil", "My Life In Brazil", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[124] = ("Newbie Black", "Newbie Black", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[125] = ("Party of 3", "Party of 3", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[126] = ("Pawg", "Pawg", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[127] = ("Penny Show", "Penny Show", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[128] = ("Porn Star Spa", "Porn Star Spa", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[129] = ("Power Munch", "Power Munch", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[130] = ("Public Bang", "Public Bang", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[131] = ("Slutty White Girls", "Slutty White Girls", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[132] = ("Stepmom Videos", "Stepmom Videos", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[133] = ("Street Ranger", "Street Ranger", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[134] = ("Tugjobs", "Tugjobs", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[135] = ("Working Latinas", "Working Latinas", "https://bangbros.com", "https://bangbros.com/search/")
    searchSites[136] = ("Tushy", "Tushy", "https://www.tushy.com", "https://www.tushy.com/api")
    searchSites[137] = ("Reality Kings", "Reality Kings", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[138] = ("40 Inch Plus", "40 Inch Plus", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[139] = ("8th Street Latinas", "8th Street Latinas", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[140] = ("Bad Tow Truck", "Bad Tow Truck", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[141] = ("Big Naturals", "Big Naturals", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[142] = ("Big Tits Boss", "Big Tits Boss", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[143] = ("Bikini Crashers", "Bikini Crashers", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[144] = ("Captain Stabbin", "Captain Stabbin", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[145] = ("CFNM Secret", "CFNM Secret", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[146] = ("Cum Fiesta", "Cum Fiesta", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[147] = ("Cum Girls", "Cum Girls", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[148] = ("Dangerous Dongs", "Dangerous Dongs", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[149] = ("Euro Sex Parties", "Euro Sex Parties", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[150] = ("Extreme Asses", "Extreme Asses", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[151] = ("Extreme Naturals", "Extreme Naturals", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[152] = ("First Time Auditions", "First Time Auditions", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[153] = ("Flower Tucci", "Flower Tucci", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[154] = ("Girls of Naked", "Girls of Naked", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[155] = ("Happy Tugs", "Happy Tugs", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[156] = ("HD Love", "HD Love", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[157] = ("Hot Bush", "Hot Bush", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[158] = ("In the VIP", "In the VIP", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[159] = ("Mike in Brazil", "Mike in Brazil", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[160] = ("Mikes Apartment", "Mike's Apartment", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[161] = ("Milf Hunter", "Milf Hunter", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[162] = ("Milf Next Door", "Milf Next Door", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[163] = ("Moms Bang Teens", "Moms Bang Teens", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[164] = ("Moms Lick Teens", "Moms Lick Teens", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[165] = ("Money Talks", "Money Talks", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[166] = ("Monster Curves", "Monster Curves", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[167] = ("No Faces", "No Faces", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[168] = ("Pure 18", "Pure 18", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[169] = ("Real Orgasms", "Real Orgasms", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[170] = ("RK Prime", "RK Prime", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[171] = ("Round and Brown", "Round and Brown", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[172] = ("Saturday Night Latinas", "Saturday Night Latinas", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[173] = ("See My Wife", "See My Wife", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[174] = ("Sneaky Sex", "Sneaky Sex", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[175] = ("Street BlowJobs", "Street BlowJobs", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[176] = ("Team Squirt", "Team Squirt", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[177] = ("Teens Love Huge Cocks", "Teens Love Huge Cocks", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[178] = ("Top Shelf Pussy", "Top Shelf Pussy", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[179] = ("Tranny Surprise", "Tranny Surprise", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[180] = ("VIP Crew", "VIP Crew", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[181] = ("We Live Together", "We Live Together", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[182] = ("Wives in Pantyhose", "Wives in Pantyhose", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[183] = ("21Naturals", "21Naturals", "https://www.21naturals.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[184] = ("PornFidelity", "PornFidelity", "https://www.pornfidelity.com", "https://www.pornfidelity.com/episodes/search/?site=2&page=1&search=")
    searchSites[185] = ("TeenFidelity", "TeenFidelity", "https://www.pornfidelity.com", "https://www.pornfidelity.com/episodes/search/?site=3&page=1&search=")
    searchSites[186] = ("Kelly Madison", "Kelly Madison", "https://www.pornfidelity.com", "https://www.pornfidelity.com/episodes/search/?site=1&page=1&search=")
    searchSites[187] = ("TeamSkeet", "TeamSkeet", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[188] = ("Exxxtra Small", "Exxxtra Small", "https://www.exxxtrasmall.com", "https://store.psmcdn.net/EXS-organic-ooJ4duo8")
    searchSites[189] = ("Teen Pies", "Teen Pies", "https://www.teenpies.com", "https://store.psmcdn.net/organic-tp-ka0WooXi")
    searchSites[190] = ("Innocent High", "Innocent High", "https://www.innocenthigh.com", "https://store.psmcdn.net/organic-ih-pouT0rah")
    searchSites[191] = ("Teen Curves", "Teen Curves", "https://www.teencurves.com/", "https://store.psmcdn.net/tc-organic-4dwlgywovp")
    searchSites[192] = ("CFNM Teens", "CFNM Teens", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[193] = ("Teens Love Anal", "Teens Love Anal", "https://www.teensloveanal.com", "https://store.psmcdn.net/organic-tla-lee9eZee")
    searchSites[194] = ("My Babysitters Club", "My Babysitters Club", "https://www.mybabysittersclub.com", "https://store.psmcdn.net/organic-bsc-Ac5eich1")
    searchSites[195] = ("She's New", "She's New", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[196] = ("Teens Do Porn", "Teens Do Porn", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[197] = ("POV Life", "POV Life", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[198] = ("The Real Workout", "The Real Workout", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[199] = ("This Girl Sucks", "This Girl Sucks", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[200] = ("Teens Love Money", "Teens Love Money", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[201] = ("Oye Loca", "Oye Loca", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[202] = ("Titty Attack", "Titty Attack", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[203] = ("Teeny Black", "Teeny Black", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[204] = ("Lust HD", "Lust HD", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[205] = ("Rub A Teen", "Rub A Teen", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[206] = ("Her Freshman Year", "Her Freshman Year", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[207] = ("Self Desire", "Self Desire", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[208] = ("Solo Interviews", "Solo Interviews", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[209] = ("Team Skeet Extras", "Team Skeet Extras", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[210] = ("Dyked", "Dyked", "https://www.dyked.com", "https://store.psmcdn.net/DYK-organic-kiedei7O")
    searchSites[211] = ("Badmilfs", "Badmilfs", "https://www.badmilfs.com", "https://store.psmcdn.net/Organic-bad-aiGhaiL5")
    searchSites[212] = ("Gingerpatch", "Gingerpatch", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[213] = ("BraceFaced", "BraceFaced", "https://www.teamskeet.com", "https://store.psmcdn.net/ts-organic-UNieTh9i")
    searchSites[214] = ("TeenJoi", "TeenJoi", "https://www.teenjoi.com", "https://store.psmcdn.net/JOI-organic-q8uvjxl29p")
    searchSites[215] = ("StepSiblings", "StepSiblings", "https://www.stepsiblings.com", "https://store.psmcdn.net/organic-sss-no7OhCoo")
    searchSites[216] = ("Lets Doe It", "Let's Doe It", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[217] = ("The White Boxxx", "The White Boxxx", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[218] = ("Scam Angels", "Scam Angels", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[219] = ("Chicas Loca", "Chicas Loca", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[220] = ("Her Limit", "Her Limit", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[221] = ("A Girl Knows", "A Girl Knows", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[222] = ("Porno Academie", "Porno Academie", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[223] = ("Xchimera", "Xchimera", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[224] = ("Carne Del Mercado", "Carne Del Mercado", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[225] = ("XXX Shades", "XXX Shades", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[226] = ("Bums Bus", "Bums Bus", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[227] = ("Bitches Abroad", "Bitches Abroad", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[228] = ("La Cochonne", "La Cochonne", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[229] = ("Crowd Bondage", "Crowd Bondage", "https://forbondage.com", "https://forbondage.com/search.en.html?q=")
    searchSites[230] = ("Relaxxxed", "Relaxxxed", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[231] = ("My Naughty Album", "My Naughty Album", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[232] = ("Tu Venganza", "Tu Venganza", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[233] = ("Bums Buero", "Bums Buero", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[234] = ("Los Consoladores", "Los Consoladores", "https://vipsexvault.com", "https://vipsexvault.com/search.en.html?q=")
    searchSites[235] = ("Quest for Orgasm", "Quest for Orgasm", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[236] = ("Trans Bella", "Trans Bella", "https://transbella.com", "https://transbella.com/search.en.html?q=")
    searchSites[237] = ("Her Big Ass", "Her Big Ass", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[238] = ("Horny Hostel", "Horny Hostel", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[239] = ("Fucked In Traffic", "Fucked In Traffic", "https://vipsexvault.com", "https://vipsexvault.com/search.en.html?q=")
    searchSites[240] = ("Las Folladoras", "Las Folladoras", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[241] = ("Badtime Stories", "Badtime Stories", "https://forbondage.com", "https://forbondage.com/search.en.html?q")
    searchSites[242] = ("Exposed Casting", "Exposed Casting", "https://vipsexvault.com", "https://vipsexvault.com/search.en.html?q=")
    searchSites[243] = ("Kinky Inlaws", "Kinky Inlaws", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[244] = ("Doe Projects", "Doe Projects", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[245] = ("Porndoepedia", "Porndoepedia", "https://vipsexvault.com", "https://vipsexvault.com/search.en.html?q=")
    searchSites[246] = ("Casting Francais", "Casting Francais", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[247] = ("Bums Besuch", "Bums Besuch", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[248] = ("Special Feet Force", "Special Feet Force", "https://forbondage.com", "https://forbondage.com/search.en.html?q")
    searchSites[249] = ("Trans Taboo", "Trans Taboo", "https://transbella.com", "https://transbella.com/search.en.html?q=")
    searchSites[250] = ("Operacion Limpieza", "Operacion Limpieza", "https://letsdoeit.com", "https://letsdoeit.com/search.en.html?q=")
    searchSites[251] = ("La Novice", "La Novice", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[252] = ("Casting Alla Italiana", "Casting Alla Italiana", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[253] = ("PinUp Sex", "PinUp Sex", "https://vipsexvault.com", "https://vipsexvault.com/search.en.html?q=")
    searchSites[254] = ("Hausfrau Ficken", "Hausfrau Ficken", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[255] = ("Deutschland Report", "Deutschland Report", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[256] = ("Reife Swinger", "Reife Swinger", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[257] = ("Scambisti Maturi", "Scambisti Maturi", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[258] = ("Sextape Germany", "Sextape Germany", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[259] = ("XXX Omas", "XXX Omas", "https://amateureuro.com", "https://amateureuro.com/search.en.html?q=")
    searchSites[260] = ("LegalPorno", "LegalPorno", "https://www.legalporno.com", "https://www.legalporno.com/search/?query=")
    searchSites[261] = ("Mofos", "Mofos", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[262] = ("ShareMyBF", "ShareMyBF", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[263] = ("Don't Break Me", "Don't Break Me", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[264] = ("I Know That Girl", "I Know That Girl", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[265] = ("Let's Try Anal", "Let's Try Anal", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[266] = ("Pervs On Patrol", "Pervs On Patrol", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[267] = ("Stranded Teens", "Stranded Teens", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[268] = ("Mofos B Sides", "Mofos B Sides", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[269] = ("Shes a Freak", "She's a Freak", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[270] = ("Public Pickups", "Public Pickups", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[271] = ("Babes", "Babes", "https://www.babes.com", "https://site-api.project1service.com")
    searchSites[272] = ("Babes Unleashed", "Babes Unleashed", "https://www.babes.com", "https://site-api.project1service.com")
    searchSites[273] = ("Black is Better", "Black is Better", "https://www.babes.com", "https://site-api.project1service.com")
    searchSites[274] = ("Elegant Anal", "Elegant Anal", "https://www.babes.com", "https://site-api.project1service.com")
    searchSites[275] = ("Office Obsession", "Office Obsession", "https://www.babes.com", "https://site-api.project1service.com")
    searchSites[276] = ("Stepmom Lessons", "Stepmom Lessons", "https://www.babes.com", "https://site-api.project1service.com")
    searchSites[277] = ("Evil Angel", "Evil Angel", "https://www.evilangel.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[278] = ("HardX", "HardX", "https://www.xempire.com", "https://www.xempire.com/en/search/hardx/")
    searchSites[279] = ("GloryHoleSecrets", "GloryHoleSecrets", "http://www.gloryholesecrets.com", "http://www.gloryholesecrets.com/tour/search.php?query=")
    searchSites[280] = ("New Sensations", "New Sensations", "http://www.newsensations.com", "https://www.newsensations.com/tour_ns/")
    searchSites[281] = ("Pure Taboo", "Pure Taboo", "https://www.puretaboo.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[282] = ("Swallowed", "Swallowed", "https://tour.swallowed.com", "https://tour.swallowed.com/view/")
    searchSites[283] = ("TrueAnal", "TrueAnal", "https://tour.trueanal.com", "https://tour.trueanal.com/view/")
    searchSites[284] = ("Nympho", "Nympho", "https://tour.nympho.com", "https://tour.nympho.com/view/")
    searchSites[285] = ("EroticaX", "EroticaX", "https://www.xempire.com", "https://www.xempire.com/en/search/eroticax/")
    searchSites[286] = ("DarkX", "DarkX", "https://www.xempire.com", "https://www.xempire.com/en/search/darkx/")
    searchSites[287] = ("LesbianX", "LesbianX", "http://www.xempire.com", "http://www.xempire.com/en/search/lesbianx/")
    searchSites[288] = ("Twistys", "Twistys", "https://www.twistys.com", "https://site-api.project1service.com")
    searchSites[289] = ("WhenGirlsPlay", "WhenGirlsPlay", "https://www.twistys.com", "https://site-api.project1service.com")
    searchSites[290] = ("MomKnowsBest", "MomKnowsBest", "https://www.twistys.com", "https://site-api.project1service.com")
    searchSites[291] = ("TwistysHard", "TwistysHard", "https://www.twistys.com", "https://site-api.project1service.com")
    searchSites[292] = ("VirtualTaboo", "VirtualTaboo", "https://virtualtaboo.com", "https://virtualtaboo.com/search?q=")
    searchSites[293] = ("Spizoo", "Spizoo", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[294] = ("Private", "Private", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[295] = ("Anal Introductions", "Anal Introductions", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[296] = ("Blacks on Sluts", "Blacks on Sluts", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[297] = ("I confess Files", "I confess Files", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[298] = ("Private Fetish", "Private Fetish", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[299] = ("Mission Ass Possible", "Mission Ass Possible", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[300] = ("Private MILFs", "Private MILFs", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[301] = ("Russian Fake Agent", "Russian Fake Agent", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[302] = ("Russian Teen Ass", "Russian Teen Ass", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[303] = ("Sex on the beach", "Sex on the beach", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[304] = ("Private Stars", "Private Stars", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[305] = ("Tight and Teen", "Tight and Teen", "https://www.private.com", "https://www.private.com/search.php?query=")
    searchSites[306] = ("PassionHD", "PassionHD", "https://www.passion-hd.com", "https://passion-hd.com/video/")
    searchSites[307] = ("FantasyHD", "FantasyHD", "https://www.fantasyhd.com", "https://fantasyhd.com/video/")
    searchSites[308] = ("PornPros", "PornPros", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[309] = ("18YearsOld", "18YearsOld", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[310] = ("RealExGirlfriends", "RealExGirlfriends", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[311] = ("MassageCreep", "MassageCreep", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[312] = ("DeepThroatLove", "DeepThroatLove", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[313] = ("TeenBFF", "TeenBFF", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[314] = ("ShadyPi", "ShadyPi", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[315] = ("CrueltyParty", "CrueltyParty", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[316] = ("Disgraced18", "Disgraced18", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[317] = ("MilfHumiliation", "MilfHumiliation", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[318] = ("CumshotSurprise", "CumshotSurprise", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[319] = ("40ozBounce", "40ozBounce", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[320] = ("JurassicCock", "JurassicCock", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[321] = ("FreaksOfCock", "FreaksOfCock", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[322] = ("EuroHumpers", "EuroHumpers", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[323] = ("FreaksOfBoobs", "FreaksOfBoobs", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[324] = ("CumDisgrace", "CumDisgrace", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[325] = ("CockCompetition", "CockCompetition", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[326] = ("PimpParade", "PimpParade", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[327] = ("SquirtDisgrace", "SquirtDisgrace", "https://www.pornpros.com", "https://pornpros.com/video/")
    searchSites[328] = ("DigitalPlayground", "DigitalPlayground", "https://www.digitalplayground.com", "https://site-api.project1service.com")
    searchSites[329] = ("Throated", "Throated", "https://www.blowpass.com", "https://www.blowpass.com/en/search/throated/scene/")
    searchSites[330] = ("Nuru Massage", "Nuru Massage", "https://www.fantasymassage.com", "https://www.fantasymassage.com/en/search/")
    searchSites[331] = ("Nuru Massage", "Nuru Massage", "https://www.fantasymassage.com", "https://www.fantasymassage.com/en/search/")
    searchSites[332] = ("DDF Babes", "DDF Babes", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[333] = ("SexyHub", "SexyHub", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[334] = ("Dane Jones", "Dane Jones", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[335] = ("Fitness Rooms", "Fitness Rooms", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[336] = ("Girlfriends.xxx", "Girlfriends.xxx", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[337] = ("Lesbea", "Lesbea", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[338] = ("Massage Rooms", "Massage Rooms", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[339] = ("MomXXX", "MomXXX", "https://www.sexyhub.com", "https://site-api.project1service.com")
    searchSites[340] = ("FakeHub", "FakeHub", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[341] = ("Big Cock Bully", "Big Cock Bully", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[342] = ("VirtualRealPorn", "VirtualRealPorn", "https://virtualrealporn.com/", "https://virtualrealporn.com/vr-porn-video/")
    searchSites[343] = ("Analized", "Analized", "https://analized.com", "https://analized.com/search.php?query=")
    searchSites[344] = ("James Deen", "James Deen", "https://jamesdeen.com", "https://jamesdeen.com/search.php?query=")
    searchSites[345] = ("Twisted Visual", "Twisted Visual", "https://twistedvisual.com", "https://twistedvisual.com/search.php?query=")
    searchSites[346] = ("Only Prince", "Only Prince", "https://onlyprince.com", "https://onlyprince.com/search.php?query=")
    searchSites[347] = ("Bad Daddy POV", "Bad Daddy POV", "https://baddaddypov.com", "https://baddaddypov.com/search.php?query=")
    searchSites[348] = ("POV Perverts", "POV Perverts", "https://povperverts.net", "https://povperverts.net/search.php?query=")
    searchSites[349] = ("Pervert Gallery", "Pervert Gallery", "https://pervertgallery.com", "https://pervertgallery.com/search.php?query=")
    searchSites[350] = ("DTF Sluts", "DTF Sluts", "https://dtfsluts.com", "https://dtfsluts.com/search.php?query=")
    searchSites[351] = ("Mommy Blows Best", "Mommy Blows Best", "http://www.blowpass.com", "http://www.blowpass.com/en/search/mommyblowsbest/scene/")
    searchSites[352] = ("Only Teen Blowjobs", "Only Teen Blowjobs", "http://www.blowpass.com", "http://www.blowpass.com/en/search/onlyteenblowjobs/scene/")
    searchSites[353] = ("1000 Facials", "1000 Facials", "http://www.blowpass.com", "http://www.blowpass.com/en/search/1000facials/scene/")
    searchSites[354] = ("Immoral Live", "Immoral Live", "http://www.blowpass.com", "http://www.blowpass.com/en/search/immorallive/scene/")
    searchSites[355] = ("Fantasy Massage", "Fantasy Massage", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[356] = ("All Girl Massage", "All Girl Massage", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[357] = ("Soapy Massage", "Soapy Massage", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[358] = ("Milking Table", "Milking Table", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[359] = ("Massage Parlor", "Massage Parlor", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[360] = ("Tricky Spa", "Tricky Spa", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[361] = ("Sweetheart Video", "Sweetheart Video", "https://www.milehighmedia.com", "https://site-api.project1service.com")
    searchSites[362] = ("Reality Junkies", "Reality Junkies", "http://www.milehighmedia.com", "https://site-api.project1service.com")
    searchSites[363] = ("SweetSinner", "SweetSinner", "https://www.milehighmedia.com", "https://site-api.project1service.com")
    searchSites[364] = ("Doghouse Digital", "Doghouse Digital", "http://www.milehighmedia.com", "https://site-api.project1service.com")
    searchSites[365] = ("21Sextury", "21Sextury", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[366] = ("Anal Teen Angels", "Anal Teen Angels", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[367] = ("Deepthroat Frenzy", "Deepthroat Frenzy", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[368] = ("DP Fanatics", "DP Fanatics", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[369] = ("Footsie Babes", "Footsie Babes", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[370] = ("Gapeland", "Gapeland", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[371] = ("Lez Cuties", "Lez Cuties", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[372] = ("Pix and Video", "Pix and Video", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[373] = ("21FootArt", "21FootArt", "http://www.21naturals.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[374] = ("21EroticAnal", "21EroticAnal", "http://www.21naturals.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[375] = ("Mommys Girl", "Mommy's Girl", "http://www.girlsway.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[376] = ("Web Young", "Web Young", "http://www.girlsway.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[377] = ("Girls Try Anal", "Girls Try Anal", "http://www.girlsway.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[378] = ("Sextape Lesbians", "Sextape Lesbians", "http://www.girlsway.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[379] = ("Girlsway Originals", "Girlsway Originals", "http://www.girlsway.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[380] = ("Girlfriends Films", "Girlfriends Films", "http://www.girlfriendsfilms.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/query")
    searchSites[381] = ("Burning Angel", "Burning Angel", "http://www.burningangel.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[382] = ("Pretty Dirty", "Pretty Dirty", "http://www.prettydirty.com", "http://www.prettydirty.com/en/search/")
    searchSites[383] = ("Devils Film", "Devil's Film", "http://www.devilsfilm.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[384] = ("Peter North", "Peter North", "http://www.peternorth.com", "http://www.peternorth.com/en/search/")
    searchSites[385] = ("Rocco Siffredi", "Rocco Siffredi", "http://www.roccosiffredi.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[386] = ("Tera Patrick", "Tera Patrick", "http://www.terapatrick.com", "http://www.terapatrick.com/en/search/")
    searchSites[387] = ("Sunny Leone", "Sunny Leone", "http://www.sunnyleone.com", "http://www.sunnyleone.com/en/search/scene/")
    searchSites[388] = ("Lane Sisters", "Lane Sisters", "http://www.lanesisters.com", "http://www.lanesisters.com/en/search/scene/")
    searchSites[389] = ("Dylan Ryder", "Dylan Ryder", "http://www.dylanryder.com", "http://www.dylanryder.com/en/search/scene/")
    searchSites[390] = ("Abbey Brooks", "Abbey Brooks", "http://www.abbeybrooks.com", "http://www.abbeybrooks.com/en/search/scene/")
    searchSites[391] = ("Devon Lee", "Devon Lee", "http://www.devonlee.com", "http://www.devonlee.com/en/search/scene/")
    searchSites[392] = ("Hanna Hilton", "Hanna Hilton", "http://www.hannahilton.com", "http://www.hannahilton.com/en/search/scene/")
    searchSites[393] = ("LA Sluts", "LA Sluts", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[394] = ("Slut Stepsister", "Slut Stepsister", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[395] = ("Teens Love Cream", "Teens Love Cream", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[396] = ("Latina Stepmom", "Latina Stepmom", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[397] = ("Fake Taxi", "Fake Taxi", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[398] = ("Fakehub Originals", "Fakehub Originals", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[399] = ("Public Agent", "Public Agent", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[400] = ("Fake Agent", "Fake Agent", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[401] = ("Female Agent", "Female Agent", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[402] = ("Fake Hospital", "Fake Hospital", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[403] = ("Fake Agent UK", "Fake Agent UK", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[404] = ("Fake Cop", "Fake Cop", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[405] = ("Female Fake Taxi", "Female Fake Taxi", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[406] = ("Fake Driving School", "Fake Driving School", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[407] = ("Fake Hostel", "Fake Hostel", "https://www.fakehub.com", "https://site-api.project1service.com")
    searchSites[408] = ("Dogfart", "Dogfart", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[409] = ("BlacksOnBlondes", "BlacksOnBlondes", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[410] = ("CuckoldSessions", "CuckoldSessions", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[411] = ("GloryHole", "GloryHole", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[412] = ("BlacksOnCougars", "BlacksOnCougars", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[413] = ("WeFuckBlackGirls", "WeFuckBlackGirls", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[414] = ("WatchingMyMomGoBlack", "WatchingMyMomGoBlack", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[415] = ("InterracialBlowbang", "InterracialBlowbang", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[416] = ("CumBang", "CumBang", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[417] = ("InterracialPickups", "InterracialPickups", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[418] = ("WatchingMyDaughterGoBlack", "WatchingMyDaughterGoBlack", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[419] = ("ZebraGirls", "ZebraGirls", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[420] = ("GloryHoleInitiations", "GloryHoleInitiations", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[421] = ("DogfartBehindTheScenes", "DogfartBehindTheScenes", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[422] = ("BlackMeatWhiteFeet", "BlackMeatWhiteFeet", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[423] = ("SpringThomas", "SpringThomas", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[424] = ("KatieThomas", "KatieThomas", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[425] = ("RuthBlackwell", "RuthBlackwell", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[426] = ("CandyMonroe", "CandyMonroe", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[427] = ("WifeWriting", "WifeWriting", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[428] = ("BarbCummings", "BarbCummings", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[429] = ("TheMinion", "TheMinion", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[430] = ("BlacksOnBoys", "BlacksOnBoys", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[431] = ("GloryholesAndHandjobs", "GloryholesAndHandjobs", "https://www.dogfartnetwork.com", "https://www.dogfartnetwork.com/tour/search.php?search=")
    searchSites[432] = ("Jules Jordan", "Jules Jordan", "https://www.julesjordan.com", "https://www.julesjordan.com/trial/search.php?query=")
    searchSites[433] = ("DDFNetwork", "DDFNetwork", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[434] = ("Sandys Fantasies", "Sandy's Fantasies", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[435] = ("Cherry Jul", "Cherry Jul", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[436] = ("Eve Angel Official", "Eve Angel Official", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[437] = ("Sex Video Casting", "Sex Video Casting", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[438] = ("Hairy Twatter", "Hairy Twatter", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[439] = ("DDF Xtreme", "DDF Xtreme", "https://ddfnetwork.com", "https://ddfnetwork.com/videos/freeword/")
    searchSites[440] = ("DDF Busty", "DDF Busty", "https://ddfbusty.com", "https://ddfbusty.com/videos/freeword/")
    searchSites[441] = ("House of Taboo", "House of Taboo", "https://houseoftaboo.com", "https://houseoftaboo.com/videos/freeword/")
    searchSites[442] = ("Euro Girls on Girls", "Euro Girls on Girls", "https://eurogirlsongirls.com", "https://eurogirlsongirls.com/videos/freeword/")
    searchSites[443] = ("1ByDay", "1ByDay", "https://1by-day.com", "https://1by-day.com/videos/freeword/")
    searchSites[444] = ("Euro Teen Erotica", "Euro Teen Erotica", "https://euroteenerotica.com", "https://euroteenerotica.com/videos/freeword/")
    searchSites[445] = ("Hot Legs and Feet", "Hot Legs & Feet", "https://hotlegsandfeet.com", "https://hotlegsandfeet.com/videos/freeword/")
    searchSites[446] = ("Only Blowjob", "Only Blowjob", "https://onlyblowjob.com", "https://onlyblowjob.com/videos/freeword/")
    searchSites[447] = ("Hands on Hardcore", "Hands on Hardcore", "https://handsonhardcore.com", "https://handsonhardcore.com/videos/freeword/")
    searchSites[448] = ("PerfectGonzo", "PerfectGonzo", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?q=")
    searchSites[449] = ("AllInternal", "AllInternal", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=allinternal&q=")
    searchSites[450] = ("AssTraffic", "AssTraffic", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=asstraffic&q=")
    searchSites[451] = ("CumForCover", "CumForCover", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=cumforcover&q=")
    searchSites[452] = ("Primecups", "Primecups", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=primecups&q=")
    searchSites[453] = ("PurePOV", "PurePOV", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=purepov&q=")
    searchSites[454] = ("SpermSwap", "SpermSwap", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=spermaswap&q=")
    searchSites[455] = ("TamedTeens", "TamedTeens", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=tamedteens&q=")
    searchSites[456] = ("GiveMePink", "GiveMePink", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=givemepink&q=")
    searchSites[457] = ("FistFlush", "FistFlush", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=fistflush&q=")
    searchSites[458] = ("MilfThing", "MilfThing", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=milfthing&q=")
    searchSites[459] = ("PerfectGonzoInterview", "PerfectGonzoInterview", "https://www.perfectgonzo.com", "https://www.perfectgonzo.com/movies?tag=interview&q=")
    searchSites[460] = ("21Sextreme", "21Sextreme", "http://www.21sextreme.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[461] = ("LustyGrandmas", "LustyGrandmas", "http://www.21sextreme.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[462] = ("GrandpasFuckTeens", "GrandpasFuckTeens", "http://www.21sextreme.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[463] = ("TeachMeFisting", "TeachMeFisting", "http://www.21sextreme.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[464] = ("Zoliboy", "Zoliboy", "http://www.21sextreme.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[465] = ("DominatedGirls", "DominatedGirls", "http://www.21sextreme.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[466] = ("Asshole Fever", "Asshole Fever", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[467] = ("Anal College", "Anal College", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[468] = ("Watch Your Wife", "Watch Your Wife", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[469] = ("BadoinkVR", "BadoinkVR", "https://www.badoinkvr.com", "https://badoinkvr.com/vrpornvideos/search/")
    searchSites[470] = ("BabeVR", "BabeVR", "https://www.babevr.com", "https://babevr.com/vrpornvideos/search/")
    searchSites[471] = ("18VR", "18VR", "https://www.18vr.com", "https://18vr.com/vrpornvideos/search/")
    searchSites[472] = ("KinkVR", "KinkVR", "http://www.kinkvr.com", "https://kinkvr.com/bdsm-vr-videos/search/")
    searchSites[473] = ("VRCosplayX", "VRCosplayX", "https://www.vrcosplayx.com", "https://vrcosplayx.com/cosplaypornvideos/search/")
    searchSites[474] = ("VRBangers", "VRBangers", "https://www.vrbangers.com", "https://vrbangers.com/?post_type=video&s=")
    searchSites[475] = ("SexBabesVR", "SexBabesVR", "https://www.sexbabesvr.com", "https://sexbabesvr.com/virtualreality/scene/id/")
    searchSites[476] = ("WankzVR", "WankzVR", "https://www.wankzvr.com", "https://www.wankzvr.com/search?q=")
    searchSites[477] = ("MilfVR", "MilfVR", "https://www.milfvr.com", "https://www.milfvr.com/search?q=")
    searchSites[478] = ("Joymii", "Joymii", "https://www.joymii.com", "https://www.joymii.com/search?query=")
    searchSites[479] = ("POVD", "POVD", "https://www.povd.com", "https://povd.com/video/")
    searchSites[480] = ("Cum4K", "Cum4K", "https://www.cum4k.com", "https://cum4k.com/video/")
    searchSites[481] = ("Exotic4k", "Exotic4k", "https://www.exotic4k.com", "https://exotic4k.com/video/")
    searchSites[482] = ("Tiny4k", "Tiny4k", "https://www.tiny4k.com", "https://tiny4k.com/video/")
    searchSites[483] = ("Lubed", "Lubed", "https://www.lubed.com", "https://lubed.com/video/")
    searchSites[484] = ("PureMature", "PureMature", "https://www.puremature.com", "https://puremature.com/video/")
    searchSites[485] = ("NannySpy", "NannySpy", "https://www.nannyspy.com", "https://nannyspy.com/video/")
    searchSites[486] = ("Holed", "Holed", "https://www.holed.com", "https://holed.com/video/")
    searchSites[487] = ("CastingCouchX", "CastingCouch-X", "https://www.castingcouch-x.com", "https://castingcouch-x.com/video/")
    searchSites[488] = ("SpyFam", "SpyFam", "https://www.spyfam.com", "https://spyfam.com/video/")
    searchSites[489] = ("MyVeryFirstTime", "MyVeryFirstTime", "https://www.myveryfirsttime.com", "https://myveryfirsttime.com/video/")
    searchSites[490] = ("Kink", "Kink", "http://www.kink.com", "http://www.kink.com/search?q=")
    searchSites[491] = ("Brutal Sessions", "Brutal Sessions", "http://www.kink.com", "http://www.kink.com/search?channelIds=brutalsessions&q=")
    searchSites[492] = ("Device Bondage", "Device Bondage", "http://www.kink.com", "http://www.kink.com/search?channelIds=devicebondage&q=")
    searchSites[493] = ("Families Tied", "Families Tied", "http://www.kink.com", "http://www.kink.com/search?channelIds=familiestied&q=")
    searchSites[494] = ("Hardcore Gangbang", "Hardcore Gangbang", "http://www.kink.com", "http://www.kink.com/search?channelIds=hardcoregangbang&q=")
    searchSites[495] = ("Hogtied", "Hogtied", "http://www.kink.com", "http://www.kink.com/search?channelIds=hogtied&q=")
    searchSites[496] = ("Kink Features", "Kink Features", "http://www.kink.com", "http://www.kink.com/search?channelIds=kinkfeatures&q=")
    searchSites[497] = ("Kink University", "Kink University", "http://www.kink.com", "http://www.kink.com/search?channelIds=kinkuniversity&q=")
    searchSites[498] = ("Public Disgrace", "Public Disgrace", "http://www.kink.com", "http://www.kink.com/search?channelIds=publicdisgrace&q=")
    searchSites[499] = ("Sadistic Rope", "Sadistic Rope", "http://www.kink.com", "http://www.kink.com/search?channelIds=sadisticrope&q=")
    searchSites[500] = ("Sex and Submission", "Sex and Submission", "http://www.kink.com", "http://www.kink.com/search?channelIds=sexandsubmission&q=")
    searchSites[501] = ("The Training of O", "The Training of O", "http://www.kink.com", "http://www.kink.com/search?channelIds=thetrainingofo&q=")
    searchSites[502] = ("The Upper Floor", "The Upper Floor", "http://www.kink.com", "http://www.kink.com/search?channelIds=theupperfloor&q=")
    searchSites[503] = ("Water Bondage", "Water Bondage", "http://www.kink.com", "http://www.kink.com/search?channelIds=waterbondage&q=")
    searchSites[504] = ("Everything Butt", "Everything Butt", "http://www.kink.com", "http://www.kink.com/search?channelIds=everythingbutt&q=")
    searchSites[505] = ("Foot Worship", "Foot Worship", "http://www.kink.com", "http://www.kink.com/search?channelIds=footworship&q=")
    searchSites[506] = ("Fucking Machines", "Fucking Machines", "http://www.kink.com", "http://www.kink.com/search?channelIds=fuckingmachines&q=")
    searchSites[507] = ("TS Pussy Hunters", "TS Pussy Hunters", "http://www.kink.com", "http://www.kink.com/search?channelIds=tspussyhunters&q=")
    searchSites[508] = ("TS Seduction", "TS Seduction", "http://www.kink.com", "http://www.kink.com/search?channelIds=tsseduction&q=")
    searchSites[509] = ("Ultimate Surrender", "Ultimate Surrender", "http://www.kink.com", "http://www.kink.com/search?channelIds=ultimatesurrender&q=")
    searchSites[510] = ("30 Minutes of Torment", "30 Minutes of Torment", "http://www.kink.com", "http://www.kink.com/search?channelIds=30minutesoftorment&q=")
    searchSites[511] = ("Bound Gods", "Bound Gods", "http://www.kink.com", "http://www.kink.com/search?channelIds=boundgods&q=")
    searchSites[512] = ("Bound in Public", "Bound in Public", "http://www.kink.com", "http://www.kink.com/search?channelIds=boundinpublic&q=")
    searchSites[513] = ("Butt Machine Boys", "Butt Machine Boys", "http://www.kink.com", "http://www.kink.com/search?channelIds=buttmachineboys&q=")
    searchSites[514] = ("Men on Edge", "Men on Edge", "http://www.kink.com", "http://www.kink.com/search?channelIds=menonedge&q=")
    searchSites[515] = ("Naked Kombat", "Naked Kombat", "http://www.kink.com", "http://www.kink.com/search?channelIds=nakedkombat&q=")
    searchSites[516] = ("Divine Bitches", "Divine Bitches", "http://www.kink.com", "http://www.kink.com/search?channelIds=divinebitches&q=")
    searchSites[517] = ("Electrosluts", "Electrosluts", "http://www.kink.com", "http://www.kink.com/search?channelIds=electrosluts&q=")
    searchSites[518] = ("Men in Pain", "Men In Pain", "http://www.kink.com", "http://www.kink.com/search?channelIds=meninpain&q=")
    searchSites[519] = ("Whipped Ass", "Whipped Ass", "http://www.kink.com", "http://www.kink.com/search?channelIds=whippedass&q=")
    searchSites[520] = ("Wired Pussy", "Wired Pussy", "http://www.kink.com", "http://www.kink.com/search?channelIds=wiredpussy&q=")
    searchSites[521] = ("Bound Gang Bangs", "Bound Gang Bangs", "http://www.kink.com", "http://www.kink.com/search?channelIds=boundgangbangs&q=")
    searchSites[522] = ("Manuel Ferrara", "Manuel Ferrara", "https://www.manuelferrara.com", "https://www.manuelferrara.com/trial/search.php?query=")
    searchSites[523] = ("The Ass Factory", "The Ass Factory", "https://www.theassfactory.com", "https://www.theassfactory.com/trial/search.php?query=")
    searchSites[524] = ("Sperm Swallowers", "Sperm Swallowers", "https://www.spermswallowers.com", "https://www.spermswallowers.com/trial/search.php?query=")
    searchSites[525] = ("Nubile Films", "Nubile Films", "https://nubilefilms.com", "https://nubilefilms.com/video/")
    searchSites[526] = ("Nubiles Porn", "Nubiles Porn", "https://nubiles-porn.com", "https://nubiles-porn.com/video/")
    searchSites[527] = ("Step Siblings Caught", "Step Siblings Caught", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/16/")
    searchSites[528] = ("Moms Teach Sex", "Moms Teach Sex", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/8/")
    searchSites[529] = ("Bad Teens Punished", "Bad Teens Punished", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/18/")
    searchSites[530] = ("Princess Cum", "Princess Cum", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/17/")
    searchSites[531] = ("Nubiles Unscripted", "Nubiles Unscripted", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/22/")
    searchSites[532] = ("Nubiles Casting", "Nubiles Casting", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/6/")
    searchSites[533] = ("Petite HD Porn", "Petite HD Porn", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/9/")
    searchSites[534] = ("Driver XXX", "Driver XXX", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/13/")
    searchSites[535] = ("Petite Ballerinas Fucked", "Petite Ballerinas Fucked", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/14/")
    searchSites[536] = ("Teacher Fucks Teens", "Teacher Fucks Teens", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/15/")
    searchSites[537] = ("Bountyhunter Porn", "Bountyhunter Porn", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/23/")
    searchSites[538] = ("Daddys Lil Angel", "Daddy's Lil Angel", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/25/")
    searchSites[539] = ("My Family Pies", "My Family Pies", "https://nubiles-porn.com", "https://nubiles-porn.com/video/website/26/")
    searchSites[540] = ("NubilesNet", "Nubiles", "https://nubiles.net", "https://nubiles.net/video/")
    searchSites[541] = ("Bratty Sis", "Bratty Sis", "https://brattysis.com", "https://brattysis.com/video/gallery/")
    searchSites[542] = ("Anilos", "Anilos", "https://anilos.com", "https://anilos.com/video/")
    searchSites[543] = ("Hot Crazy Mess", "Hot Crazy Mess", "https://hotcrazymess.com", "https://hotcrazymess.com/video/")
    searchSites[544] = ("NF Busty", "NF Busty", "https://nfbusty.com", "https://nfbusty.com/video/")
    searchSites[545] = ("That Sitcom Show", "That Sitcom Show", "https://thatsitcomshow.com", "https://thatsitcomshow.com/video/")
    searchSites[546] = ("FuckedHard18", "FuckedHard18", "http://fuckedhard18.com", "http://fuckedhard18.com/membersarea/search.php?st=advanced&site[]=5&qall=")
    searchSites[547] = ("MassageGirls18", "MassageGirls18", "http://massagegirls18.com", "http://massagegirls18.com/membersarea/search.php?st=advanced&site[]=4&qall=")
    searchSites[548] = ("BellaPass", "BellaPass", "https://www.bellapass.com", "https://bellapass.com/search.php?query=")
    searchSites[549] = ("Bryci", "Bryci", "https://www.bryci.com", "https://bryci.com/search.php?query=")
    searchSites[550] = ("Katie Banks", "Katie Banks", "https://www.katiebanks.com", "https://katiebanks.com/search.php?query=")
    searchSites[551] = ("Alexis Monroe", "Alexis Monroe", "https://www.alexismonroe.com", "https://alexismonroe.com/search.php?query=")
    searchSites[552] = ("Cali Carter", "Cali Carter", "https://www.calicarter.com", "https://calicarter.com/search.php?query=")
    searchSites[553] = ("Talia Shepard", "Talia Shepard", "https://www.taliashepard.com", "https://taliashepard.com/search.php?query=")
    searchSites[554] = ("Jana Fox", "Jana Fox", "https://www.janafox.com", "https://janafox.com/search.php?query=")
    searchSites[555] = ("Monroe Lee", "Monroe Lee", "https://www.monroelee.com", "https://monroelee.com/search.php?query=")
    searchSites[556] = ("Aleah Jasmine", "Aleah Jasmine", "https://www.aleahjasmine.com", "https://aleahjasmine.com/search.php?query=")
    searchSites[557] = ("Cece September", "Cece September", "https://www.ceceseptember.com", "https://ceceseptember.com/search.php?query=")
    searchSites[558] = ("Hunter Leigh", "Hunter Leigh", "https://www.hunterleigh.com", "https://hunterleigh.com/search.php?query=")
    searchSites[559] = ("Ava Dawn", "Ava Dawn", "https://www.avadawn.com", "https://avadawn.com/search.php?query=")
    searchSites[560] = ("Bella Next Door", "Bella Next Door", "https://www.bellanextdoor.com", "https://bellanextdoor.com/search.php?query=")
    searchSites[561] = ("Joe Perv", "Joe Perv", "https://www.joeperv.com", "https://joeperv.com/search.php?query=")
    searchSites[562] = ("HD 19", "HD 19", "https://www.hd19.com", "https://hd19.com/search.php?query=")
    searchSites[563] = ("Bella HD", "Bella HD", "https://www.bellahd.com", "https://bellahd.com/search.php?query=")
    searchSites[564] = ("Amateur Allure", "Amateur Allure", "https://www.amateurallure.com", "https://www.amateurallure.com/tour/search.php?st=advanced&cat%5B%5D=5&qany=")
    searchSites[565] = ("Swallow Salon", "Swallow Salon", "https://www.swallowsalon.com", "https://www.swallowsalon.com/search.php?st=advanced&cat%5B%5D=5&format=h&qany=")
    searchSites[566] = ("Black Valley Girls", "Black Valley Girls", "https://www.blackvalleygirls.com", "https://store.psmcdn.net/BCG-organic-dhed18vuav")
    searchSites[567] = ("Sis Loves Me", "Sis Loves Me", "https://www.sislovesme.com", "https://store.psmcdn.net/SLM-organic-b75inmn9fu")
    searchSites[568] = ("Manyvids", "Manyvids", "https://www.manyvids.com", "https://www.manyvids.com/video/")
    searchSites[569] = ("SinsVR", "SinsVR", "https://www.sinsvr.com", "https://sinsvr.com/virtualreality/scene/id/")
    searchSites[570] = ("StasyQ VR", "StasyQ VR", "https://www.stasyqvr.com", "https://stasyqvr.com/virtualreality/scene/id/")
    searchSites[571] = ("First Class POV", "First Class POV", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[572] = ("Intimate Lesbians", "Intimate Lesbians", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[573] = ("The Stripper Experience", "The Stripper Experience", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[574] = ("Porn Goes Pro", "Porn Goes Pro", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[575] = ("Jessica Jaymes XXX", "Jessica Jaymes XXX", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[576] = ("Pornstar Tease", "Pornstar Tease", "https://www.spizoo.com", "https://www.spizoo.com/search.php?query=")
    searchSites[577] = ("Raw Attack", "Raw Attack", "https://www.rawattack.com", "https://rawattack.com/search.php?query=")
    searchSites[578] = ("CzechVR", "CzechVR", "https://www.czechvr.com", "https://www.czechvr.com/model-")
    searchSites[579] = ("CzechVR Fetish", "CzechVR Fetish", "https://www.czechvrfetish.com", "https://www.czechvrfetish.com/model-")
    searchSites[580] = ("CzechVR Casting", "CzechVR Casting", "https://www.czechvrcasting.com", "https://www.czechvrcasting.com/model-")
    searchSites[581] = ("Slut Stepmom", "Slut Stepmom", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[582] = ("ZZ Series", "ZZ Series", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[583] = ("Latina Sex Tapes", "Latina Sex Tapes", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[584] = ("Mano Job", "Mano Job", "https://www.finishesthejob.com", "https://www.finishesthejob.com/search?search=")
    searchSites[585] = ("The Dick Suckers", "The Dick Suckers", "https://www.finishesthejob.com", "https://www.finishesthejob.com/search?search=")
    searchSites[586] = ("Mister POV", "Mister POV", "https://www.finishesthejob.com", "https://www.finishesthejob.com/search?search=")
    searchSites[587] = ("4K Desire", "4K Desire", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[588] = ("All Interracial", "All Interracial", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[589] = ("Bang My Stepmom", "Bang My Stepmom", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[590] = ("Big Tits Like Big Dicks", "Big Tits Like Big Dicks", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[591] = ("Bubbly Massage", "Bubbly Massage", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[592] = ("Cougar Sex Club", "Cougar Sex Club", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[593] = ("Ebony Internal", "Ebony Internal", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[594] = ("Escort Trick", "Escort Trick", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[595] = ("Exploited 18", "Exploited 18", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[596] = ("Handjob Harry", "Handjob Harry", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[597] = ("I am Eighteen", "I am Eighteen", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[598] = ("Lesbian Sistas", "Lesbian Sistas", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[599] = ("Make Them Gag", "Make Them Gag", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[600] = ("My Milf Boss", "My Milf Boss", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[601] = ("Not So Innocent Teens", "Not So Innocent Teens", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[602] = ("Rap Video Auditions", "Rap Video Auditions", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[603] = ("Real Blowjob Auditions", "Real Blowjob Auditions", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[604] = ("Round Juicy Butts", "Round Juicy Butts", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[605] = ("Schoolgirl Internal", "Schoolgirl Internal", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[606] = ("Service Whores", "Service Whores", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[607] = ("Sex For Grades", "Sex For Grades", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[608] = ("Spoiled Slut", "Spoiled Slut", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[609] = ("Swallow For Cash", "Swallow For Cash", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[610] = ("Tight Holes Big Poles", "Tight Holes Big Poles", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[611] = ("Wank My Wood", "Wank My Wood", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[612] = ("Wankz TV", "Wankz TV", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[613] = ("Whale Tail'n", "Whale Tail'n", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[614] = ("Wild Massage", "Wild Massage", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[615] = ("XXX At Work", "XXX At Work", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[616] = ("Young Dirty Lesbians", "Young Dirty Lesbians", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[617] = ("Young Sluts Hardcore", "Young Sluts Hardcore", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[618] = ("Matrix Models", "Matrix Models", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[619] = ("Blow Patrol", "Blow Patrol", "https://www.wankz.com", "https://www.wankz.com/search?q=")
    searchSites[620] = ("Sleazy Stepdad", "Sleazy Stepdad", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[621] = ("SexArt", "SexArt", "https://www.sexart.com", "https://www.sexart.com/api")
    searchSites[622] = ("TheLifeErotic", "TheLifeErotic", "https://www.thelifeerotic.com", "https://www.thelifeerotic.com/api")
    searchSites[623] = ("VivThomas", "VivThomas", "https://www.vivthomas.com", "https://www.vivthomas.com/api")
    searchSites[624] = ("Baeb", "Baeb", "http://www.baeb.com", "http://baeb.com/video/")
    searchSites[625] = ("Open Family", "Open Family", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[626] = ("Family Strokes", "Family Strokes", "https://www.familystrokes.com", "https://store.psmcdn.net/FS-organic-1rstmyhj44")
    searchSites[627] = ("Tonights Girlfriend", "Tonights Girlfriend", "https://www.tonightsgirlfriend.com", "https://www.tonightsgirlfriend.com/pornstar/")
    searchSites[628] = ("KarupsPC", "Karups Private Collection", "https://www.karups.com", "https://www.karups.com/models/search/")
    searchSites[629] = ("KarupsHA", "Karups Hometown Amateurs", "https://www.karups.com", "https://www.karups.com/models/search/")
    searchSites[630] = ("KarupsOW", "Karups Older Women", "https://www.karups.com", "https://www.karups.com/models/search/")
    searchSites[631] = ("Teen Mega World", "Teen Mega World", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[632] = ("18 First Sex", "18 First Sex", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[633] = ("ATMovs", "ATMovs", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[634] = ("About Girls Love", "About Girls Love", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[635] = ("Anal Angels", "Anal Angels", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[636] = ("Anal Beauty", "Anal Beauty", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[637] = ("Beauty 4K", "Beauty 4K", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[638] = ("BeautyAngels", "BeautyAngels", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[639] = ("Coeds Reality", "Coeds Reality", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[640] = ("Creampie Angels", "Creampie Angels", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[641] = ("Dirty Coach", "Dirty Coach", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[642] = ("Dirty Doctor", "Dirty Doctor", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[643] = ("el Porno Latino", "el Porno Latino", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[644] = ("ExGfBox", "ExGfBox", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[645] = ("First BGG", "First BGG", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[646] = ("Fuck Studies", "Fuck Studies", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[647] = ("Gag N Gape", "Gag N Gape", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[648] = ("Home Teen Vids", "Home Teen Vids", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[649] = ("Home Toy Teens", "Home Toy Teens", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[650] = ("Lolly Hardcore", "Lolly Hardcore", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[651] = ("No Boring", "No Boring", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[652] = ("Nubile Girls HD", "Nubile Girls HD", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[653] = ("NylonsX", "NylonsX", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[654] = ("Old N Young", "Old N Young", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[655] = ("Private Teen Video", "Private Teen Video", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[656] = ("Solo Teen Girls", "Solo Teen Girls", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[657] = ("Squirting Virgin", "Squirting Virgin", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[658] = ("Teen Sex Mania", "Teen Sex Mania", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[659] = ("Teen Stars Only", "Teen Stars Only", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[660] = ("Teens 3 Some", "Teens 3 Some", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[661] = ("TmwVRnet", "TmwVRnet", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[662] = ("Tricky Masseur", "Tricky Masseur", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[663] = ("WOW Orgasms", "WOW Orgasms", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[664] = ("Watch Me Fucked", "Watch Me Fucked", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[665] = ("X Angels", "X Angels", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[666] = ("Teen Sex Movs", "Teen Sex Movs", "http://teenmegaworld.net", "http://teenmegaworld.net/search.php?query=")
    searchSites[667] = ("PJGirls", "PJGirls", "http://www.pjgirls.com", "http://www.pjgirls.com/en/videos/?fulltext=")
    searchSites[668] = ("Screwbox", "Screwbox", "https://screwbox.com", "https://screwbox.com/search.php?query=")
    searchSites[669] = ("Dorcel Club", "Dorcel Club", "https://www.dorcelclub.com", "https://www.dorcelclub.com/en/search?search=")
    searchSites[670] = ("TushyRaw", "TushyRaw", "https://www.tushyraw.com", "https://www.tushyraw.com/api")
    searchSites[671] = ("Deeper", "Deeper", "https://www.deeper.com", "https://www.deeper.com/api")
    searchSites[672] = ("MissaX", "MissaX", "https://missax.com", "https://missax.com/tour/search.php?query=")
    searchSites[673] = ("AllHerLuv", "AllHerLuv", "https://allherluv.com", "https://allherluv.com/tour/search.php?query=")
    searchSites[674] = ("Mylf", "Mylf", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[675] = ("MylfBoss", "MylfBoss", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[676] = ("MylfBlows", "MylfBlows", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[677] = ("Milfty", "Milfty", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[678] = ("Got Mylf", "Got Mylf", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[679] = ("Mom Drips", "Mom Drips", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[680] = ("Mylfed", "Mylfed", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[681] = ("Milf Body", "Milf Body", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[682] = ("Lone Milf", "Lone Milf", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[683] = ("Full Of JOI", "Full Of JOI", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[684] = ("ManualAddActors", "ManualAddActors", "", "")
    searchSites[685] = ("First Anal Quest", "First Anal Quest", "http://www.firstanalquest.com", "http://www.firstanalquest.com/search/?q=")
    searchSites[686] = ("PervMom", "PervMom", "https://www.pervmom.com", "https://store.psmcdn.net/PVM-organic-rg7wwuc7uh")
    searchSites[687] = ("Chantas Bitches", "Chantas Bitches", "http://www.kink.com", "http://www.kink.com/search?channelIds=chantasbitches&q=")
    searchSites[688] = ("Hegre", "Hegre", "http://www.hegre.com", "http://www.hegre.com/search?q=")
    searchSites[689] = ("Femdom Empire", "Femdom Empire", "https://femdomempire.com", "https://femdomempire.com/tour/search.php?st=advanced&qany=")
    searchSites[690] = ("Day With A Porn Star", "Day With A Porn Star", "http://www.brazzers.com", "https://www.brazzers.com/videos-search/")
    searchSites[691] = ("Watch Your Mom", "Watch Your Mom", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[692] = ("Butt Plays", "Butt Plays", "http://www.21sextury.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[693] = ("Dorcel Vision", "Dorcel Vision", "https://www.dorcelvision.com", "https://www.dorcelvision.com/en/search?type=4&keyword=")
    searchSites[694] = ("Feminized", "Feminized", "http://feminized.com", "http://feminized.com/tour/search.php?st=advanced&qany=")
    searchSites[695] = ("XConfessions", "XConfessions", "https://xconfessions.com", "https://2rzi1cnto2-dsn.algolia.net/1/indexes/*/queries")
    searchSites[696] = ("Czech Amateurs", "Czech Amateurs", "https://czechamateurs.com", "https://czechamateurs.com/tour/search/?q=")
    searchSites[697] = ("Czech Bangbus", "Czech Bangbus", "https://czechbangbus.com", "https://czechbangbus.com/tour/search/?q=")
    searchSites[698] = ("Czech Bitch", "Czech Bitch", "https://czechbitch.com", "https://czechbitch.com/tour/search/?q=")
    searchSites[699] = ("Czech Cabins", "Czech Cabins", "https://czechcabins.com", "https://czechcabins.com/tour/search/?q=")
    searchSites[700] = ("Czech Couples", "Czech Couples", "https://czechcouples.com", "https://czechcouples.com/tour/search/?q=")
    searchSites[701] = ("Czech Dungeon", "Czech Dungeon", "https://czechdungeon.com", "https://czechdungeon.com/tour/search/?q=")
    searchSites[702] = ("Czech Estrogenolit", "Czech Estrogenolit", "https://czechestrogenolit.com", "https://czechestrogenolit.com/tour/search/?q=")
    searchSites[703] = ("Czech Experiment", "Czech Experiment", "https://czechexperiment.com", "https://czechexperiment.com/tour/search/?q=")
    searchSites[704] = ("Czech Fantasy", "Czech Fantasy", "https://czechfantasy.com", "https://czechfantasy.com/tour/search/?q=")
    searchSites[705] = ("Czech First Video", "Czech First Video", "https://czechfirstvideo.com", "https://czechfirstvideo.com/tour/search/?q=")
    searchSites[706] = ("Czech Game", "Czech Game", "https://czechgame.com", "https://czechgame.com/tour/search/?q=")
    searchSites[707] = ("Czech Gangbang", "Czech Gangbang", "https://czechgangbang.com", "https://czechgangbang.com/tour/search/?q=")
    searchSites[708] = ("Czech Garden Party", "Czech Garden Party", "https://czechgardenparty.com", "https://czechgardenparty.com/tour/search/?q=")
    searchSites[709] = ("Czech Harem", "Czech Harem", "https://czechharem.com", "https://czechharem.com/tour/search/?q=")
    searchSites[710] = ("Czech Home Orgy", "Czech Home Orgy", "https://czechhomeorgy.com", "https://czechhomeorgy.com/tour/search/?q=")
    searchSites[711] = ("Czech Lesbians", "Czech Lesbians", "https://czechlesbians.com", "https://czechlesbians.com/tour/search/?q=")
    searchSites[712] = ("Czech Massage", "Czech Massage", "https://czechmassage.com", "https://czechmassage.com/tour/search/?q=")
    searchSites[713] = ("Czech Mega Swingers", "Czech Mega Swingers", "https://czechmegaswingers.com", "https://czechmegaswingers.com/tour/search/?q=")
    searchSites[714] = ("Czech Orgasm", "Czech Orgasm", "https://czechorgasm.com", "https://czechorgasm.com/tour/search/?q=")
    searchSites[715] = ("Czech Parties", "Czech Parties", "https://czechparties.com", "https://czechparties.com/tour/search/?q=")
    searchSites[716] = ("Czech Pawn Shop", "Czech Pawn Shop", "https://czechpawnshop.com", "https://czechpawnshop.com/tour/search/?q=")
    searchSites[717] = ("Czech Pool", "Czech Pool", "https://czechpool.com", "https://czechpool.com/tour/search/?q=")
    searchSites[718] = ("Czech Sauna", "Czech Sauna", "https://czechsauna.com", "https://czechsauna.com/tour/search/?q=")
    searchSites[719] = ("Czech Sharking", "Czech Sharking", "https://czechsharking.com", "https://czechsharking.com/tour/search/?q=")
    searchSites[720] = ("Czech Snooper", "Czech Snooper", "https://czechsnooper.com", "https://czechsnooper.com/tour/search/?q=")
    searchSites[721] = ("Czech Solarium", "Czech Solarium", "https://czechsolarium.com", "https://czechsolarium.com/tour/search/?q=")
    searchSites[722] = ("Czech Spy", "Czech Spy", "https://czechspy.com", "https://czechspy.com/tour/search/?q=")
    searchSites[723] = ("Czech Streets", "Czech Streets", "https://czechstreets.com", "https://czechstreets.com/tour/search/?q=")
    searchSites[724] = ("Czech Super Models", "Czech Super Models", "https://czechsupermodels.com", "https://czechsupermodels.com/tour/search/?q=")
    searchSites[725] = ("Czech Taxi", "Czech Taxi", "https://czechtaxi.com", "https://czechtaxi.com/tour/search/?q=")
    searchSites[726] = ("Czech Toilets", "Czech Toilets", "https://czechtoilets.com", "https://czechtoilets.com/tour/search/?q=")
    searchSites[727] = ("Czech Twins", "Czech Twins", "https://czechtwins.com", "https://czechtwins.com/tour/search/?q=")
    searchSites[728] = ("Czech Wife Swap", "Czech Wife Swap", "https://czechwifeswap.com", "https://czechwifeswap.com/tour/search/?q=")
    searchSites[729] = ("ArchAngel", "ArchAngel", "https://www.archangelvideo.com", "https://www.archangelvideo.com/tour/search.php?query=")
    searchSites[730] = ("We Are Hairy", "We Are Hairy", "https://www.wearehairy.com", "https://www.wearehairy.com/search/?query=")
    searchSites[731] = ("Love Her Feet", "Love Her Feet", "https://www.loveherfeet.com", "https://www.loveherfeet.com/tour/search.php?query=")
    searchSites[732] = ("MomPOV", "MomPOV", "http://www.mompov.com", "http://www.mompov.com/tour/?s=")
    searchSites[733] = ("Property Sex", "Property Sex", "https://www.propertysex.com", "https://site-api.project1service.com")
    searchSites[735] = ("Fucked and Bound", "Fucked and Bound", "http://www.kink.com", "http://www.kink.com/search?channelIds=fuckedandbound&q=")
    searchSites[736] = ("Captive Male", "Captive Male", "http://www.kink.com", "http://www.kink.com/search?channelIds=captivemale&q=")
    searchSites[737] = ("TransAngels", "TransAngels", "https://www.transangels.com", "https://site-api.project1service.com")
    searchSites[738] = ("Girls Gone Pink", "Girls Gone Pink", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[739] = ("Real Slut Party", "Real Slut Party", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[740] = ("Mofos Lab", "Mofos Lab", "https://www.mofos.com", "https://site-api.project1service.com")
    searchSites[741] = ("Straplezz", "Straplezz", "https://straplezz.com", "https://straplezz.com/updates/")
    searchSites[742] = ("LittleCaprice", "LittleCaprice", "https://www.littlecaprice-dreams.com", "https://www.littlecaprice-dreams.com/?s=")
    searchSites[743] = ("WowGirls", "WowGirls", "https://www.wowgirls.xxx", "https://www.wowgirls.xxx/?s=")
    searchSites[744] = ("VIPissy", "VIPissy", "https://www.vipissy.com", "https://www.vipissy.com/updates?search=")
    searchSites[745] = ("GirlsOutWest", "GirlsOutWest", "https://tour.girlsoutwest.com", "https://tour.girlsoutwest.com/trailers/")
    searchSites[746] = ("Girls Rimming", "Girls Rimming", "https://www.girlsrimming.com", "https://www.girlsrimming.com/tour/trailers/")
    searchSites[747] = ("Gangbang Creampie", "Gangbang Creampie", "https://gangbangcreampie.com", "https://gangbangcreampie.com/tour/search.php?query=")
    searchSites[749] = ("Show My BF", "Show My BF", "https://tour.naughtyamerica.com", "https://i6p9q9r18e-3.algolianet.com/1/indexes/*/queries")
    searchSites[748] = ("DadCrush", "DadCrush", "https://www.dadcrush.com", "https://store.psmcdn.net/DC-organic-w8xs8e0dv3")
    searchSites[750] = ("POV Massage", "POV Massage", "http://www.fantasymassage.com", "http://www.fantasymassage.com/en/search/")
    searchSites[751] = ("Step Secrets", "Step Secrets", "http://www.stepsecrets.com", "https://stepsecrets.com/?query=")
    searchSites[752] = ("VRHush", "VRHush", "https://www.vrhush.com", "https://vrhush.com/scenes/")
    searchSites[753] = ("MetArt", "MetArt", "https://www.metart.com", "https://www.metart.com/api")
    searchSites[754] = ("MetArtX", "MetArtX", "https://www.metartx.com", "https://www.metartx.com/api")
    searchSites[755] = ("Nubiles ET", "Nubiles ET", "https://nubileset.com", "https://nubileset.com/video/")
    searchSites[756] = ("Detention Girls", "Detention Girls", "https://detentiongirls.com", "https://detentiongirls.com/video/")
    searchSites[757] = ("Mylfdom", "Mylfdom", "https://www.mylfdom.com", "https://www.mylfdom.com/movies/")
    searchSites[758] = ("Fitting-Room", "Fitting-Room", "https://www.fitting-room.com", "https://www.fitting-room.com/videos/")
    searchSites[759] = ("FamilyHookups", "FamilyHookups", "https://www.familyhookups.com", "https://site-api.project1service.com")
    searchSites[760] = ("Clips4Sale", "Clips4Sale", "https://www.clips4sale.com", "https://www.clips4sale.com/studio/")
    searchSites[761] = ("VogoV", "VogoV", "https://vogov.com", "https://vogov.com/search/?q=")
    searchSites[762] = ("Ultrafilms", "Ultrafilms", "https://www.ultrafilms.xxx", "https://www.ultrafilms.xxx/?s=")
    searchSites[763] = ("FuckingAwesome", "FuckingAwesome", "https://fuckingawesome.com", "https://fuckingawesome.com/search/videos/")
    searchSites[764] = ("ToughLoveX", "ToughLoveX", "https://tour.toughlovex.com", "https://tour.toughlovex.com/models?letter=")
    searchSites[765] = ("CumLouder", "CumLouder", "https://www.cumlouder.com", "https://www.cumlouder.com/search?q=")
    searchSites[766] = ("Deep Lush", "Deep Lush", "https://deeplush.com", "https://deeplush.com/video/")
    searchSites[767] = ("AllAnal", "AllAnal", "https://tour.allanal.com", "https://tour.allanal.com/view/")
    searchSites[768] = ("TurningTwistys", "TurningTwistys", "https://www.twistys.com", "https://site-api.project1service.com")
    searchSites[769] = ("GirlCum", "GirlCum", "https://www.girlcum.com", "https://www.girlcum.com/video/")
    searchSites[770] = ("ZeroTolerance", "ZeroTolerance", "http://www.ztod.com", "http://www.ztod.com/videos?query=")
    searchSites[771] = ("ClubFilly", "ClubFilly", "http://www.clubfilly.com", "http://www.clubfilly.com/scenefocus.php?vnum=V")
    searchSites[772] = ("Insex", "Insex", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[773] = ("Sexually Broken", "Sexuallybroken", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[774] = ("Infernal Restraints", "Infernalrestraints", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[775] = ("Real Time Bondage", "Realtimebondage", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[776] = ("Hardtied", "Hardtied", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[777] = ("Topgrl", "Topgrl", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[778] = ("Sensual Pain", "Sensualpain", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[779] = ("Paintoy", "Paintoy", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[780] = ("Renderfiend", "Renderfiend", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[781] = ("Hotel Hostages", "Hotelhostages", "https://www.insexondemand.com", "https://www.insexondemand.com/iod/home.php?s=")
    searchSites[782] = ("GirlGirl", "GirlGirl", "https://www.girlgirl.com", "https://www.girlgirl.com/trial/search.php?query=")
    searchSites[783] = ("Cherry Pimps", "Cherry Pimps", "https://www.cherrypimps.com", "https://cherrypimps.com/search.php?query=")
    searchSites[784] = ("Wild On Cam", "Wild On Cam", "https://www.cherrypimps.com", "https://cherrypimps.com/search.php?query=")
    searchSites[785] = ("Cherry Spot", "Cherry Spot", "https://www.cherrypimps.com", "https://cherrypimps.com/search.php?query=")
    searchSites[786] = ("Britney Amber", "Britney Amber", "https://www.cherrypimps.com", "https://cherrypimps.com/search.php?query=")
    searchSites[787] = ("Confessions", "Confessions.XXX", "https://www.pimp.xxx", "https://pimp.xxx/search.php?query=")
    searchSites[788] = ("Cucked", "Cucked.XXX", "https://www.pimp.xxx", "https://pimp.xxx/search.php?query=")
    searchSites[789] = ("Drilled", "Drilled.XXX", "https://www.pimp.xxx", "https://pimp.xxx/search.php?query=")
    searchSites[790] = ("BCM", "BCM.XXX", "https://www.pimp.xxx", "https://pimp.xxx/search.php?query=")
    searchSites[791] = ("Petite", "Petite.XXX", "https://www.pimp.xxx", "https://pimp.xxx/search.php?query=")
    searchSites[792] = ("Family", "Family.XXX", "https://www.pimp.xxx", "https://pimp.xxx/search.php?query=")
    searchSites[793] = ("Wicked", "Wicked Pictures", "https://www.wicked.com", "https://wicked.com/en/movie/")
    searchSites[794] = ("18OnlyGirls", "18 Only Girls", "http://www.18onlygirls.tv", "http://18onlygirls.tv/?s=")
    searchSites[795] = ("GirlCore", "GirlCore", "https://www.girlsway.com", "https://www.girlsway.com/en/video/1/1/")
    searchSites[796] = ("Moms On Moms", "Moms On Moms", "https://www.girlsway.com", "https://www.girlsway.com/en/video/1/1/")
    searchSites[797] = ("We Like Girls", "We Like Girls", "https://www.girlsway.com", "https://www.girlsway.com/en/video/1/1/")
    searchSites[798] = ("Lil Humpers", "Lil Humpers", "https://www.lilhumpers.com", "https://site-api.project1service.com")
    searchSites[799] = ("Bellesa Films", "Bellesa Films", "https://www.bellesafilms.com/", "https://site-api.project1service.com")
    searchSites[800] = ("ClubSeventeen", "ClubSeventeen", "https://www.clubseventeen.com", "https://www.clubseventeen.com/video.php?slug=")
    searchSites[801] = ("Elegant Angel", "Elegant Angel", "https://www.elegantangel.com", "https://www.elegantangel.com/Search?fq=")
    searchSites[802] = ("Family Sinners", "Family Sinners", "https://www.familysinners.com", "https://site-api.project1service.com")
    searchSites[803] = ("ReidMyLips", "ReidMyLips", "https://www.reidmylips.com", "https://www.reidmylips.com/")
    searchSites[804] = ("Playboy Plus", "Playboy Plus", "https://www.playboyplus.com", "https://www.playboyplus.com/search")
    searchSites[805] = ("Meana Wolf", "Meana Wolf", "https://meanawolf.elxcomplete.com", "https://meanawolf.elxcomplete.com/search.php?query=")
    searchSites[806] = ("Transsensual", "Transsensual", "https://www.transsensual.com/", "https://site-api.project1service.com")
    searchSites[807] = ("DaughterSwap", "DaughterSwap", "https://www.daughterswap.com", "https://store.psmcdn.net/DSW-organic-dfangeym88")
    searchSites[808] = ("Erito", "Erito", "https://www.erito.com", "https://site-api.project1service.com")
    searchSites[809] = ("True Amateurs", "True Amateurs", "https://www.trueamateurs.com", "https://site-api.project1service.com")
    searchSites[810] = ("Hustler", "Hustler", "https://hustler.com", "https://hustler.com/search.php?query=")
    searchSites[811] = ("AmourAngels", "AmourAngels", "http://www.amourangels.com", "http://www.amourangels.com/z_cover_")
    searchSites[812] = ("JAV", "JAV", "https://www.r18.com", "https://www.r18.com/common/search/searchword=")
    searchSites[813] = ("Bang", "Bang", "https://www.bang.com", "https://617fb597b659459bafe6472470d9073a.us-east-1.aws.found.io/videos/video/_search")
    searchSites[814] = ("Vivid", "Vivid", "https://www.vivid.com", "https://www.vivid.com/")
    searchSites[815] = ("JAY's POV", "JAY's POV", "https://jayspov.net", "https://jayspov.net/MemberSceneSearch?q=")
    searchSites[816] = ("Errotica Archives", "Errotica Archives", "https://www.errotica-archives.com", "https://www.errotica-archives.com/api")
    searchSites[817] = ("ALS Scan", "ALS Scan", "https://www.alsscan.com", "https://www.alsscan.com/api")
    searchSites[818] = ("Rylsky Art", "Rylsky Art", "https://www.rylskyart.com", "https://www.rylskyart.com/api")
    searchSites[819] = ("Eternal Desire", "Eternal Desire", "https://www.eternaldesire.com", "https://www.eternaldesire.com/api")
    searchSites[820] = ("Stunning18", "Stunning18", "https://www.stunning18.com", "https://www.stunning18.com/api")
    searchSites[821] = ("Love Hairy", "Love Hairy", "https://www.lovehairy.com", "https://www.lovehairy.com/api")
    searchSites[822] = ("GF Revenge", "GF Revenge", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[823] = ("Black GFs", "Black GFs", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[824] = ("Dare Dorm", "Dare Dorm", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[825] = ("Crazy Asian GFs", "Crazy Asian GFs", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[826] = ("Crazy College GFs", "Crazy College GFs", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[827] = ("Horny Birds", "Horny Birds", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[828] = ("Reckless in Miami", "Reckless in Miami", "https://www.realitykings.com", "https://site-api.project1service.com")
    searchSites[829] = ("AmateurCFNM", "AmateurCFNM", "https://www.amateurcfnm.com/", "https://www.amateurcfnm.com/models/")
    searchSites[830] = ("PureCFNM", "PureCFNM", "https://www.purecfnm.com/", "https://www.purecfnm.com/models/")
    searchSites[831] = ("CFNMGames", "CFNMGames", "https://www.cfnmgames.com/", "https://www.cfnmgames.com/models/")
    searchSites[832] = ("GirlsAbuseGuys", "GirlsAbuseGuys", "https://www.girlsabuseguys.com/", "https://www.girlsabuseguys.com/models/")
    searchSites[833] = ("HeyLittleDick", "HeyLittleDick", "https://www.heylittledick.com/", "https://www.heylittledick.com/models/")
    searchSites[834] = ("LadyVoyeurs", "LadyVoyeurs", "https://www.ladyvoyeurs.com/", "https://www.ladyvoyeurs.com/models/")
    searchSites[835] = ("BAMVisions", "BAMVisions", "https://tour.bamvisions.com", "https://tour.bamvisions.com/search.php?st=advanced&qall=")
    searchSites[836] = ("ATKGirlfriends", "ATKGirlfriends", "https://www.atkgirlfriends.com", "https://www.atkgirlfriends.com/tour/model/")
    searchSites[837] = ("Wank It Now", "Wank It Now", "https://www.wankitnow.com", "https://www.wankitnow.com/?s=")
    searchSites[838] = ("Bopping Babes", "Bopping Babes", "https://www.boppingbabes.com", "https://www.boppingbabes.com/v2/?s=")
    searchSites[839] = ("Upskirt Jerk", "Upskirt Jerk", "https://www.upskirtjerk.com", "https://www.upskirtjerk.com/?s=")
    searchSites[840] = ("Interracial Pass", "Interracial Pass", "https://www.interracialpass.com", "https://www.interracialpass.com/t1/search.php?query=")
    searchSites[841] = ("LookAtHerNow", "LookAtHerNow", "https://www.lookathernow.com", "https://site-api.project1service.com")
    searchSites[842] = ("Mylfwood", "Mylfwood", "https://www.mylf.com", "https://www.mylf.com/movies/")
    searchSites[843] = ("AllBlackX", "AllBlackX", "https://www.xempire.com", "https://www.xempire.com/en/search/allblackx/")
    searchSites[844] = ("BBCPie", "BBCPie", "https://bbcpie.com", "https://bbcpie.com/video/")
    searchSites[845] = ("Foster Tapes", "Foster Tapes", "https://www.fostertapes.com", "https://store.psmcdn.net/FOS-organic-n5oaginage")
    searchSites[846] = ("BFFs", "BFFs", "https://www.bffs.com", "https://store.psmcdn.net/BFFS-organic-7o68xoev0j")
    searchSites[847] = ("Shoplyfter", "Shoplyfter", "https://www.shoplyfter.com", "https://store.psmcdn.net/SHL-organic-driobt7t0f")
    searchSites[848] = ("ShoplyfterMylf", "ShoplyfterMylf", "https://www.shoplyftermylf.com", "https://store.psmcdn.net/MSL-organic-ws9h564all")
    searchSites[849] = ("Little Asians", "Little Asians", "https://www.littleasians.com", "https://store.psmcdn.net/LAS-organic-whlghevsfs")
    searchSites[850] = ("Thickumz", "Thickumz", "https://www.thickumz.com", "https://store.psmcdn.net/TMZ-organic-958spxinbs")
    searchSites[851] = ("Teens Love Black Cocks", "Teens Love Black Cocks", "https://www.teensloveblackcocks.com", "https://store.psmcdn.net/TLBC-organic-w8bw4yp9io")
    searchSites[852] = ("Bi Empire", "Bi Empire", "http://www.biempire.com", "https://site-api.project1service.com")
    searchSites[853] = ("Mylf x Joybear", "Mylf x Joybear", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[854] = ("Mylf x Teamskeet", "Mylf x Teamskeet", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[855] = ("Mylf x Hussie Pass", "Mylf x Hussie Pass", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[856] = ("Mylf Of The Month", "Mylf Of The Month", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[857] = ("Mylfselects", "Mylfselects", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[858] = ("Mylf x Lady Fyre", "Mylf x Lady Fyre", "https://mylf.com", "https://www.mylf.com/movies/")
    searchSites[859] = ("Deviant Hardcore", "Deviant Hardcore", "https://www.devianthardcore.com", "https://site-api.project1service.com")
    searchSites[860] = ("She Will Cheat", "She Will Cheat", "https://www.shewillcheat.com", "https://site-api.project1service.com")
    searchSites[861] = ("My XXX Pass", "My XXX Pass", "http://www.blowpass.com", "http://www.blowpass.com/en/search/blowpass/scene/")
    searchSites[862] = ("SinsLife", "SinsLife", "https://sinslife.com/", "https://sinslife.com/tour/search.php?query=")
    searchSites[863] = ("Wet and Pissy", "Wet and Pissy", "https://www.puffynetwork.com/", "https://www.puffynetwork.com/videos?search=")
    searchSites[864] = ("Pissing In Action", "Pissing In Action", "https://sinx.com", "https://www.sinx.com/videos/all?sexualOrientation=0&searchWord=")
    searchSites[865] = ("Golden Shower Power", "Golden Shower Power", "https://sinx.com", "https://www.sinx.com/videos/all?sexualOrientation=0&searchWord=")
    searchSites[866] = ("Fully Clothed Pissing", "Fully Clothed Pissing", "https://sinx.com", "https://www.sinx.com/videos/all?sexualOrientation=0&searchWord=")
    searchSites[867] = ("Simply Anal", "Simply Anal", "https://www.puffynetwork.com/", "https://www.puffynetwork.com/videos?search=")
    searchSites[868] = ("Wet and Puffy", "Wet and Puffy", "https://www.puffynetwork.com/", "https://www.puffynetwork.com/videos?search=")
    searchSites[869] = ("We Like To Suck", "We Like To Suck", "https://www.puffynetwork.com/", "https://www.puffynetwork.com/videos?search=")
    searchSites[870] = ("Euro Babe Facials", "Euro Babe Facials", "https://www.puffynetwork.com/", "https://www.puffynetwork.com/videos?search=")
    searchSites[871] = ("Slime Wave", "Slime Wave", "https://sinx.com", "https://www.sinx.com/videos/all?sexualOrientation=0&searchWord=")
    searchSites[872] = ("Kinky Spa", "Kinky Spa", "https://www.kinkyspa.com/", "https://site-api.project1service.com")
    searchSites[873] = ("SubmissiveX", "SubmissiveX", "http://www.kink.com", "http://www.kink.com/search?channelIds=submissivex&q=")
    searchSites[874] = ("Filthy Femdom", "Filthy Femdom", "http://www.kink.com", "http://www.kink.com/search?channelIds=filthyfemdom&q=")
    searchSites[875] = ("Anal Mom", "Anal Mom", "https://analmom.com", "https://store.psmcdn.net/organic-alm-Od3Iqu9I")
    searchSites[876] = ("Bellesa House", "Bellesa House", "https://www.bellesafilms.com/", "https://site-api.project1service.com")
    searchSites[877] = ("RealityLovers", "Reality Lovers", "https://realitylovers.com/", "https://realitylovers.com/videos/search")
    searchSites[878] = ("Adult Time", "Adult Time", "https://freetour.adulttime.com", "https://tsmkfa364q-dsn.algolia.net/1/indexes/*/queries")
    searchSites[879] = ("RealJamVR", "RealJamVR", "https://www.realjamvr.com", "https://realjamvr.com/virtualreality/scene/id/")
    searchSites[880] = ("BBC Paradise", "BBC Paradise", "https://www.bbcparadise.com/", "https://www.bbcparadise.com/movies/")
    searchSites[881] = ("Jesse Loads Monster Facials", "Jesse Loads Monster Facials", "https://jesseloadsmonsterfacials.com/", "https://jesseloadsmonsterfacials.com/visitors/tour_01.html")
    searchSites[882] = ("Assylum", "Assylum", "https://www.assylum.com/", "https://www.assylum.com/?home")
    searchSites[883] = ("Big Gulp Girls", "Big Gulp Girls", "https://tour.biggulpgirls.com/", "https://tour.biggulpgirls.com/videos/")
    searchSites[884] = ("Deepthroat Sirens", "Deepthroat Sirens", "https://tour.deepthroatsirens.com/", "https://tour.deepthroatsirens.com/videos/")
    searchSites[886] = ("Bathroom Creepers", "Bathroom Creepers", "https://www.bathroomcreepers.com/creeper/", "https://www.bathroomcreepers.com/creeper/categories/movies/1/latest/")
    searchSites[887] = ("Killergram", "Killergram", "http://www.killergram.com/home.asp?page=home", "http://www.killergram.com/episodes.asp?page=episodes&ct=all")
    searchSites[888] = ("Czech Casting", "Czech Casting", "https://czechcasting.com", "https://czechcasting.com/tour/search/?q=")
    searchSites[889] = ("Premium Bukkake", "Premium Bukkake", "free.premiumbukkake.com", "https://free.premiumbukkake.com/search/")
    searchSites[890] = ("Horny DreamBabez", "Horny DreamBabez", "https://hornydreambabez.com/", "https://hornydreambabez.com/")
    searchSites[891] = ("Shot Her First", "Shot Her First", "https://hushpass.com/t1/", "https://hushpass.com/t1/search.php?query=shot+her+first+")
    searchSites[892] = ("Push Her Limits", "Push Her Limits", "http://pushherlimits.com/", "http://pushherlimits.com/")
    searchSites[893] = ("Hookup Hotshot", "Hookup Hotshot", "https://hookuphotshot.com/", "https://hookuphotshot.com/the-dates/")
    searchSites[894] = ("Exploited College Girls", "Exploited College Girls", "https://exploitedcollegegirls.com/", "https://exploitedcollegegirls.com/free/updates.php")
    searchSites[895] = ("FTV Girls", "FTV Girls", "https://www.ftvgirls.com/", "https://www.ftvgirls.com/updates.html")
    searchSites[896] = ("FTV Milfs", "FTV Milfs", "https://www.ftvmilfs.com/", "https://www.ftvmilfs.com/updates.html")
    searchSites[897] = ("Jesh By Jesh", "Jesh By Jesh", "https://www.jeshbyjesh.com/", "https://www.jeshbyjesh.com/tour/categories/movies.html")
    searchSites[898] = ("18Eighteen", "18Eighteen", "https://www.18eighteen.com/", "https://www.18eighteen.com/")
    searchSites[899] = ("Facial Cum Targets", "Facial Cum Targets", "https://www.facialcumtargets.com/", "https://www.facialcumtargets.com/")
    searchSites[900] = ("True Anal", "True Anal", "https://www.trueanal.com/", "https://www.trueanal.com/search/")
    searchSites[901] = ("Bang Trickery", "Bang Trickery", "https://www.bang.com/original/4800/bang-trickery", "https://www.bang.com/search?term=trickery+")
    return searchSites

def getSearchSiteIDByFilter(searchFilter):
    searchSites = siteValues()
    searchSitesEnum = list(enumerate(searchSites))

    # Method #3
    searchResults = []
    searchFilterF = searchFilter.lower().replace(" ", "").replace(".com", "").replace("'", "").replace("-", "")
    for searchID, sites in searchSitesEnum:
        try:
            siteNameF = sites[0].lower().replace(" ", "").replace("'", "").replace("-", "")

            if searchFilterF.startswith(siteNameF):
                searchResults.append((searchID, siteNameF))
        except:
            pass

    if searchResults:
        from operator import itemgetter
        # Debug
        print('Site found with method #3: ',end='')
        return max(searchResults, key=itemgetter(1))[0]

    # Method #2
    # First attempt to fix the commented issue below. Startswith was not working for me but this method does have good results for my tests.
    searchFilterF = searchFilter.lower().replace(".com", "").replace("'", "").split(' ', 1)[0]
    for searchID, sites in searchSitesEnum:
        try:
            siteNameF = sites[0].lower().replace(" ", "").replace("'", "")

            if searchFilterF == siteNameF:
                # Debug
                print('Site found with method #2: ',end='')
                return searchID
        except:
            pass

    # Method #1
    # Might try converting this code to use startswith() to avoid problems with overlapping site names:
    # https://www.tutorialspoint.com/python/string_startswith.htm
    # Examples:
    #  Blacked -> BlackedRaw
    #  Babes -> FootsieBabes
    #  PassionHD Love Ties -> HD Love
    searchFilterF = (
        searchFilter.lower().replace(".com", "").replace("'", ""),
        searchFilter.lower().replace(".com", "").replace("'", "").replace(" ", "")
    )
    for searchID, sites in searchSitesEnum:
        try:
            siteNameF = sites[0].lower().replace(" ", "").replace("'", "")

            if siteNameF in searchFilterF[0] or siteNameF in searchFilterF[1]:
                # Debug
                print('Site found with method #1: ',end='')
                return searchID
        except:
            pass
    # Debug
    print(f'Search Filter: {searchFilterF}')
    return # was None


def getSearchSettings(mediaTitle: str):

    searchSites = siteValues()

    mediaTitle = mediaTitle.replace(".", " ")
    mediaTitle = mediaTitle.replace(" - ", " ")
    mediaTitle = mediaTitle.replace("-", " ")
    mediaTitle = re.sub(' +', ' ', mediaTitle)
    mediaTitle = mediaTitle.strip()

    # Search Site abbreviations
    # Using Regex instead of .replace or .startswith so it can be case insensitive

    abbreviations = (
        ('^18og ', '18OnlyGirls '),
        ('^18yo ', '18YearsOld '),
        ('^1kf ', '1000Facials '),
        ('^21ea ', '21EroticAnal '),
        ('^21fa ', '21FootArt '),
        ('^21n ', '21Naturals '),
        ('^2cst ', '2ChicksSameTime '),
        ('^a1o1 ', 'Asian1on1 '),
        ('^aa ', 'AmateurAllure '),
        ('^ad ', 'AmericanDaydreams '),
        ('^add ', 'ManualAddActors '),
        ('^agm ', 'AllGirlMassage '),
        ('^am ', 'AssMasterpiece '),
        ('^analb ', 'AnalBeauty '),
        ('^ap ', 'AssParade '),
        ('^av ', 'AvaSpice '),
        ('^baebz ', 'Baeb '),
        ('^bblib ', 'BigButtsLikeItBig '),
        ('^bcasting ', 'BangCasting '),
        ('^bcb ', 'BigCockBully '),
        ('^bcc ', 'Backroom Casting Couch'),
        ('^bch ', 'BigCockHero '),
        ('^bconfessions ', 'BangConfessions '),
        ('^bdpov ', 'BadDaddyPOV '),
        ('^bex ', 'BrazzersExxtra '),
        ('^bgb ', 'BabyGotBoobs '),
        ('^bgbs ', 'BoundGangbangs '),
        ('^bglamkore ', 'BangGlamkore '),
        ('^bgonzo ', 'BangGonzo '),
        ('^bin ', 'BigNaturals '),
        ('^bjf ', 'BlowjobFridays '),
        ('^bmf ', 'BigMouthfuls '),
        ('^bp ', 'ButtPlays '),
        ('^brealteens ', 'BangRealTeens '),
        ('^brf', 'BackRoomFacials '),
        ('^btas ', 'BigTitsatSchool '),
        ('^btaw ', 'BigTitsatWork '),
        ('^btc', 'BigTitCreampie '),
        ('^btis ', 'BigTitsinSports '),
        ('^btiu ', 'BigTitsinUniform '),
        ('^btlbd ', 'BigTitsLikeBigDicks '),
        ('^btra ', 'BigTitsRoundAsses '),
        ('^btrickery ', 'BangTrickery '),
        ('^burna ', 'BurningAngel '),
        ('^bwb ', 'BigWetButts '),
        ('^cagfs ', 'CrazyAsianGFs '),
        ('^cc ', 'CzechCasting'),
        ('^cfnm ', 'ClothedFemaleNudeMale '),
        ('^clip ', 'LegalPorno '),
        ('^cps ', 'CherryPimps '),
        ('^creepers ', 'BathroomCreepers '),
        ('^css ', 'CzechStreets '),
        ('^cuf ', 'CumFiesta '),
        ('^cws ', 'CzechWifeSwap '),
        ('^da ', 'DoctorAdventures '),
        ('^daughter ', 'DaughterSwap '),
        ('^daughters ', 'DaughterSwap '),
        ('^dbm ', 'DontBreakMe '),
        ('^dc ', 'DorcelVision '),
        ('^ddfb ', 'DDFBusty '),
        ('^dm ', 'DirtyMasseur '),
        ('^dnj ', 'DaneJones '),
        ('^dpg ', 'DigitalPlayground '),
        ('^dsw ', 'DaughterSwap '),
        ('^dwc ', 'DirtyWivesClub '),
        ('^dwp ', 'DayWithAPornstar '),
        ('^dontbreakme ', "DontBreakMe "),
        ('^ecg ', 'ExploitedCollegeGirls '),
        ('^esp ', 'EuroSexParties '),
        ('^ete ', 'EuroTeenErotica '),
        ('^etrasmall ', 'ExxxtraSmall '),
        ('^ext ', 'ExxxtraSmall '),
        ('^excogi ', 'ExploitedCollegeGirls '),
        ('^fams ', 'FamilyStrokes '),
        ('^faq ', 'FirstAnalQuest '),
        ('fct ', 'FacialCumTargets'),
        ('^fds ', 'FakeDrivingSchool '),
        ('^ff ', 'Facial Fest'),
        ('^fft ', 'FemaleFakeTaxi '),
        ('^fhd ', 'FantasyHD '),
        ('^fhl ', 'FakeHostel '),
        ('^fho ', 'FakehubOriginals '),
        ('^fittingroom ', 'Fitting-Room '),
        ('^fka ', 'FakeAgent '),
        ('^fm ', 'FuckingMachines '),
        ('^fms ', 'FantasyMassage '),
        ('^frs ', 'FitnessRooms '),
        ('^ft ', 'FastTimes '),
        ('^ftx ', 'FakeTaxi '),
        ('^gbcp ', 'GangbangCreampie '),
        ('^gft ', 'GrandpasFuckTeens '),
        ('^gta ', 'GirlsTryAnal '),
        ('^gw ', 'GirlsWay '),
        ('^h1o1 ', 'Housewife1on1 '),
        ('^ham ', 'HotAndMean '),
        ('^hart ', 'Hegre '),
        ('^hcm ', 'HotCrazyMess '),
        ('^hdb ', 'HornyDreamBabez '),
        ('^hegre-art ', 'Hegre '),
        ('^hoh ', 'HandsOnHardcore '),
        ('^hotab ', 'HouseofTaboo '),
        ('^ht ', 'Hogtied '),
        ('^hustl3r ', 'Hustler '),
        ('^ihw ', 'IHaveAWife '),
        ('^ihaw ', 'IHaveAWife '),
        ('^iktg ', 'IKnowThatGirl '),
        ('^il ', 'ImmoralLive '),
        ('^jbyj ', 'JeshByJesh '),
        ('^jp ', 'JaysPOV '),
        ('^jlmf ', 'JesseLoadsMonsterFacials '),
        ('^kha ', 'KarupsHA '),
        ('^kow ', 'KarupsOW '),
        ('^kpc ', 'KarupsPC '),
        ('^la ', 'LatinAdultery '),
        ('^latn ', 'LookAtHerNow '),
        ('^lcd ', 'LittleCaprice '),
        ('^lhf ', 'LoveHerFeet '),
        ('^littlecapricedreams ', 'LittleCaprice '),
        ('^lsb ', 'Lesbea '),
        ('^lst ', 'LatinaSexTapes '),
        ('^lta ', 'LetsTryAnal '),
        ('^maj ', 'ManoJob '),
        ('^mbb ', 'MommyBlowsBest '),
        ('^mbt ', 'MomsBangTeens '),
        ('^mc ', 'MassageCreep '),
        ('^mcu ', 'MonsterCurves '),
        ('^mda ', 'MyDirtyMaid'),
        ('^mdhf ', 'MyDaughtersHotFriend '),
        ('^mdhg ', 'MyDadsHotGirlfriend '),
        ('^mfa ', 'ManuelFerrara '),
        ('^mfhg ', 'MyFriendsHotGirl '),
        ('^mfhm ', 'MyFriendsHotMom '),
        ('^mfl ', 'Mofos '),
        ('^mfst ', 'MyFirstSexTeacher '),
        ('^mgbf ', 'MyGirlfriendsBustyFriend '),
        ('^mgb ', 'MommyGotBoobs '),
        ('^mic ', 'MomsInControl '),
        ('^mih ', 'MilfHunter '),
        ('^mj ', 'ManoJob '),
        ('^mlib ', 'MilfsLikeItBig '),
        ('^mlt ', 'MomsLickTeens '),
        ('^mmgs ', 'MommysGirl '),
        ('^mmts ', 'MomsTeachSex '),
        ('^mnm ', 'MyNaughtyMassage '),
        ('^mom ', 'MomXXX '),
        ('^mpov ', 'MisterPOV '),
        ('^mr ', 'MassageRooms '),
        ('^mrs ', 'MassageRooms '),
        ('^mshf ', 'MySistersHotFriend '),
        ('^mts ', 'MomsTeachSex '),
        ('^mvft ', 'MyVeryFirstTime '),
        ('^mwhf ', 'MyWifesHotFriend '),
        ('^naf ', 'NeighborAffair '),
        ('^nam ', 'NaughtyAmerica '),
        ('^na ', 'NaughtyAthletics '),
        ('^naughtyamericavr ', 'NaughtyAmerica '),
        ('^nb ', 'NaughtyBookworms '),
        ('^news ', 'NewSensations '),
        ('^nf ', 'NubileFilms '),
        ('^no ', 'NaughtyOffice '),
        ('^nrg ', 'NaughtyRichGirls '),
        ('^nubilef ', 'NubileFilms '),
        ('^num ', 'NuruMassage '),
        ('^nw ', 'NaughtyWeddings '),
        ('^obj ', 'OnlyBlowjob '),
        ('^otb ', 'OnlyTeenBlowjobs '),
        ('^passion-hd ', 'PassionHD '),
        ('^pav ', 'PixAndVideo '),
        ('^pba ', 'PublicAgent '),
        ('^pc ', 'PrincessCum '),
        ('^pdmcl ', 'ChicasLoca '),
        ('^pf ', 'PornFidelity '),
        ('^phd ', 'PassionHD '),
        ('^phdp ', 'PetiteHDPorn '),
        ('^plib ', 'PornstarsLikeitBig '),
        ('^pop ', 'PervsOnPatrol '),
        ('^ppu ', 'PublicPickups '),
        ('^prdi ', 'PrettyDirty '),
        ('^ps ', 'PropertySex '),
        ('^ptt ', 'Petite '),
        ('^pud ', 'PublicDisgrace '),
        ('^pup ', 'PublicPickups'),
        ('^reg ', 'RealExGirlfriends '),
        ('^rkp ', 'RKPrime '),
        ('^rws ', 'RealWifeStories '),
        ('^saf ', 'ShesAFreak '),
        ('^sart ', 'SexArt '),
        ('^sas ', 'SexandSubmission '),
        ('^sbj ', 'StreetBlowjobs '),
        ("^Shes New ", "She's New "),
        ('^sins ', 'SinsLife '),
        ('^sislove ', 'SisLovesMe '),
        ('^smb ', 'ShareMyBF '),
        ('^ssc ', 'StepSiblingsCaught '),
        ('^ssn ', 'ShesNew '),
        ('^sts ', 'StrandedTeens '),
        ('^swsn ', 'SwallowSalon '),
        ('^tdp ', 'TeensDoPorn '),
        ('^tds ', 'TheDickSuckers '),
        ('^ted ', 'Throated '),
        ('^tf ', 'TeenFidelity '),
        ('^tgs ', 'ThisGirlSucks '),
        ('^these ', 'TheStripperExperience '),
        ('^tla ', 'TeensLoveAnal '),
        ('^tlc ', 'TeensLoveCream '),
        ('^tle ', 'TheLifeErotic '),
        ('^tlhc ', 'TeensLoveHugeCocks '),
        ('^tlib ', 'TeensLikeItBig '),
        ('^tlm ', 'Teens Love Money '),
        ('^togc ', 'Tonights Girlfriend Classic '),
        ('^tog ', 'Tonights Girlfriend '),
        ('^tra ', 'True Anal'),
        ('^tspa ', 'Tricky Spa '),
        ('^tss ', 'That Sitcom Show '),
        ('^tuf ', 'The Upper Floor '),
        ('^wa ', 'Whipped Ass '),
        ('^wfbg ', 'We Fuck Black Girls '),
        ('^wkp ', 'Wicked '),
        ('^wlt ', 'We Live Together '),
        ('^woc ', 'Wild On Cam '),
        ('^wov ', 'Wives On Vacation '),
        ('^wowg ', 'Wow Girls '),
        ('^wy ', 'Web Young '),
        ('^zl ', 'Zoliboy'),
        ('^ztod ', 'Zero Tolerance '),
        ('^zzs ', 'ZZ series '),
    )
    abbFixed = False
    for abbreviation, full in abbreviations:
        r = re.compile(abbreviation, flags=re.IGNORECASE)
        mediatitle2 = ""
        mediatitle2 = mediaTitle.replace("_", " ")
        mediatitle2 = mediatitle2.replace("-", " ")
        mediatitle2 = mediatitle2.replace(".", " ")
        #print(mediatitle2)
        if r.match(mediatitle2):
            mediaTitle = r.sub(full, mediatitle2, 1)
            abbFixed = True
            #print(mediaTitle)
            break

    if abbFixed:
        # Debug
        print(f"\n(abbrev fixed) ")

    # Search Site ID
    searchSiteID = None
    # Date/Actor or Title
    searchType = None
    # What to search for
    searchTitle = None
    # Date search
    searchDate = None
    # Actors search
    searchActors = None
    fullsitename = ""
    # Remove Site from Title
    searchSiteID = getSearchSiteIDByFilter(mediaTitle)
    if searchSiteID:
        # Debug
        print(f"site ID: {searchSiteID} ({searchSites[searchSiteID][0]})")
        if searchSites[searchSiteID][0]:
            fullsitename = searchSites[searchSiteID][0]
        # searchSites [0] matches madiaTitle
        if mediaTitle[:len(searchSites[searchSiteID][0])].lower() == searchSites[searchSiteID][0].lower():
            searchTitle = mediaTitle[len(searchSites[searchSiteID][0]) + 1:]
        # searchSites [0] contains an ' but mediaTitle does not
        elif mediaTitle[:len(searchSites[searchSiteID][0].replace("'", ""))].lower() == \
                searchSites[searchSiteID][0].lower().replace("'", ""):
            searchTitle = mediaTitle[len(searchSites[searchSiteID][0]):]
        # searchSites [0] contains an ' and spaces but mediaTitle does not
        elif mediaTitle[:len(searchSites[searchSiteID][0].replace(" ", "").replace("'", ""))].lower() == \
                searchSites[searchSiteID][0].lower().replace(" ", "").replace("'", ""):
            searchTitle = mediaTitle[len(searchSites[searchSiteID][0].replace(" ", "").replace("'", "")) + 1:]
        # searchSites [0] and mediaTitle have the same punctuation but differnt spaces
        elif mediaTitle[:len(searchSites[searchSiteID][0].replace(" ", ""))].lower() == \
                searchSites[searchSiteID][0].lower().replace(" ", ""):
            searchTitle = mediaTitle[len(searchSites[searchSiteID][0].replace(" ", "")) + 1:]
        else:
            title = mediaTitle.replace('.com', '').title()
            site = searchSites[searchSiteID][0].lower()
            title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
            site = re.sub(r'\W', '', site)

            matched = False
            while ' ' in title:
                title = title.replace(' ', '', 1)
                if title.lower().startswith(site):
                    matched = True
                    break

            if matched:
                searchTitle = re.sub(site, '', title, 1, flags=re.IGNORECASE)
                searchTitle = ' '.join(searchTitle.split())
            else:
                searchTitle = mediaTitle
        if searchTitle[:4].lower() == "com ":
            searchTitle = searchTitle[4:]
    else:
        searchTitle = mediaTitle

    '''
    # Gamma Ent remove Scene number from BONUS and BTS
    if searchSiteID == 53 or searchSiteID == 183 or (searchSiteID >= 276 and searchSiteID <= 278) or \
            searchSiteID == 281 or (searchSiteID >= 285 and searchSiteID <= 287) or (searchSiteID >= 329 \
            and searchSiteID <= 332) or (searchSiteID >= 351 and searchSiteID <= 392) \
            or (searchSiteID >= 460 and searchSiteID <= 466) or searchSiteID == 692:
        if "Bonus" in searchTitle or "Bts" in searchTitle:
            alpha = searchTitle.find('Scene ', 0)
            omega = searchTitle.find('Scene ', 0) + 9
            sceneNumber = searchTitle[alpha:omega]
            searchTitle = searchTitle.replace(sceneNumber, "")
    '''

    #print("searchTitle (before date processing): " + searchTitle)


    # Search Type
    searchTitle = searchTitle.replace('#', '')
    searchDate = None
    regex = [
        (r'\b\d{4} \d{2} \d{2}\b', '%Y %m %d'),
        (r'\b\d{2} \d{2} \d{2}\b', '%y %m %d'),
        (r'\b\d{2} \d{2} \d{4}\b', '%d %m %Y'),
        (r'\b\d{2} \d{2} \d{2}\b', '%d %m %y'),
        (r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}.*?\s\d{2}|\d{4}', '%b %d %Y'),
        (
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2}.*?\s\\d{2}|\d{4}',
        '%b %d %Y'),
        (
        r'\d{2}[.*?][\s?](January|February|March|April|May|June|July|August|September|October|November|December)[\s?][.*?]\s\d{2}|\d{4}',
        '%b %d %Y'),
        (r'(\d+)[/\.-](\d+)[/\.-](\d+)', '%y %m %d'),
    ]
    date_obj = None
    for r, dateFormat in regex:
        #print(r + " - " + dateFormat)
        date = re.search(r, searchTitle)
        if date:
            try:
                date_obj = datetime.strptime(date.group(), dateFormat)
                #print("Date found")

            except:
                pass

            if date_obj:
                searchDate = date_obj.strftime('%Y-%m-%d')
                searchTitle = ' '.join(re.sub(r, '', searchTitle, 1).split())
                break

    return searchSiteID, fullsitename, searchTitle, searchDate