# Changelog


## 0.1.1 (2016-09-05)

### New

* Added play_count logging for scene_tags, actors and website upon playing a scene. Also added order by play count options for them. [Curt Wagner]

### Changes

* Deprecated CHANGELOG.rst in favour of CHANGELOG.md. [Shaun Clayton]


## 0.1.0 (2016-09-04)

### New

* Updated CHANGELOG.rst. [Shaun Clayton]

* Added stub for CHANGELOG.rst. [Shaun Clayton]

### Other

* Hopefully fixed the problem that prevent `makemigrations` from executing. [Curt Wagner]

* [Issue #42] Added &#x27;usage_count&#x27; to actor\scene tags website and actors. Also added option to sort by usage count. [Curt Wagner]

* [Issue #43] Added &#x27;play_count&#x27; and &#x27;date_last_played&#x27; sorting options to scenes that will help track down scenes recently watched. Also added play count as a search option. [Curt Wagner]

* [Issue #30] Added &#x27;scene_tags&#x27; to &#x27;website&#x27; also added &#x27;scene_tags&#x27; to &#x27;actor_tags&#x27;. Now whenever a websitector added to scenes their tags are added as well. (When they are removed the tags are removed). EX: Adding &#x27;Stoya&#x27; who is tagged with &#x27;eye.color.green&#x27; will tag the scene with &#x27;eye.color.green&#x27;. and removing &#x27;Stoya&#x27; will remove &#x27;eye.color.green&#x27; tag. [Curt Wagner]

* Corrected formatting / grammar. [Shaun Clayton]

* Corrected grammatical error. [Shaun Clayton]

* - Corrected formatting of scraper popup message. [Shaun Clayton]

* - Added missing tooltip for scene tag aliases input - Added code to strip leading/trailing spaces from scene/website aliases. [Shaun Clayton]

* [Issue #30] Added &#x27;aliases&#x27; to scenes tags and websites. Also added &#x27;date modified&#x27; to almost all models. This will require migrating. [Curt Wagner]

* Fixed JS warning / error from improperly terminated quote. [Shaun Clayton]

* Fixed typos. [sjclayton]

* Fixed typos. [sjclayton]

* Update README.md. [curtwagner1984]

* Fixed issue with weight being converted incorrectly after earlier changes. [sjclayton]

  Was:

  &#x27;&#x27;&#x27;html
  &lt;td class=&quot;alright&quot;&gt;
                      &lt;span ng-if=&quot;$ctrl.actor != undefined &amp;&amp; $ctrl.actor.weight != undefined&quot;&gt;
                              ({{ $ctrl.weightConvertPounds($ctrl.actor.height)}} pounds)
                      &lt;/span&gt;
                  &lt;/td&gt;
  &#x27;&#x27;&#x27;
  instead of:

  ```html
  &lt;td class=&quot;alright&quot;&gt;
                      &lt;span ng-if=&quot;$ctrl.actor != undefined &amp;&amp; $ctrl.actor.weight != undefined&quot;&gt;
                              ({{ $ctrl.weightConvertPounds($ctrl.actor.weight)}} pounds)
                      &lt;/span&gt;
                  &lt;/td&gt;
  ```

  Works now!

* [Issue #11] Made it so &#x27;order by&#x27; option is retained for actors,scenes,websites,tags and folders. Also added &#x27;Random&#x27; option in folder view Also added &quot;Date_added&quot; field to folders. Will require to makemigrations and migrate. [Curt Wagner]

* [Issue #11] Made it so &#x27;order by&#x27; option is retained for actors,scenes,websites,tags and folders. Also added &#x27;Random&#x27; option in folder view. [Curt Wagner]

* Made it so scenes that can&#x27;t be ffprobed won&#x27;t be added. [Curt Wagner]

* Removed &#x27;missing ethnicity&#x27; from section-wrapper. [Curt Wagner]

* Minor adjustments to inch conversion function from issue #20, also some adjustments that will hopefully help create a single executable file. [Curt Wagner]

* Added conversion for weight and height to Imperial #20. [sjclayton]

* Added conversion for weight and height to Imperial. [sjclayton]

  - Add conversion display for Weight and Height to imperial measurement #20

* Partially Implemented -- &quot;[Feature Request] Add confirmation for removing/deleting items from database or disk #31&quot; [sjclayton]

* Partially Implemented -- &quot;[Feature Request] Add confirmation for removing/deleting items from database or disk #31&quot; [sjclayton]

  - Right now only works when removing a scene from the database.

* Revised README.md. [sjclayton]

* Revised README.md. [sjclayton]

* Revised README.md. [sjclayton]

* Revised README.md. [sjclayton]

  - Revised to make it read more like a product page (description) and less like a forum post.... we aren&#x27;t on EMP. =P
  - Corrected various spelling, formatting and grammatical errors.
  - Fixed screenshot links so they are more visible and when clicked on they show full screen (instead of quarter size).

* Update styles.css. [sjclayton]

* Update styles.css. [sjclayton]

  - Centered actor profile picture on Actor Detail view.

* Update tmdb_search.py. [sjclayton]

* Update actor-detail.template.html. [sjclayton]

* Fixed issue with timezone offset affecting birth date display. [sjclayton]

  - Added change to correct timezone offset changing the birthday being displayed on Actor detail page.

* Corrected spelling / formatting and grammar (will continue to cleanup later) [sjclayton]

* Update add-items.template.html. [sjclayton]

  - Corrected formatting
  - Improved consistency of strings

* Update settings.template.html. [sjclayton]

  - Improve consistency of strings
  - Corrected popover for clean database

* Update tmdb_search.py. [sjclayton]

  - Improve consistency of strings

* Update views.py. [sjclayton]

  - Corrected formatting
  - Improve consistency of strings

* Update actor-detail.template.html. [sjclayton]

  Improve consistency of strings

* Update actor-detail.template.html. [sjclayton]

  Corrected formatting and grammar

* Corrected formatting. [sjclayton]

* Update filename_parser.py. [sjclayton]

  Corrected formatting / grammar

* Partially implemented &#x27;&#x27;[Feature Request] Add button to play random scene #27&#x27;. Play random scene works with scene, actors, websites and scenetags but only when the search term is blank. [Curt Wagner]

* Fixed issue &#x27;[Bug] Not all Actors displayed after Items Per Page set #28&#x27; [Curt Wagner]

* Clean db now also deletes folders in /media/ of actors\scenes that are no longer in the database. [Curt Wagner]

* Modified formatting for branding. [sjclayton]

* Modified formatting for branding. [sjclayton]

* Updated favicons reference - broad scope support. [sjclayton]

* Updated favicons reference - broad scope support. [sjclayton]

* Added more favicon compatibility images and code. [sjclayton]

  - Broad scope icon and favicon support

* Updated favicons reference. [sjclayton]

* Updated favicons images. [sjclayton]

  - New style and bolder icon

* Corrected formatting. [sjclayton]

* Corrected formatting. [sjclayton]

* Corrected formatting. [sjclayton]

* Corrected formatting. [sjclayton]

* Added MKV to accepted extensions. [Curt Wagner]

* Corrected formatting. [sjclayton]

* Corrected formatting. [sjclayton]

* Corrected formatting. [sjclayton]

* Corrected formatting. [sjclayton]

* Corrected spelled and formatting. [sjclayton]

* Update settings.template.html. [sjclayton]

  Modified items per page options, removed 1000 - as it would be way to process intensive and take way to long to load. Added a couple of extra choices (25 and 250)

* Changed how grid view works, it now should keep current query results. Also in actor detail view, when switching to grid view will automatically hide actor info. [Curt Wagner]

* Made DOB of actors to work. [Curt Wagner]

* Added favicons reference to head. [sjclayton]

* Delete favicon.png. [sjclayton]

* Added favicon and a placeholder icon from google. [Curt Wagner]

* Creating sample when adding scenes should work now (Really) [Curt Wagner]

* Added favicon images. [sjclayton]

* Creating sample when adding scenes should work now. [Curt Wagner]

* Update ffmpeg_process.py. [sjclayton]

* Update ffmpeg_process.py. [sjclayton]

* Added option to delete actor\scene tags and websites from database. [Curt Wagner]

* Temporarily disabled changes to caching parameters. [sjclayton]

  Needs further testing!  As it is causing slow page loads while not actually providing the desired results.

* Removed unnecessary buttons from the upload profile image interface. Added functuanality to crop existing images. [Curt Wagner]

* Update ffmpeg_process.py. [sjclayton]

* Update ffmpeg_process.py. [sjclayton]

* Added OS detection to ffmpeg_process.py. [sjclayton]

  Added detection of which platform we are running under so that the paths can be adjusted accordingly.

* Fixed formatting - removed redundant double label for Height and Weight. [sjclayton]

* Create LICENSE.txt. [curtwagner1984]

* Create README.md. [curtwagner1984]

* Fixed typo in actor detail. [Curt Wagner]

* Strip trailing and leading spaces from Actors inserted into database. [sjclayton]

  Fixes the potential issue of leaving a space after a comma when importing a bulk list of Actors, was causing scraping errors as it was scraping the Actor name with the spaces included.

* Merge pull request #1 from sjclayton/sjclayton (#1) [sjclayton]

* Added multi_platform open file function to use in &#x27;open_folder&#x27; view. Added printing out of error messages in ffmpeg_process and tmdb_search. Added meta tags to index-head in hopes of preventing broweser caching. [Curt Wagner]

* Update views.py. [sjclayton]

  Fixed spelling error

* Update settings.template.html. [sjclayton]

  Corrected formatting and grammatical issues

* Update actor-detail.template.html. [sjclayton]

  Corrected spelling and formatting errors

* Update tmdb_search.py. [sjclayton]

  Corrected hardcoded MEDIA_PATH variable

* Added clean database option in settings (Now also removes aliases without actors) [Curt Wagner]

* Added clean database option in settings. [Curt Wagner]

* Added option to delete scenes from disk. [Curt Wagner]

* Added option to remove scene from database. [Curt Wagner]

* Hopefuly made it more friendly to linux, and fixed scenes no showing bug resulting from grid view. [Curt Wagner]

* Made grid option persistent using ngStorage. [Curt Wagner]

* Removed winsound from the project. Also added experimental grid view, and an option to hide info on actor detail page. [Curt Wagner]

* Added rating and runner up toggle to actor list. [Curt Wagner]

* Added more search options and filters. [Curt Wagner]

* Changed actor profile image dir names from actor names to actor id EX: instead media/actor/isis love/profile/profile.jpg it will be media/actor/17/profile/profile.jpg. [Curt Wagner]

  Also moved startup function from settings.py to urls.py and made it so that the folder names would change automatically on startup if they need to.

* Freeones scraper will now search for alias if it failed to find the main name. [Curt Wagner]

* Added rating bar to scene list view, also added settings.json versioning and &#x27;last lookup&#x27; field for all scenes in settings.json. [Curt Wagner]

* Added recursion option to folder view. Now it&#x27;s possible to view scenes that are inside of the current subfolders. [Curt Wagner]

* Actor Detail view looks slightly better. [Curt Wagner]

* Made it possible to search and order scenes in actor,website and scene tags views. [Curt Wagner]

* Scene list multiple tagging now works, fixed issue where pagination won&#x27;t show in actor detail view. [Curt Wagner]

* Added &#x27;Runner Up&#x27;, and &#x27;Play Scene&#x27; to scene list options. [Curt Wagner]

* Added &#x27;Runner Up&#x27;, and &#x27;Play Scene&#x27; to scene list options. [Curt Wagner]

* Minor bug fix in addScenes. [Curt Wagner]

* Fixed some of the title issues... [Curt Wagner]

* Made actor name editable. [Curt Wagner]

* Added (x years old) to actor details if date of birth exists.  Moved loading of Actors,alisas,websits and tags out of the fileparser function so it won&#x27;t load them each iteration. [Curt Wagner]

* Fixed dir creation path when actor image is uploaded. [Curt Wagner]

* Minor update to search term. [Curt Wagner]

* Added &#x27;google image search&#x27; to actor details. [Curt Wagner]

* Changed upload url from &quot;127.0.0.1:8000/upload&quot; to &quot;/upload/&quot; [Curt Wagner]

* Added &quot;is_exempt_from_one_word_search&quot; to actor details. [Curt Wagner]

* Made folder view work with id paths  EX:&quot;#!/folder/105&quot; instead of calculating path internally. Also removed threading from &#x27;add_scenes&#x27; function in addItems view. [Curt Wagner]

* Added unkown person image. [Curt Wagner]

* Initial commit. [Curt Wagner]

