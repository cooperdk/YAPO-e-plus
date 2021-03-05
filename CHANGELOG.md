# Changelog

(WIN) = Windows exclusive, (LIN) = Linux exclusive

## (0.7.6.55)

### Changes

* Another command argument is introduced (works in both compiled and Python version).
It is now possible to disable both the automatic browser opening (command argument: no-browser) as well as automatic 
  migration (command argument: no-migration). This makes YAPO boot faster, but it will error out if a migration is 
  actually needed.

## 210304 (0.7.6.51)

 *This update requires migrations. This happens automatically.*

**Note: this small update will not be compiled, unless requested.**

### New

* The YAPO Tags API is now in use. Currently, I have only had time to plug it into single tag views, but it works for both actor tags and scene tags and saves backdrop images and thumbnails to disk as well as descriptions to the database together with aliases (hopefully, not tested yet).

## 210227 (0.7.6.5)

  *This update may require a [requirements upgrade](https://pip.pypa.io/en/stable/reference/pip_install/#examples)
  as well as various changes as described below.*

### Changes

* The media directory has been moved away from the videos/ directory, as it is modified by the user, it really had no place within the codebase.
  Moving the directory can be done manually, but I advise you to let YAPO do it (by simply starting it). The yapo.py script will catch your old directory, move it, and make sure your configuration reflects the change. The stored data was prepared for this move, so no data loss will occur.
* There are no more hardcoded constants. In essence, all paths and modifiable settings are controlled with the configuration file (config/settings.yml) and default values for those not set in that file.
* Working directories like /config and /database are now generated on first startup.
* The scene details view generated a 404 error for each video preview picture. This has been fixed (AngularJS template).


## 210217 (0.7.6.4)

  *This update requires a [requirements upgrade](https://pip.pypa.io/en/stable/reference/pip_install/#examples)*

### Changes

* YAPO now has a naughty waitress! I switched the webserver part from the built-in Django development server to the Waitress WSGI server, and it's (a lot) faster.
  It is started in a slightly different way. I have changed the startup so generally you will now start YAPO by executing:
  `python yapo.py`
  The old manage.py (which is used to enter the emergency shell, etc) is still available in the Github build. The frozen build will have a companion app instead.
* On startup, YAPO now checks if there is a database present, and one is generated if not.
* I am beginning to adapt the UI and view backends to display various results in the UI alert field on top of the page. For now, it works with the database cleanup utility and the duplicate scanner, among others.

## 210215 (0.7.6.3)

### Changes

* The duplicate checker no longer recurses the entire dataset. I found a way to filter duplicates and designed it so that the first copy is the original, and any subsequent copies are marked as duplicates. Instead of taking about two minutes for a 11,000 scene database, it now completes in less than one tenth of a second (not counting the file deletion and database removal).
  A warning about duplicates is now displayed in the startup-sequence (Hail Amiga!) if there are any.
  Also, I have implemented a further check so the duplicate checker only deletes files with identical hashes as well as identical filesizes.



## 210212 (0.7.6.2)

### Changes

* Once again, Freeones has changed their site structure and the actor scraper did not work.
  It has now been converted to make use of XPATH instead of pure BeautifulSoup parsing, making it much easier to update.
* Whenever a scraper has no record of an actor, the error code will now be 404 Not Found and not 501 not Implemented. 
* FPS will always be an integer. Videos with a framerate of 29.97 will now be registered as 30 fps.


## 210209 (0.7.6.1)

### Changes

* An error had occured in the settings template which made it impossible to alter the URL and port that YAPO listens to.
* Miscellaneous refactoring
* Now requires at least Django 3.1

## 210208 (0.7.6)

### Changes

* More sites recognized by the title parser

### New

* Bangbros sites will now be identified if they have the original Bangbros filenames.
  
  TpDB does not support the Bangbros release IDs so I had to create a script to parse it and send a request to the Bangbros site. If the scene title (filename) is a Bangbros release ID, the title the TpDB scanner uses will change causing TpDB to be able to find the scene information.
   

* Beginning code to enable backup creation/restoration from the web UI

## 210205 (0.7.5.1)

_Requires migration as the database structure has changed! Check the README under "installation and upgrade instructions", section 4._

### Changes

* The TpDB scanner now stores the original video URL of scenes. Requires a re-scan.

* The TpDB scanner no longer uses tags to keep track of scanned scenes and scan validity. It will however convert the tags to fields in the database during a rescan, or using the tool below.

### New

* YAPO now has a few management commands (just like "migrate" and "makemigrations"). They were necessary in order to allow users to scan TpDB (The Porn Database).
  - The first tool (get-clean-titles) will get clean scene titles from TpDB, which are needed for the scene filename renamer (may consume some time).
  - The second tool (mark-scenes) will update scenes with TpDB registrations by setting a field in the database to True.
  - The third tool (convert-tags) will convert the old YAPO TpDB tags (TpDB: Scanned: True, TpDB, Match: Good, etc) by setting fields in the database (this is time consuming).

  You can start YAPO's Django management CLI by typing "python manage.py" (or yapo-eplus.exe for the compiled version) followed by any of the commands above, or "help <command>" for more information about the individual commands.
## 210203 (0.7.5)

_Requires migration as the database structure has changed! Check the README under "installation and upgrade instructions", section 4._
 
_May also require you to enter settings and "save" the renaming format under "file renaming"._
### Changes

* The TpDB automatic re-titler now saves the clean, original title of a scene. This will be used soon.
Also, the TpDB re-titler uses the same basic code as the renamer and re-titles based on your specification. What the TpDB module does NOT do is rename your file (an option will be added later)

### New

* YAPO now includes a file renamer. Currently only accessible from the scene detail page (scene view) and only renames one scene.
  The renamer will rename your scene files based on your format (in settings). If a specific format is entered for a single website (in the website view), the particular website renaming format will be used.
  If a scene belongs to more than one website (which is possible), the first will be selected.
* Release date is now displayed on the scene detail page. Not yet editable so only dates pulled from TpDB are displayed.

## 210202 (0.7.4)

### Changes

* (WIN) The video contact sheet generator was unable to run if ffmpeg/ffprobe weren't placed in a path where the system looked for it. This is fixed. (#57)
* (WIN) The "Open folder" button in the scene detail will now open the file explorer but also select the file. (#54)
* Added more substrings for the title parser's filename cleaner
* More adjustments to the scene title parser and YAPO detects more abbreviated websites

### New

* Video contact sheets in the scene list and grid view. The icon is placed on the scene thumbnail (#52)

## 200910 (0.7.3u1)

### Changes

* YAPO has a new logo, and the version is displayed on the navigation bar in the web app
* Changes to the TpDB scanner as their API changed
* (WIN) Added a feature to auto-download FFMPEG so the user doesn't have to find a full installation
* Changes in the versioning system. YAPO will now always notify when a new version is available

### New

* Panic button. Press "ESC" while the browser is focused to quickly open weather.com in a new tab.

## 200820 (0.7.3)

## Changes

* More websites supported by the title parser
* Opened up an option to donate (on the right hand side on the Github page)


## 200810 (0.7.1)

### New

* YAPO now "plugs into" The Porn DB and requests scene information if configured for this.
* Autonomous registration of websites when found in TpDB
* Ability to automatically re-title scenes so that they don't appear as their filename
* Actors now scraped from four sources (in this order): IMDB, TMDB, TpDB and Freeones. Any information not already present will be added.

## 200628-0205 (0.6.12)

### Changes

* Smaller updates: Freeones scraper, all javascript dependencies now included with new locations

## 200628-0205 (0.6.12)

### New

* YAPO will now stream videos with the embedded HTML5 player. WMV, AVI and FLV files must still be played using the VLC button, and you can only generate previews for files that cannot be played internally. 
* On startup, YAPO will report the amount of available memory, cores, and your CPU's speed. If these are sufficient, YAPO will (later) allow for transcoding of the above mentioned files.
* YAPO now runs on Django 3.0.7 (latest release), and only supports Python 3.7 or newer.
  The Docker image (check README.md) is now working, but requires you to mount your video folders within the virtual environment.

## 200605-0035

### New

* Now creating video contact sheets of all videos. In the next update, this sheet will be displayed by clicking the appropriate button in the scene detail view. They are located in each scene's folder under "video/media/scenes".
* Layout change. YAPO is now in dark mode, Bootstrap is updated and I have made a nicer layout. Be aware that some dropdown boxes are hard to make out, this will be changed soon.
* Now prepared for more focused actor photo searching. In a soon-to-come update, YAPO will download two additional profile shots and three action shots (that is, two portrait mode photos and three landscape photos).

REQUIRES A PIP INSTALL OF NEW REQUIREMENTS:

From the YAPO main dir, execute:
`pip install --r requirements.txt`


## 200525-0210

### New

* Reworked the database to handle various exclusions. You can now enter any words that shouldn't trigger a website or actor tag, a website or it's aliases.
For example, the word "floral" in the filename would trigger a tag named "oral" - by excluding "floral" you can prevent this).
Another example is the fact that there is a website named "Stepsiblings Caught" and another one just named "Stepsiblings". By adding "Stepsiblings" in the exclusion list for "Stepsiblings Caught", the system will not incorrectly register the website "Stepsiblings" for a file that should only be registered to "Stepsiblings Caught".


THIS REQUIRES A DATABASE MIGRATION BEFORE RUNNING YAPO.

In a command shell from the YAPO main directory, run these two commands:


`python manage.py makemigrations`

`python manage.py migrate`


Then run YAPO.


`python manage.py runserver ip:port (ex. 127.0.0.1:8000)`


Check README.md for more information, if needed.


* Update notification
* Website logos will be displayed in the website view, if the logo exists in videos/media/logos. Thanks to GernBlanston for sharing them.
* Disk space report and number of actors will be reported on launch. Also, a file named actors.txt will be exported at launch for backup and sharing purposes.
* New actor field: piercings.
* Automatic tags: Bra cups, breast size groups (fx large or huge), height groups, piercings.
* New scraper: IMDB, TMDB
* Video hashing. YAPO e+ generates a 256-bit hash for each scene and there is a function under Settings to remove duplicate scenes.

### Changes

* Supporting the new Freeones layout.
* Updated the Python version requirement and dependencies.
* Tattoos now displayed correctly.

## 0.2.0 

A report of changes will be added at a later date.

## 0.1.3 (2016-09-09)

### New

* Folders added to Yapo in the 'add' menu are now logged and can be rescanned for new files in the 'settings' menu. This is not retroactive so folders added before this update will not be present in the settings menu. They will if one was to re-add them. [Curt Wagner]
* Added option to bulk add comma separated websites and scene tags in the add page. [Curt Wagner]

### Changes

* New experimental layout for Scene Detail page. [Shaun Clayton]

## 0.1.2 (2016-09-07)

### New

* Added 'playlist' category. Scenes can now be added to custom lists, multiple scenes can be added in one go. Also same scene can be in multiple lists. Random play works with playlists. In addition to help keep track of randomly played scenes [Issue #43] every time the random play button is used, the played scene is added to an auto generated playlist called 'random plays'. [Curt Wagner]

### Changes

* Added missing confirmation to delete scene(s) from disk function. [Shaun Clayton]
* Delete scenes from disk function now has secondary reminder confirmation for added prevention of accidental file deletion.

### Fix

* [Issue #31] Fixed bug where incorrect input params were fed to the removeItem function in scene-list.component.js. [Curt Wagner]

## 0.1.1 (2016-09-05)

### New

* Added play_count logging for scene_tags, actors and website upon playing a scene. Also added order by play count options for them. [Curt Wagner]

### Changes

* Deprecated CHANGELOG.rst in favour of CHANGELOG.md. [Shaun Clayton]

## 0.1.0 (2016-09-04)

### New

* Updated CHANGELOG.rst. [Shaun Clayton]
* Added stub for CHANGELOG.rst. [Shaun Clayton]

### Older

* Hopefully fixed the problem that prevent `makemigrations` from executing. [Curt Wagner]
* [Issue #42] Added &#x27;usage_count&#x27; to actor\scene tags website and actors. Also added option to sort by usage count. [Curt Wagner]
* [Issue #43] Added &#x27;play_count&#x27; and &#x27;date_last_played&#x27; sorting options to scenes that will help track down scenes recently watched. Also added play count as a search option. [Curt Wagner]
* [Issue #30] Added &#x27;scene_tags&#x27; to &#x27;website&#x27; also added &#x27;scene_tags&#x27; to &#x27;actor_tags&#x27;. Now whenever a website/actor added to scenes their tags are added as well. (When they are removed the tags are removed). EX: Adding &#x27;Stoya&#x27; who is tagged with &#x27;eye.color.green&#x27; will tag the scene with &#x27;eye.color.green&#x27;. and removing &#x27;Stoya&#x27; will remove &#x27;eye.color.green&#x27; tag. [Curt Wagner]
* Corrected formatting of scraper popup message. [Shaun Clayton]
* Added missing tooltip for scene tag aliases input - Added code to strip leading/trailing spaces from scene/website aliases. [Shaun Clayton]
* [Issue #30] Added &#x27;aliases&#x27; to scenes tags and websites. Also added &#x27;date modified&#x27; to almost all models. This will require migrating. [Curt Wagner]
* [Issue #11] Made it so &#x27;order by&#x27; option is retained for actors,scenes,websites,tags and folders. Also added &#x27;Random&#x27; option in folder view Also added &quot;Date_added&quot; field to folders. Will require to makemigrations and migrate. [Curt Wagner]
* Made it so scenes that can&#x27;t be ffprobed won&#x27;t be added. [Curt Wagner]
* Added conversion for weight and height to Imperial #20. [Shaun Clayton]
* Partially Implemented -- &quot;[Feature Request] Add confirmation for removing/deleting items from database or disk #31&quot; [Shaun Clayton]
* Fixed issue with timezone offset affecting birth date display. [Shaun Clayton]
* Added change to correct timezone offset changing the birthday being displayed on Actor detail page.
* Partially implemented &#x27;&#x27;[Feature Request] Add button to play random scene #27&#x27;. Play random scene works with scene, actors, websites and scenetags but only when the search term is blank. [Curt Wagner]
* Fixed issue &#x27;[Bug] Not all Actors displayed after Items Per Page set #28&#x27; [Curt Wagner]
* Clean db now also deletes folders in /media/ of actors\scenes that are no longer in the database. [Curt Wagner]
* Updated favicons images. [Shaun Clayton]
* New style and bolder icon
* Added MKV to accepted extensions. [Curt Wagner]
* Corrected spelling and formatting. [Shaun Clayton]
* Changed how grid view works, it now should keep current query results. Also in actor detail view, when switching to grid view will automatically hide actor info. [Curt Wagner]
* Made DOB of actors to work. [Curt Wagner]
* Creating sample when adding scenes should work now (Really) [Curt Wagner]
* Added favicon images. [Shaun Clayton]
* Added option to delete actor\scene tags and websites from database. [Curt Wagner]
* Removed unnecessary buttons from the upload profile image interface. Added functuanality to crop existing images. [Curt Wagner]
* Added OS detection to ffmpeg_process.py. [Shaun Clayton]
* Added detection of which platform we are running under so that the paths can be adjusted accordingly.
* Fixed formatting - removed redundant double label for Height and Weight. [Shaun Clayton]
* Strip trailing and leading spaces from Actors inserted into database. [Shaun Clayton]
* Fixes the potential issue of leaving a space after a comma when importing a bulk list of Actors, was causing scraping errors as it was scraping the Actor name with the spaces included.
* Added clean database option in settings (Now also removes aliases without actors) [Curt Wagner]
* Added option to delete scenes from disk. [Curt Wagner]
* Added option to remove scene from database. [Curt Wagner]
* Made grid option persistent using ngStorage. [Curt Wagner]
* Added rating and runner up toggle to actor list. [Curt Wagner]
* Added more search options and filters. [Curt Wagner]
* Freeones scraper will now search for alias if it failed to find the main name. [Curt Wagner]
* Added rating bar to scene list view, also added settings.json versioning and &#x27;last lookup&#x27; field for all scenes in settings.json. [Curt Wagner]
* Added toggleable recursion option to folder view. Now it&#x27;s possible to view scenes that are inside of the current folder only or view scenes inside the current folder and all of it's subfolders. [Curt Wagner]
* Made scenes in Actor, Scene Tags, and websites searchable, also added applicable order options to each one of them. [Curt Wagner]
* Added &#x27;Runner Up&#x27;, and &#x27;Play Scene&#x27; to scene list options. [Curt Wagner]
* Made actor name editable. [Curt Wagner]
* Added (x years old) to actor details if date of birth exists. [Curt Wagner]
* Added &#x27;Google Image Search&#x27; to actor details. [Curt Wagner]
* Added &quot;is_exempt_from_one_word_search&quot; to actor details. [Curt Wagner]
* Added unknown person image. [Curt Wagner]

