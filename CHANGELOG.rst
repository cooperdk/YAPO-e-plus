Changelog
=========

0.1.0 (2016-09-04)
------------------

New
~~~

- Updated CHANGELOG.rst. [Shaun Clayton]

- Added stub for CHANGELOG.rst. [Shaun Clayton]

Other
~~~~~

- Hopefully fixed the problem that prevent `makemigrations` from
  executing. [Curt Wagner]

- [Issue #42] Added 'usage_count' to actor\scene tags website and
  actors. Also added option to sort by usage count. [Curt Wagner]

- [Issue #43] Added 'play_count' and 'date_last_played' sorting options
  to scenes that will help track down scenes recently watched. Also
  added play count as a search option. [Curt Wagner]

- [Issue #30] Added 'scene_tags' to 'website' also added 'scene_tags' to
  'actor_tags'. Now whenever a website\actor added to scenes their tags
  are added as well. (When they are removed the tags are removed). EX:
  Adding 'Stoya' who is tagged with 'eye.color.green' will tag the scene
  with 'eye.color.green'. and removing 'Stoya' will remove
  'eye.color.green' tag. [Curt Wagner]

- Corrected formatting / grammar. [Shaun Clayton]

- Corrected grammatical error. [Shaun Clayton]

- - Corrected formatting of scraper popup message. [Shaun Clayton]

- - Added missing tooltip for scene tag aliases input - Added code to
  strip leading/trailing spaces from scene/website aliases. [Shaun
  Clayton]

- [Issue #30] Added 'aliases' to scenes tags and websites. Also added
  'date modified' to almost all models. This will require migrating.
  [Curt Wagner]

- Fixed JS warning / error from improperly terminated quote. [Shaun
  Clayton]

- Fixed typos. [sjclayton]

- Fixed typos. [sjclayton]

- Update README.md. [curtwagner1984]

- Fixed issue with weight being converted incorrectly after earlier
  changes. [sjclayton]

  Was:

  '''html
  <td class="alright">
                      <span ng-if="$ctrl.actor != undefined && $ctrl.actor.weight != undefined">
                              ({{ $ctrl.weightConvertPounds($ctrl.actor.height)}} pounds)
                      </span>
                  </td>
  '''
  instead of:

  ```html
  <td class="alright">
                      <span ng-if="$ctrl.actor != undefined && $ctrl.actor.weight != undefined">
                              ({{ $ctrl.weightConvertPounds($ctrl.actor.weight)}} pounds)
                      </span>
                  </td>
  ```

  Works now!

- [Issue #11] Made it so 'order by' option is retained for
  actors,scenes,websites,tags and folders. Also added 'Random' option in
  folder view Also added "Date_added" field to folders. Will require to
  makemigrations and migrate. [Curt Wagner]

- [Issue #11] Made it so 'order by' option is retained for
  actors,scenes,websites,tags and folders. Also added 'Random' option in
  folder view. [Curt Wagner]

- Made it so scenes that can't be ffprobed won't be added. [Curt Wagner]

- Removed 'missing ethnicity' from section-wrapper. [Curt Wagner]

- Minor adjustments to inch conversion function from issue #20, also
  some adjustments that will hopefully help create a single executable
  file. [Curt Wagner]

- Added conversion for weight and height to Imperial #20. [sjclayton]

- Added conversion for weight and height to Imperial. [sjclayton]

  - Add conversion display for Weight and Height to imperial measurement #20

- Partially Implemented -- "[Feature Request] Add confirmation for
  removing/deleting items from database or disk #31" [sjclayton]

- Partially Implemented -- "[Feature Request] Add confirmation for
  removing/deleting items from database or disk #31" [sjclayton]

  - Right now only works when removing a scene from the database.

- Revised README.md. [sjclayton]

- Revised README.md. [sjclayton]

- Revised README.md. [sjclayton]

- Revised README.md. [sjclayton]

  - Revised to make it read more like a product page (description) and less like a forum post.... we aren't on EMP. =P
  - Corrected various spelling, formatting and grammatical errors.
  - Fixed screenshot links so they are more visible and when clicked on they show full screen (instead of quarter size).

- Update styles.css. [sjclayton]

- Update styles.css. [sjclayton]

  - Centered actor profile picture on Actor Detail view.

- Update tmdb_search.py. [sjclayton]

- Update actor-detail.template.html. [sjclayton]

- Fixed issue with timezone offset affecting birth date display.
  [sjclayton]

  - Added change to correct timezone offset changing the birthday being displayed on Actor detail page.

- Corrected spelling / formatting and grammar (will continue to cleanup
  later) [sjclayton]

- Update add-items.template.html. [sjclayton]

  - Corrected formatting
  - Improved consistency of strings

- Update settings.template.html. [sjclayton]

  - Improve consistency of strings
  - Corrected popover for clean database

- Update tmdb_search.py. [sjclayton]

  - Improve consistency of strings

- Update views.py. [sjclayton]

  - Corrected formatting
  - Improve consistency of strings

- Update actor-detail.template.html. [sjclayton]

  Improve consistency of strings

- Update actor-detail.template.html. [sjclayton]

  Corrected formatting and grammar

- Corrected formatting. [sjclayton]

- Update filename_parser.py. [sjclayton]

  Corrected formatting / grammar

- Partially implemented ''[Feature Request] Add button to play random
  scene #27'. Play random scene works with scene, actors, websites and
  scenetags but only when the search term is blank. [Curt Wagner]

- Fixed issue '[Bug] Not all Actors displayed after Items Per Page set
  #28' [Curt Wagner]

- Clean db now also deletes folders in /media/ of actors\scenes that are
  no longer in the database. [Curt Wagner]

- Modified formatting for branding. [sjclayton]

- Modified formatting for branding. [sjclayton]

- Updated favicons reference - broad scope support. [sjclayton]

- Updated favicons reference - broad scope support. [sjclayton]

- Added more favicon compatibility images and code. [sjclayton]

  - Broad scope icon and favicon support

- Updated favicons reference. [sjclayton]

- Updated favicons images. [sjclayton]

  - New style and bolder icon

- Corrected formatting. [sjclayton]

- Corrected formatting. [sjclayton]

- Corrected formatting. [sjclayton]

- Corrected formatting. [sjclayton]

- Added MKV to accepted extensions. [Curt Wagner]

- Corrected formatting. [sjclayton]

- Corrected formatting. [sjclayton]

- Corrected formatting. [sjclayton]

- Corrected formatting. [sjclayton]

- Corrected spelled and formatting. [sjclayton]

- Update settings.template.html. [sjclayton]

  Modified items per page options, removed 1000 - as it would be way to process intensive and take way to long to load. Added a couple of extra choices (25 and 250)

- Changed how grid view works, it now should keep current query results.
  Also in actor detail view, when switching to grid view will
  automatically hide actor info. [Curt Wagner]

- Made DOB of actors to work. [Curt Wagner]

- Added favicons reference to head. [sjclayton]

- Delete favicon.png. [sjclayton]

- Added favicon and a placeholder icon from google. [Curt Wagner]

- Creating sample when adding scenes should work now (Really) [Curt
  Wagner]

- Added favicon images. [sjclayton]

- Creating sample when adding scenes should work now. [Curt Wagner]

- Update ffmpeg_process.py. [sjclayton]

- Update ffmpeg_process.py. [sjclayton]

- Added option to delete actor\scene tags and websites from database.
  [Curt Wagner]

- Temporarily disabled changes to caching parameters. [sjclayton]

  Needs further testing!  As it is causing slow page loads while not actually providing the desired results.

- Removed unnecessary buttons from the upload profile image interface.
  Added functuanality to crop existing images. [Curt Wagner]

- Update ffmpeg_process.py. [sjclayton]

- Update ffmpeg_process.py. [sjclayton]

- Added OS detection to ffmpeg_process.py. [sjclayton]

  Added detection of which platform we are running under so that the paths can be adjusted accordingly.

- Fixed formatting - removed redundant double label for Height and
  Weight. [sjclayton]

- Create LICENSE.txt. [curtwagner1984]

- Create README.md. [curtwagner1984]

- Fixed typo in actor detail. [Curt Wagner]

- Strip trailing and leading spaces from Actors inserted into database.
  [sjclayton]

  Fixes the potential issue of leaving a space after a comma when importing a bulk list of Actors, was causing scraping errors as it was scraping the Actor name with the spaces included.

- Merge pull request #1 from sjclayton/sjclayton (#1) [sjclayton]

- Added multi_platform open file function to use in 'open_folder' view.
  Added printing out of error messages in ffmpeg_process and
  tmdb_search. Added meta tags to index-head in hopes of preventing
  broweser caching. [Curt Wagner]

- Update views.py. [sjclayton]

  Fixed spelling error

- Update settings.template.html. [sjclayton]

  Corrected formatting and grammatical issues

- Update actor-detail.template.html. [sjclayton]

  Corrected spelling and formatting errors

- Update tmdb_search.py. [sjclayton]

  Corrected hardcoded MEDIA_PATH variable

- Added clean database option in settings (Now also removes aliases
  without actors) [Curt Wagner]

- Added clean database option in settings. [Curt Wagner]

- Added option to delete scenes from disk. [Curt Wagner]

- Added option to remove scene from database. [Curt Wagner]

- Hopefuly made it more friendly to linux, and fixed scenes no showing
  bug resulting from grid view. [Curt Wagner]

- Made grid option persistent using ngStorage. [Curt Wagner]

- Removed winsound from the project. Also added experimental grid view,
  and an option to hide info on actor detail page. [Curt Wagner]

- Added rating and runner up toggle to actor list. [Curt Wagner]

- Added more search options and filters. [Curt Wagner]

- Changed actor profile image dir names from actor names to actor id EX:
  instead media/actor/isis love/profile/profile.jpg it will be
  media/actor/17/profile/profile.jpg. [Curt Wagner]

  Also moved startup function from settings.py to urls.py and made it so that the folder names would change automatically on startup if they need to.

- Freeones scraper will now search for alias if it failed to find the
  main name. [Curt Wagner]

- Added rating bar to scene list view, also added settings.json
  versioning and 'last lookup' field for all scenes in settings.json.
  [Curt Wagner]

- Added recursion option to folder view. Now it's possible to view
  scenes that are inside of the current subfolders. [Curt Wagner]

- Actor Detail view looks slightly better. [Curt Wagner]

- Made it possible to search and order scenes in actor,website and scene
  tags views. [Curt Wagner]

- Scene list multiple tagging now works, fixed issue where pagination
  won't show in actor detail view. [Curt Wagner]

- Added 'Runner Up', and 'Play Scene' to scene list options. [Curt
  Wagner]

- Added 'Runner Up', and 'Play Scene' to scene list options. [Curt
  Wagner]

- Minor bug fix in addScenes. [Curt Wagner]

- Fixed some of the title issues... [Curt Wagner]

- Made actor name editable. [Curt Wagner]

- Added (x years old) to actor details if date of birth exists.  Moved
  loading of Actors,alisas,websits and tags out of the fileparser
  function so it won't load them each iteration. [Curt Wagner]

- Fixed dir creation path when actor image is uploaded. [Curt Wagner]

- Minor update to search term. [Curt Wagner]

- Added 'google image search' to actor details. [Curt Wagner]

- Changed upload url from "127.0.0.1:8000/upload" to "/upload/" [Curt
  Wagner]

- Added "is_exempt_from_one_word_search" to actor details. [Curt Wagner]

- Made folder view work with id paths  EX:"#!/folder/105" instead of
  calculating path internally. Also removed threading from 'add_scenes'
  function in addItems view. [Curt Wagner]

- Added unkown person image. [Curt Wagner]

- Initial commit. [Curt Wagner]


