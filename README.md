# YAPO e+
## Yet Another Porn Organizer (extended plus)

#### *The YAPO website is coming soon!*

*If you don't want to mess with Python and all the dependencies, there is an installer (Windows 10 64-bit) located here: https://github.com/cooperdk/YAPO-e-plus/releases. It may not include newer commits, please check the changelog and you can manually update the YAPO code after installation.*

##### This is a branch of the original YAPO on which I'm making improvements, such as in-browser playback, file matching and more scraping options. Find the original readme at the bottom (delimited with a line of "=" signs).

There is a setup available for an easy install. On the releases page, there is a "Getting Started" guide which also includes setup instructions.

There's also a Docker image which is described further down.

A copy of the setup with pre-registered actors, websites and tags (thousands of them) is available. It will be available on Patreon shortly. Until then, contact me here to gain access to it.

ATTENTION - The program directory should be renamed to "YAPO" (upper case) as some functions depend on this! 

There is a **set of logos** available for websites, thanks to @GernBlanston#0168 from Porn Organizing (https://discord.gg/6TvpGA) - get them here: https://gitea.unknown.name/Trizkat/site-logos - they should be unpacked to your YAPO root. YAPO simply matches the website name in your installation with a PNG image in videos/media/logos and if there's a name match, the logo will be shown on the website view. Currently, the filename MUST match the  website name (not case-sensitive). This means that you should rename the logos to whatever you call your websites, or vice versa. I will be working on an automatic website addition tool in the future.

Requirements: FFMPEG, VLC (for out-of-browser playback, if you prefer that) and Python 3.7+ installed. If you use the installer, everything is pre-installed for you.

If something is not working, it is generally enough to make sure all dependencies are installed. Please consult step 3 and 4 under "Installation and upgrade instructions"  below.

##### Discuss and share on Discord: https://discord.gg/zdm7Mdg

---------------

#### NEW FEATURES:

- Streaming scene playback from within YAPO e+ (with working seek bar).
- Working dockerfile
- Contact sheets.
  These are generated in each scene's folder under videos/media/scenes. They can be displayed by clicking the appropriate button on the scene detail view.
- Layout change.
  An update to Bootstrap and a new, darker design for YAPO. Bootstrap 4 will be implemented later.
- Ready for focused actor photo searching (Google), feature to be added later.
- Exclusions now available for scene tags, actor tags and websites.
  You can now enter any words that shouldn't trigger a website or actor tag, a website or it's aliases.
  For example, the word "floral" in the filename would trigger a tag named "oral" - by excluding "floral" you can prevent this).
  Another example is the fact that there is a website named "Stepsiblings Caught" and another one just named "Stepsiblings".
  By adding "Stepsiblings" in the exclusion list for "Stepsiblings Caught", the system will not incorrectly register the website "Stepsiblings" for a file that should only be registered to "Stepsiblings Caught".


- Now supports the new Freeones site layout. The scraper now shows a progress bar for each actor scrape.

- As mentioned, we now offer website/producer logos in the website view, if the logo exists in videos/media/logos. Thanks to GernBlanston for sharing them.

- New Python module requirements, it may be necessary to upgrade your modules.

- On startup, the total disk usage for the video collection and other information is reported. Also, the database is backed up and your actor collection is exported to a text file in the main YAPO dir.

- YAPO e+ will now strip the measurements field for a bra cup size, tag the actor with the cup size, and also tag with a breast size grouping (fx large or huge).

- YAPO e+ will also tag an actor based on height. Actors of normal height (161-178 cm) won't be tagged.

- Tatto information shows up in the actor details, and a group tag for tattoo amounts is added.

- A field has been added to register information about piercings. In addition, typical types of piercings are sent to the actor tags.

- YAPO e+ scrapes actor information from IMDB first (best biographies), then from TMDB (next best profiles and best profile pictures) and then from Freeones (best all-round information). If there's a photo in the system and it's taken from TMDB or added by the user, the system no longer downloads a new one, even if you force scrape to update the actor.
  This also ensures that your manually added photos won't be overwritten. A button will be added later, so you can delete the profile photo.

- YAPO e+ hashes all scenes (don't worry, it's FAST!) and adds the hash checksum to the scenes table.
  When requested in settings, it will perform a dupe check after confirmation, and delete all duplicates so only one copy remains.

- A lot of uninteresting console log text has been silenced.

#### COMING NEXT:

- Soon: Automated importing of Trizkat's actor photo library
- More scrapers
- Experimental scene scraping

#### PLANNED:

