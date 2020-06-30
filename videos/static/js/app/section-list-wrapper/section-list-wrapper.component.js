angular.module('sectionListWrapper').component('sectionListWrapper', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/section-list-wrapper/section-wrapper.template.html',
        bindings: {
            sectionType: '=',
            mainPage: '=',
            callingObject: '=',
            callingObjectType: '='

        },
        controller: ['$scope', '$rootScope', '$rootScope', 'scopeWatchService', '$routeParams', 'helperService',
            function ActorListWrapperController($scope, Actor, $rootScope, scopeWatchService, $routeParams, helperService) {

                var self = this;

                var searchTerm = "";

                var sectionListWrapperLoaded = false;

                self.orderFields = "";
                self.searchInFields = "";
                self.runnerUp = 0;

                $scope.missingEthnicity = false;


                if (helperService.getGridView() != undefined) {
                    if (helperService.getGridView()['actor'] == undefined) {
                        self.actorGridView = false;
                    } else {
                        self.actorGridView = helperService.getGridView()['actor']
                    }

                    if (helperService.getGridView()['scene'] == undefined) {
                        self.sceneGridView = false;
                    } else {
                        self.sceneGridView = helperService.getGridView()['scene']
                    }
                } else {
                    self.actorGridView = false;
                    self.sceneGridView = false;
                }


                self.saveGridView = function () {


                    // self.mainPage = false;

                    helperService.setGridView({'actor': self.actorGridView, 'scene': self.sceneGridView});

                    scopeWatchService.gridViewOptionChnaged("a");

                    // scopeWatchService.searchTermChanged({
                    //     'sectionType': self.sectionType,
                    //     'searchTerm': self.searchTerm,
                    //     'searchField': self.searchField
                    // });
                    //
                    // scopeWatchService.sortOrderChanged({'sectionType': self.sectionType, 'sortBy': self.sortBy});
                    // scopeWatchService.runnerUpChanged({'sectionType': self.sectionType, 'runnerUp': self.runnerUp});


                };


                self.routParam = $routeParams.parentId;

                self.sectionTypefunc = function (typeToCheck) {
                    console.log("sectionTypefunc triggered " + self.sectionType);

                    if (self.sectionType == typeToCheck) {
                        console.log("self.sectionType == typeToCheck is" + (self.sectionType == typeToCheck))
                    }

                    return self.sectionType == typeToCheck;
                };

                var actorOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Desc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Desc",
                    "height": "Height Asc",
                    "-height": "Height Desc",
                    "ethnicity": "Ethnicity Asc ",
                    "-ethnicity": "Ethnicity Dsc ",
                    "weight": "Weight Asc",
                    "-weight": "Weight Desc",
                    "country_of_origin": "Country Of Origin Asc",
                    "-country_of_origin": "Country Of Origin Desc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Desc",
                    "date_of_birth": "Date Of Birth Asc",
                    "-date_of_birth": "Date Of Birth Desc",
                    "measurements": "Measurements Asc",
                    "-measurements": "Measurements Desc",
                    "usage_count": "Usage Count Asc",
                    "-usage_count": "Usage Count Desc",
                    "play_count": "Play Count Asc",
                    "-play_count": "Play Count Desc",
                    "random": "Random"


                };

                var actorSearchInFields = {

                    "name": "Name",
                    "rating": "Rating",
                    "height": "Height",
                    "ethnicity": "Ethnicity",
                    "weight": "Weight",
                    "country_of_origin": "Country Of Origin",
                    "measurements": "Measurements"
                };

                var sceneOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Desc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Desc",
                    "path_to_dir": "Path Asc",
                    "-path_to_dir": "Path Desc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Desc",
                    "date_last_played": "Date Last Played Asc",
                    "-date_last_played": "Date Last Played Desc",
                    "play_count": "Play Count Asc",
                    "-play_count": "Play Count Desc",
                    "height": "Resolution Height Asc",
                    "-height": "Resolution Height Desc",
                    "duration": "Duration Asc",
                    "-duration": "Duration Desc",
                    "size": "Size Asc",
                    "-size": "Size Desc",
                    "framerate": "Framerate Asc",
                    "-framerate": "Framerate Desc",
                    "hash": "Hash Asc",
                    "-hash": "Hash Desc",
                    "random": "Random"
                };

                var sceneSearchInFields = {

                    "name": "Name",
                    "rating": "Rating",
                    "path_to_file": "Path",
                    "duration": "Duration",
                    "size": "Size",
                    "framerate": "Framerate",
                    "height": "Resolution Height",
                    "play_count": "Play Count",
                    "hash": "Hash"

                };


                var websiteOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Desc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Desc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Desc",
                    "usage_count": "Usage Count Asc",
                    "-usage_count": "Usage Count Desc",
                    "play_count": "Play Count Asc",
                    "-play_count": "Play Count Desc",
                    "random": "Random"


                };

                var websiteSearchInFields = {

                    "name": "Name",
                    "rating": "Rating"

                };

                var actorTagOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Desc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Desc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Desc",
                    "usage_count": "Usage Count Asc",
                    "-usage_count": "Usage Count Desc",
                    "random": "Random"


                };


                var actorTagSearchInFields = {

                    "name": "Name",
                    "rating": "Rating"

                };

                var sceneTagOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Desc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Desc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Desc",
                    "usage_count": "Usage Count Asc",
                    "-usage_count": "Usage Count Desc",
                    "play_count": "Play Count Asc",
                    "-play_count": "Play Count Desc",
                    "random": "Random"


                };

                var sceneTagSearchInFields = {

                    "name": "Name",
                    "rating": "Rating"

                };


                var dbFolderOrderFields = {

                    "name": "Path Asc",
                    "-name": "Path Desc",
                    "last_folder_name_only": "Last Folder Name Asc",
                    "-last_folder_name_only": "Last Folder Name Desc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Desc",
                    "random": "Random"


                };

                var dbFolderSearchInFields = {

                    "name": "Path",
                    "last_folder_name_only": "Last Folder Name"


                };


                var getSortBy = function (section) {
                    var ans = "name";

                    var sectionSortByDict = helperService.getSortByInSectionWrapper();

                    if (sectionSortByDict != undefined) {

                        if (sectionSortByDict[section] != undefined) {

                            ans = sectionSortByDict[section]
                        }

                    }

                    return ans;

                };


                // self.sortBy = "name";
                self.searchField = "name";


                self.searchTerm = searchTerm;


                self.searchTermChanged = function () {

                    scopeWatchService.searchTermChanged({
                        'sectionType': self.sectionType,
                        'searchTerm': self.searchTerm,
                        'searchField': self.searchField
                    })
                };


                self.sortOrderChanged = function () {

                    scopeWatchService.sortOrderChanged({'sectionType': self.sectionType, 'sortBy': self.sortBy});
                    helperService.setSortByInSectionWrapper(self.sortBy, self.sectionType)
                };

                self.mainPageInit = function () {
                    scopeWatchService.sortOrderChanged({
                        'sectionType': self.sectionType,
                        'sortBy': self.sortBy,
                        'mainPage': self.mainPage
                    });
                 if (self.sectionType == 'ActorList') {
                    self.orderFields = actorOrderFields;
                    self.searchInFields = actorSearchInFields;
                    $rootScope.title = "Actors";
                    self.sortBy = getSortBy('ActorList');
                    


                } else if (self.sectionType == 'SceneList') {
                    self.orderFields = sceneOrderFields;
                    self.searchInFields = sceneSearchInFields;
                    $rootScope.title = "Scenes";
                    self.sortBy = getSortBy('SceneList');
                    

                } else if (self.sectionType == 'WebsiteList') {
                    self.orderFields = websiteOrderFields;
                    self.searchInFields = websiteSearchInFields;
                    $rootScope.title = "Websites";
                    self.sortBy = getSortBy('WebsiteList');
                    

                } else if (self.sectionType == 'ActorTagList') {
                    self.orderFields = actorTagOrderFields;
                    self.searchInFields = actorTagSearchInFields;
                    $rootScope.title = "Actor Tags";
                    self.sortBy = getSortBy('ActorTagList');
                    

                } else if (self.sectionType == 'SceneTagList') {
                    self.orderFields = sceneTagOrderFields;
                    self.searchInFields = sceneTagSearchInFields;
                    $rootScope.title = "Scene Tags";
                    self.sortBy = getSortBy('SceneTagList');
                    

                } else if (self.sectionType == 'DbFolder') {
                    self.orderFields = dbFolderOrderFields;
                    self.searchInFields = dbFolderSearchInFields;
                    $rootScope.title = "Folders";
                    self.sortBy = getSortBy('DbFolder');
                    


                }
                };


                self.runnerUpFilterChange = function () {
                    scopeWatchService.runnerUpChanged({'sectionType': self.sectionType, 'runnerUp': self.runnerUp});
                };


                if (self.sectionType == 'ActorList') {
                    self.orderFields = actorOrderFields;
                    self.searchInFields = actorSearchInFields;
                    $rootScope.title = "Actors";
                    self.sortBy = getSortBy('ActorList');
                    self.mainPageInit();


                } else if (self.sectionType == 'SceneList') {
                    self.orderFields = sceneOrderFields;
                    self.searchInFields = sceneSearchInFields;
                    $rootScope.title = "Scenes";
                    self.sortBy = getSortBy('SceneList');
                    self.mainPageInit();

                } else if (self.sectionType == 'WebsiteList') {
                    self.orderFields = websiteOrderFields;
                    self.searchInFields = websiteSearchInFields;
                    $rootScope.title = "Websites";
                    self.sortBy = getSortBy('WebsiteList');
                    self.mainPageInit();

                } else if (self.sectionType == 'ActorTagList') {
                    self.orderFields = actorTagOrderFields;
                    self.searchInFields = actorTagSearchInFields;
                    $rootScope.title = "Actor Tags";
                    self.sortBy = getSortBy('ActorTagList');
                    self.mainPageInit();

                } else if (self.sectionType == 'SceneTagList') {
                    self.orderFields = sceneTagOrderFields;
                    self.searchInFields = sceneTagSearchInFields;
                    $rootScope.title = "Scene Tags";
                    self.sortBy = getSortBy('SceneTagList');
                    self.mainPageInit();

                } else if (self.sectionType == 'DbFolder') {
                    self.orderFields = dbFolderOrderFields;
                    self.searchInFields = dbFolderSearchInFields;
                    $rootScope.title = "Folders";
                    self.sortBy = getSortBy('DbFolder');
                    self.mainPageInit();


                }

                sectionListWrapperLoaded = true;


                $scope.$on("didSectionListWrapperLoaded", function (event, callingSection) {

                    if (self.sectionType == callingSection) {
                        self.mainPageInit();
                    }

                });


            }
        ]
    }
);