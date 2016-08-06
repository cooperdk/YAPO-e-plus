// Register `phoneList` component, along with its associated controller and template
angular.module('sectionListWrapper').component('sectionListWrapper', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/section-list-wrapper/section-wrapper.template.html',
        bindings: {
            sectionType: '='
        },
        controller: ['$scope', '$rootScope', '$rootScope', 'scopeWatchService',
            function ActorListWrapperController($scope, Actor, $rootScope, scopeWatchService) {

                var self = this;
                $rootScope.title = "Actors";

                var searchTerm = "";

                self.orderFields = "";
                self.runnerUp = 0;

                self.sectionTypefunc = function (typeToCheck) {
                    console.log("sectionTypefunc triggered " + self.sectionType);
                    return self.sectionType == typeToCheck;
                };

                var actorOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Dsc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Dsc",
                    "height": "Height Asc",
                    "-height": "Height Dsc",
                    "ethnicity": "Ethnicity Asc ",
                    "-ethnicity": "Ethnicity Dsc ",
                    "weight": "Weight Asc",
                    "-weight": "Weight Dsc",
                    "country_of_origin": "Country Of Origin Asc",
                    "-country_of_origin": "Country Of Origin Dsc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Dsc",
                    "date_of_birth": "Date Of Birth Asc",
                    "-date_of_birth": "Date Of Birth Dsc",
                    "measurements": "Measurements Asc",
                    "-measurements": "Measurements Dsc",
                    "random": "Random"


                };

                var sceneOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Dsc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Dsc",
                    "path_to_dir": "Path Asc",
                    "-path_to_dir": "Path Dsc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Dsc",
                    "random": "Random"


                };

                var websiteOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Dsc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Dsc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Dsc",
                    "random": "Random"


                };

                var actorTagOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Dsc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Dsc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Dsc",
                    "random": "Random"


                };

                var sceneTagOrderFields = {

                    "name": "Name Asc",
                    "-name": "Name Dsc",
                    "rating": "Rating Asc",
                    "-rating": "Rating Dsc",
                    "date_added": "Date Added Asc",
                    "-date_added": "Date Added Dsc",
                    "random": "Random"


                };


                if (self.sectionType == 'ActorList') {
                    self.orderFields = actorOrderFields;
                } else if (self.sectionType == 'SceneList') {
                    self.orderFields = sceneOrderFields;
                } else if (self.sectionType == 'WebsiteList') {
                    self.orderFields = websiteOrderFields;
                } else if (self.sectionType == 'ActorTagList') {
                    self.orderFields = actorTagOrderFields;
                } else if (self.sectionType == 'SceneTagList') {
                    self.orderFields = sceneTagOrderFields;
                }


                self.sortBy = "name";


                self.searchTerm = searchTerm;

                self.searchTermChanged = function () {

                    scopeWatchService.searchTermChanged(self.searchTerm)
                };


                self.sortOrderChanged = function () {

                    scopeWatchService.sortOrderChanged(self.sortBy);
                };
                self.runnerUpFilterChange = function () {


                    scopeWatchService.runnerUpChanged(self.runnerUp);

                };


            }
        ]
    }
);