- Photo gallery section
- DVD section
- Additional actor photos (up to 5)
- Function to move all videos belonging to a website or actor so that they reside in the same folder and an ability to set this automatically
- An API for videohashes, tags and actors to avoid hundreds of people re-inventing the wheel

#### Installation and upgrade instructions

##### Local install

1. **Get a copy of YAPO onto your computer**. Either by downloading the zip, by getting the [docker image](https://hub.docker.com/repository/docker/cooperdk/yapo-eplus/general), or by [cloning from git](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository). The docker image will require some work to setup, since every video folder must be mounted in the image.

1. **Clone the git branch of your choice** - master or develop. Do this by doing:

    `git branch -b <master or develop>`

    `git clone -b https://github.com/cooperdk/YAPO-e-plus.git <install dir>`

    The install dir should be <drive>\YAPO (Windows) or \YAPO (Linux).

    You can also just download the branch of your choice by selecting that branch on the Github page, and pressing the green "Clone" button and then clicking "Download zip".

    * **Linux specific:**

      Install FFMPEG using your package manager, or compile it. It should be as complete as possible, with H.264/H.265, AAC, MP3 etc.
      Personally, I use [this package]() (Ubuntu). After following the directions on the page, just do apt-get install ffmpeg and you have a copy with all the libraries you're ever going to need.

    * **Windows specific:**

      Download [FFMPEG](https://ffmpeg.zeranoe.com/builds/) and move ffmpeg.exe, ffplay.exe and ffprobe.exe in the archive's `bin/` folder to the subfolder `videos/ffmpeg` in the YAPO e+ root folder. On Windows, YAPO looks for them there and only there. This binary includes everything needed by YAPO. I advise you to update it regularly, Zeranoe builds new versions all the time.

1. **Install all Python dependencies by executing:**

    `pip install -R requirements.txt`
    from the main YAPO e+ folder. This installs Django and any other libraries in their minimum required versions.

1. **Since the YAPO e+ models occasionally change, it may be necessary to migrate**.

    1. Prepare database migration:
        ```bash
        python manage.py makemigrations
        ```

        This will look over the new code and create scripts to make the adjustments to the database.

    1. Execute the database migration scripts:
        ```bash
        python manage.py migrate
        ```
        
        This will actually make the adjustments to the database it took note of in the previous step.

    1. If you get this error when you're done:
        ```bash
        You are trying to add a non-nullable field **'date_added'** to folder without a default; we can't do that (the database needs  something to populate existing rows).
        ```
       
        When asked to select a fix, select option 1 and type in `datetime.datetime.now()` and press enter.
       
        If you need more help installing the software, first look towards the end of this document, there's a section named "Installation".
        Only if you really have difficulties, register an issue on Github. I will offer installation help, by mail or through Teamviewer, for a coffee donation.
        
        If you get errors other that those in part 3 above, try to do
        
        `python manage.py migrate --fake`
        
        (or replace fake with fake-initial if you don't have a db.sqlite3 database file in your main YAPO e+ folder)
        
        You can also secure your database with the command:
        
        `python manage.py dumpdata --indent=4 > database.json`
        
        Which will export your database tables to json format. You can then import it after executing step 1 and 2 above to generate a new database with the command:
        
        `python manage.py loaddata database.json --ignorenonexistent`
        
        If you have any issues with this, I will fix your database for a small donation. There are sometimes problems due to Django's way of updating databases. Typically, it is due to primary keys in built-in tables.

**Running YAPO in a Docker environment**

- To do this, you will need a working [Docker installation](https://www.docker.com/get-started) (on Windows, only Docker Desktop is supported, since I had no luck in connecting to my Docker Toolbox environment).

  Get the release by doing:

  `docker pull cooperdk/yapo-eplus`

  And run it with:

  `docker run -i -t -p 8000 cooperdk/yapo-eplus`

  The -i argument is needed if YAPO needs to ask you a question, and the -t argument makes sure that you have TTY abilities for your session. The Docker image is hardcoded to serve on port 8000, which is why it has to be opened with the -p argument.

  The database should be setup the first time you run the environment, and you can use the Docker CLI to mount your video folders as Samba shares. On Windows, this requires you to create network shares for each of your main video folders that you want YAPO to access. I don't suggest that you copy the files over to the Docker image.

  Docker Desktop requires the May 2020 update of Windows 10 Home (build 2004), or any version of Windows 10 Professional. You cannot install Docker Desktop on an older release of Windows 10 Home.
  
  The docker image is built on a Debian system. Please read up on the above if you're not sure what I mean. If you need support for this, I offer my help for a donation.

8. **Enjoy**!

For visual help setting up your YAPO system, I am preparing guides and tips. You can find a "getting started" guide on the [releases page](https://github.com/cooperdk/YAPO-e-plus/releases).

This concludes this document. Below you'll find the document created by the author of YAPO redux, which was forked from the original YAPO.

------

# YAPO
YAPO - Yet Another Porn Organizer

Greetings fellow pervs!

YAPO is a software I made to organize and manage porn collections.
It's not finished yet, but if you want to try it anyway, at the bottom of the page there are videos that will have you running YAPO in less than 15 minutes. There are also screenshots at the bottom of the page as well.

#### Demo/Tutorial video of YAPO usage:
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/1LjWD2L8cjI/0.jpg)](https://www.youtube.com/watch?v=1LjWD2L8cjI)

#####  Background 
About a year ago an EMP (Empornium) user named ''julesx'' created an app called Pornganizer. 
It's basically a cataloging software fine tuned for cataloging porn. It has actors, tags, websites etc. I thought it was a wonderful idea, because in my mind, the first and **most limiting factor** in any collection is the extent to which the collector is aware of it.

*For example:*
Let's say you may have a collection of 300 clips but you don't really remember or are not aware of what each one contains. So let's say you want to watch a clip with a redhead, your collection may have 50 clips with redheads in them, but you are limited only to the clips that you **remember** having redheads in them which *is a fraction* of that number. So effectively you don't have a collection of 300 clips, you only have a collection of the clips you are aware of, unless you actively go though your clips each time you want to watch something **OR** if you use a cataloging software like Pornganizer.

If you do use a cataloging software, you can just tag all the 'redhead' clips with the appropriate tag and whenever you want to watch a redhead clip, you just click that tag and you have **all** of the clips that contain redheads, immediately.

Of course the benefits of cataloging and tagging don't end there, you can have multiple tags on multiple actors and multiple categories so your queries could become extremely specific like: 
"redheads who have green eyes and were born after 1990 and are taller than 160 cm".

Another benefit of such a software is that it stores all the entries in a database and not in a folder structure.
Imagine that you have 2 folders, one for Stoya and one for James Deen. It's entirely possible that there are scenes in the Stoya folder that have both Stoya and James Deen in them but are missing from the James Deen folder, so when you go to the James Deen folder, you miss out on all those scenes.
In a cataloging software on the other hand, when you search for Stoya, you get all the scenes that are tagged with her name, across all folders and drives.

There are more benefits to cataloging, but I think you can get the picture. 

So I started to use Pornganizer and it was great, but I had a few issues with it. The most pressing one for me as a software student was that its code was closed source for some reason. So every time I had an idea of how to improve it, instead of downloading the code and making modifications I had to try and convince the developer to add those changes. Another thing, is that Pornganizer is for Windows only. 

So I decided that I'll make my own Pornganizer, with Blackjack and hookers.

# What is YAPO?

Basically YAPO is a product of me wanting to learn Python and wanting to create a cataloging software similar to Pornganizer. Two birds, one stone... I thought.
Ironically enough, as of writing this YAPO can't do any of the things I wanted ''julesx'' to put in Pornganizer, **YET**. 

I chose to implement the whole thing as a web app that runs on a local server.
My vision was it being a kind of a _Netflix thing_.
So I used Python's Django as the server and AngularJS as the client.

I hope some people who know Python, HTML, AngularJS and CSS will find it interesting enough to add some code of their own to this. I'm really crap at CSS and styling that is why YAPO's interface leaves a lot to be desired. But the good thing is that the interface is just CSS and HTML and anyone with even the most rudimentary CSS/HTML knowledge can add something, and make it better.


### What can YAPO do as of now?
* It can import scenes to it's database and create screenshots for them (later I want to make an option to create a screenshot contact sheet like we have on EMP (Empornium) for each torrent, and for the user to be able to open the video at the specific time where he/she clicks on the contact sheet).

* It can optionally create a sample video for the imported scenes, a sample is about 10MB in size and is between 30 and 90 seconds long. For now the length and the number of segments of the sample videos are extrapolated from the source duration, but eventually the user will be able to make their own sample videos.

* It can tag actors, websites and tags for the scenes, and for actors.

* It can navigate folders (the folders that were added to the database)

* It can scrape actor information from TMDb and freeones.com

* And other things I don't remember or can't articulate...

### What are the limitations of YAPO?
Due to the limitation of web-apps it's currently impossible to play the videos inside the browser window (though it will be possible in the future using ffmpeg to transcode the video, exactly in the way [Emby Media Center](https://emby.media/)  does it). Right now YAPO can only show the sample videos inside the browser window and relies on an external player (VLC) to play the full scenes, (just like Pornganizer).

##### What is YAPO's potential in the future?
* Well, because it's a local server, it can do neat things. For instance it can be accessed from your phone over the local network. Actually not only phones, anything with a browser. Though my main goal right now is not making YAPO mobile-friendly, but because the client side is built with AngularJS and HTML bootstrap it's kind of mobile-friendly already.

* Again, because it's a client-server thing, in the future it will be possible to cast video streams to other devices. It can even be possible over the Internet, not only on the local network. Kind of like your own personal Pornhub.

* Though the reliance on VLC is a drawback for now, it's possible to do pretty nifty things with the VLC player, for example it's possible to create a video wall, programmatically opening up 4 VLC players simultaneously.

* I want to also add support for image sets.


# Screenshots:

Scene Detail view:

![alt text](https://jerking.empornium.ph/images/2016/08/10/2016-08-10_13-57-00.jpg)

Actor List view (all the meta-data you see here like height, nationality and so on is tagged automatically from TMDb and Freeones *without* manual input): 

![alt text](https://jerking.empornium.ph/images/2016/08/10/2016-08-10_13-57-46.jpg)

Actor Detail view (an example of adding an actor tag, all the red fields are editable and can be changed by the user):

![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_13-59-36.jpg)
![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_13-59-41.jpg)
![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_14-00-13.jpg)


Folder view:

![alt text](https://jerking.empornium.ph/images/2016/08/10/chrome_2016-08-10_14-09-44.jpg)


Currently YAPO is under heavy development and as far as I see it, it's not anywhere near being ready for end user distribution mainly because of the slightly tedious installation process.
In the end I want it to be 1 portable .EXE for Windows and whatever executable Linux and Mac OS use.
But for now if you want to try it, there are a few hoops you need to jump through, namely install the dependencies and download the code from GitHub.
It's not as hard as it seems and it takes less than 15 minutes to set everything up, though I understand if people find it intimidating.

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

(Watch the video above for a walkthrough of the installation.)

1. Create a virtual environment for YAPO's installation.
1. With the virtual environment activated, create a folder for YAPO and pull it from Git: `C:\YAPO\> git clone https://github.com/cooperdk/YAPO-e-plus.git`
1. Install YAPO dependencies: `pip install -r requirements.txt`
1. Install [Node.js & npm](https://nodejs.org/en/download/) and use it to install bower: `npm install -g bower`
1. Navigate to `C:\YAPO\videos\static\bower` and install JS dependencies by running: `bower install`
1. Create YAPO database from `C:\yapo\YAPO` run: `python manage.py migrate`
1. Prepare ffmpeg
    1. (On Windows) Place ffmpeg.exe and ffprobe.exe in the `C:\YAPO\videos\ffmpeg folder`
    1. (On Debian-based Linux distros) Install ffmpeg using package manager: `sudo apt update && sudo apt install ffmpeg`
1. Start the server from `C:\YAPO` run: `python manage.py runserver 127.0.0.1:8000`



PS: A few words about non-Windows OSes. 
YAPO is made using Python and JavaScript, both are OS agnostic. 
That being said, I only tested it on Windows and even though it **should** work on Linux and Mac, I think minor changes to the code needs to be made for it work just as well as on Windows. Specifically changes to functions using VLC and FFMPEG.
I would be very happy if people running Linux or Mac would test it out and report back.


#### Update instructions:
YAPO is a WIP (work in progress) and as such the code will change often, to sync with the latest changes on Git this is what you have to do:

`(py3virtualenv) C:\YAPO\> git pull` This will pull the latest updates for YAPO from the Git repository.

`(py3virtualenv) C:\YAPO\> python manage.py makemigrations`
This will look over the new code and take note of the adjustments that needs to be made to the database.

`(py3virtualenv) C:\YAPO\> python manage.py migrate`
This will actually make the adjustments to the database it took note of in the previous step.

(In this case py3virtualenv is the name of **your** virtual environment and C:\YAPO is **your** YAPO install dir )

#### Notes:

When updating YAPO, if you get the following error: 

```
> You are trying to add a non-nullable field **'date_added'** to folder without a default; we can't do that (the database needs  something to populate existing rows).

> Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
 Select an option:
```

You should select option 1 and type in `datetime.datetime.now()` and press enter.



****
