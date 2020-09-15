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
            var didSectionListWrapperLoad = false;
            // self.tags = [];
            self.pageType = 'SceneTag';

            self.nextPage = function (currentPage) {
                var input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    scene: self.scene,
                    searchTerm: self.searchTerm,
                    searchField: self.searchField,
                    sortBy: self.sortBy
                };

                self.actorsToadd = pagerService.getNextPage(input);

                self.actorsToadd.$promise.then(function (res) {
                    var paginationInfo = {
                        pageType: input.pageType,
                        pageInfo: res[1]
                    };
                    scopeWatchService.paginationInit(paginationInfo);
                    self.tags = helperService.resourceToArray(res[0]);
                });
            };

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
                if (searchTerm['sectionType'] == 'SceneTagList'){
                    self.tags = [];
                    self.searchTerm = searchTerm['searchTerm'];
                    self.searchField = searchTerm['searchField'];
                    self.nextPage(0);
                }
            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                if (sortOrder['sectionType'] == 'SceneTagList'){
                    console.log("Sort Order Changed!");
                    self.tags = [];
                    self.sortBy = sortOrder['sortBy'];
                     if (sortOrder.mainPage == undefined || sortOrder.mainPage == true ) {
                        self.nextPage(0);
                    }
                    didSectionListWrapperLoad = true;
                }
            });

            if (!didSectionListWrapperLoad) {
                scopeWatchService.didSectionListWrapperLoaded('SceneTagList')
            }


            self.deleteSceneTag = function (tagToDelete) {
                if (angular.isObject(self.scene)) {
                    var res = helperService.removeObjectFromArrayOfObjects(tagToDelete,self.tags);

                    console.log(res['resId']);
                    self.scene.scene_tags = res['resId'];
                    scopeWatchService.sceneChanged(self.scene);

                    self.tags = res['resObject'];


                    // self.actor.actor_tags.splice(self.actor.actor_tags.indexOf(tagToDelete.id,1));
                    // alert(angular.toJson(self.actor.actor_tags));
                }
            };

            self.deleteSceneTagFromDb = function (tagToDelete) {
                SceneTag.remove({sceneTagId: tagToDelete.id});
                var ans = helperService.removeObjectFromArrayOfObjects(tagToDelete,self.tags);
                self.tags = ans['resObject'];
            }

        }
    ]
});
