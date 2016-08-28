# YAPO
YAPO - Yet Another Porn Organizer

Greetings fellow pervs!

#####  TL;DR 
YAPO is a software I made to organize and manage porn collections.
It's not finished yet, but if you want to try it anyway, in the bottom of the post there are videos that will have you running YAPO in less than 15 minutes. There are screenshots and a demo video in the bottom of the post as well.

#### Demo\Tutorial of YAPO usage:
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/1LjWD2L8cjI/0.jpg)](https://www.youtube.com/watch?v=1LjWD2L8cjI)

#####  Background 
About a year ago an EMP user named ''julesx'' created an app called Pornganizer. 
It's basically a cataloging software fine tuned to cataloging porn. It has actors, tags, websites etc. I thought it was a wonderful idea, because in my mind, the first and **most limiting factor** in any collection is the extent to which the collector is aware of it.

*For example:*
Let's say you may have a collection of 300 clips but you don't really remember or aware of what each one contains. So let's say you want to watch a clip with a redhead, your collection may have 50 clips with redheads in them, but you are limited only to the clips that you **remember** having redheads in them which *is a fraction* of that number. So effectively you don't have a collection of 300 clips, you only have a collection of the clips you are aware of, unless you actively go though your clips each time you want to watch something **OR** if you use a cataloging software like Pornganizer.

If you do use a cataloging software, you can just tag all the 'redhead' clips with the appropriate tag and whenever you want to watch a redhead clip, you just click that tag and you have **all** of the clips that contain redheads, immediately.

Of Course the benefits of a cataloging and tagging don't end there, you can have multiple tags on multiple actors and multiple categories so your queries could become extremely specific like: 
"redheads who have green eyes and were born after 1990 and are higher than 160 cm".

Another benefit of such a software is that it stores all the entries in a database and not in a folder structure.
Imagine you have 2 folders, one for Stoya and one for James Deen. It's entirely possible that there are scenes in the Stoya folder that have James Deen in them but are missing from the James Deen folder, so when you go to the James Deen folder, you miss out on all those scenes.
In a cataloging software on the other hand, when you search for Stoya, you get all the scenes that are tagged with her name, across all folder and drives.

There are more benefits to cataloging, but I think you can get the picture. 

So I started to use Pornganizer and it was great, but I had a few issues with it. The most pressing one for me as a software student was that its code was closed for some reason. So every time I had and idea of how to improve it, instead of downloading the code and making modifications I had to try and convince the developer to add those changes. Another thing is that Pornganizer is for Windows only. 

So I decided that I'll make my own Pornganizer, with Blackjack and hookers.

# What is YAPO?

Basically YAPO is a product of me wanting to learn Python and me wanting to create a cataloging software similar to Pornganizer. Two birds one stone I thought.
Ironically enough as of writing this post YAPO can't do any of the things I wanted [code]julesx[/code] to put in Pornganizer, **YET**. 

I chose to implement the whole thing as a web app that runs on a local server.
My vision was it being a kind of a _Netflix thing_.
So I used Python's Django as the server and Angular JS as the client.

I hope some people who know Python, HTML, Angular or CSS or will find it interesting enough to add some code of their own to this. I'm really crap at CSS and styling that is why YAPO's interface leaves a lot to be desired. But the good thing is that the interface is just CSS and HTML and anyone with even the most rudimentary CSS\HTML knowledge can add something, and make it better.


### What can YAPO do as of now?
[*]It can import scenes to it's database and create screenshots for them. (Later I want to make an option to create a screenshot contact sheet like we have here on EMP for each torrent. And for the user to be able to open the video at the specific time when he clicks on the contact sheet.)

* It can optionally create a sample video for the imported scenes, a sample is about 10mb in size and is between 30 and 90 seconds long. For now the length and the number of segments of the sample videos are extrapolated from the source duration, but eventually the user will be able to make their own sample videos.

* It can tag actors, websites and tags for the scenes, and for actors.

* It can navigate folders (The folders that were added to the database)

* It can scrape actor information from TMDb and freeones.com

* And other things I don't remember or can't articulate...

### What are the limitations of YAPO?
Due to the limitation of web-apps it's currently impossible to play the videos inside the browser window.(Though it will be possible in the future using ffmpeg to transcode the video, exactly in the way [Emby Media Center](https://emby.media/)  does it.)Right now YAPO can only show the sample videos inside the browser window and relies on an external player(VLC) to play the full scenes.(Just like Pornganizer)

##### What YAPO's potential in the future?
* Well because it's a local server, it can do neat things. For instance it can be accessed from your phone over the local network. Actually not only phones, anything with a browser. Though my main goal right now is not making YAPO mobile friendly but because the client side is built with AngularJS and HTML bootstrap it kind of mobile friendly already.

* Again, because it's a server client thing, in the future it will be possible to cast video streams to other devices. It can even be possible over the internet on not only on local network. Kind of your own personal Pornhub.

* Though the reliance on VLC is a drawback for now, it's possible to do pretty nifty things with the VLC player, for example it's possible to create a video wall, programmatically opening up 4 VLC players simultaneously.

* I want to add support for image sets.


# Screenshots:

Scene Detail view:

![alt text](https://jerking.empornium.ph/images/2016/08/10/2016-08-10_13-57-00.md.jpg)

Actor List view (All the metadata you see here like height, nationality and so on is tagged automatically from TMDb and freeones *without* manual input

![alt text](https://jerking.empornium.ph/images/2016/08/10/2016-08-10_13-57-46.md.jpg)

Actor Detail view, example of adding an actor tag(All the red fields are editable and can be changed by the user):

![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_13-59-36.md.jpg)
![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_13-59-41.md.jpg)
![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_14-00-13.md.jpg)


Folder view:

![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_14-09-44.md.jpg)


Currently YAPO is under heavy development and as far as I see it, it's not nowhere near being ready for end user distribution mainly because the slightly tedious installation process.
In the end I want it to be 1 portable .exe for Windows and whatever executable Linux and Mac OS use.
But for now if you want to try it there are a few hoops you need to jump through, namely install the dependencies and download the code from GitHub.
It's not as hard as it seems and it takes less than 15 minutes to set everything up though I understand if people find it intimidating.

# Installation: 
I made a few videos that describe exactly what you need to do if you want to try YAPO out:

#### YAPO's dependencies:

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/shH4gFhgi58/0.jpg)](https://www.youtube.com/watch?v=shH4gFhgi58)

YAPO's dependencies are: 
* [Python 3](https://www.python.org/)
* [FFMPEG](https://ffmpeg.org/)
* [NodeJS](https://nodejs.org/en/)
* [Bower](https://bower.io/#install-bower)

####  YAPO installation:

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/uaeavs9v_gg/0.jpg)](https://www.youtube.com/watch?v=uaeavs9v_gg)

1. Create a virtual environment for YAPO's installation.
2. With the virtual environment activated create a folder for YAPO and pull it from Git EX: `c:\yapo\YAPO\> git clone https://github.com/curtwagner1984/YAPO.git`
3. Install YAPO dependencies `pip install -r requirements.txt`
4. Navigate to yapo/videos/static/bower and install JS dependencies by running `bower install`
5. Create YAPO database (from /YAPO ) `python manage.py migrate`
6. (On Windows) Place ffmpeg.exe and ffprobe.exe in /yapo/videos/ffmpeg folders
7. Start the server `python manage.py runserver 127.0.0.1:8000`



PS: A few words about Non-Windows OS. 
YAPO is made using Python and Javascript, both are OS agnostic. 
That being said, I only tested it on Windows and even though it **should** work on Linux and Mac I think minor changes to the code needs to be made for it work just as well as on Windows. Specifically changes to functions using VLC and FFMPEG.
I would be happy if people running Mac or Linux will test it out and report back.


#### Update instructions:
YAPO is a WIP and as such the code will change often, to sync with the latest changes on Git this is what you have to do:

`(py3virtualenv) c:\yapo\YAPO\>git pull` This will pull the latest updates for YAPO from the Git repository.

`(py3virtualenv) c:\yapo\YAPO\>python manage.py makemigrations`
This will look over the new code and take note of the adjustments that needs to be made to the database.

`(py3virtualenv) c:\yapo\YAPO\>python manage.py migrate`
This will actually make the adjustments to the database it took note of in the previous step

(In this case py3virtualenv is the name of **your** virtual environment and c:\yapo\YAPO is **your** YAPO install dir )
