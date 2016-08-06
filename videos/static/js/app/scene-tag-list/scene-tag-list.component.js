// Register `phoneList` component, along with its associated controller and template
angular.module('sceneTagList').component('sceneTagList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/scene-tag-list/scene-tag-list.template.html',
    bindings: {
        mainPage: '='
    },
    controller: ['$scope', 'SceneTag', 'scopeWatchService', 'pagerService', 'helperService',
        function SceneTagListController($scope, SceneTag, scopeWatchService, pagerService, helperService) {

            var self = this;
            // self.tags = [];
            self.pageType = 'SceneTag';



            self.nextPage = function (currentPage) {


                input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    scene: self.scene,
                    searchTerm: self.searchTerm,
                    sortBy: self.sortBy

                };

                self.actorsToadd = pagerService.getNextPage(input);

                self.actorsToadd.$promise.then(function (res) {

                    // self.actorsToadd = res[0];

                    var paginationInfo = {
                        pageType: input.pageType,
                        pageInfo: res[1]
                    };

                    scopeWatchService.paginationInit(paginationInfo);

                    self.tags = helperService.resourceToArray(res[0]);


                });


            };


            if (self.mainPage) {
                console.log("main page is true! + " + self.mainPage);
                self.nextPage(0);
            }

            $scope.$on("sceneLoaded", function (event, scene) {
                self.scene = scene;
                self.nextPage(0);


            });

            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType){
                    self.nextPage(pageInfo.page)
                }


            });


            $scope.$on("addSceneTagToList", function (event, sceneTag) {
                self.tags.push(sceneTag)
            });

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                self.tags = [];
                self.searchTerm = searchTerm;
                self.nextPage(0);

            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                console.log("Sort Order Changed!");
                self.tags = [];
                self.sortBy = sortOrder;
                self.nextPage(0);
            });


            self.deleteSceneTag = function (tagToDelete) {
                // alert("delete scene tag was clicked!");
                if (angular.isObject(self.scene)) {
                    // self.pk.splice(self.pk.indexOf(aliasToDelete.id), 1);
                    // alert(angular.toJson(self.actor.actor_tags));
                    // alert(angular.toJson(tagToDelete));
                    // alert(angular.toJson(self.actor.actor_tags.indexOf(tagToDelete.id)));

                    var resId = [];
                    var resObjects = [];

                    for (i = 0; i < self.tags.length; i++) {
                        if (self.tags[i].id != tagToDelete.id) {
                            resId.push(self.tags[i].id);
                            resObjects.push(self.tags[i]);

                        }
                    }
                    self.scene.scene_tags = resId;
                    scopeWatchService.sceneChanged(self.scene);

                    self.tags = resObjects;


                    // self.actor.actor_tags.splice(self.actor.actor_tags.indexOf(tagToDelete.id,1));
                    // alert(angular.toJson(self.actor.actor_tags));
                }
            }

        }
    ]
});