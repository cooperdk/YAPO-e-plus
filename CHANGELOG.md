# Changelog

## 20200525-0210

### New

* Reworked the database to handle various exclusions. You can now enter any words that shouldn't trigger a website or actor tag, a website or it's aliases.
For example, the word "floral" in the filename would trigger a tag named "oral" - by excluding "floral" you can prevent this).
Another example is the fact that there is a website named "Stepsiblings Caught" and another one just named "Stepsiblings". By adding "Stepsiblings" in the exclusion list for "Stepsiblings Caught", the system will not incorrectly register the website "Stepsiblings" for a file that should only be registered to "Stepsiblings Caught".

** THIS REQUIRES A DATABASE MIGRATION BEFORE RUNNING YAPO.

In a command shell from the YAPO main directory, run these two commands:

python manage.py makemigrations
python manage.py migrate

Then run YAPO.
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

