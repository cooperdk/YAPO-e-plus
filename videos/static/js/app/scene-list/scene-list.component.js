// Register `phoneList` component, along with its associated controller and template
angular.module('sceneList').component('sceneList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/scene-list/scene-list.template.html',
    bindings: {
        mainPage: '=',
        treeFolder: '='
    },
    controller: ['$scope', 'Scene', 'helperService', 'scopeWatchService', 'pagerService', 'Actor', 'Website', 'SceneTag',
        function SceneListController($scope, Scene, helperService, scopeWatchService, pagerService, Actor, Website, SceneTag, $rootScope) {

            var self = this;
            self.sceneArray = [];

            self.scenesToAdd = [];

            self.pageType = 'Scene';


            // $rootScope.$storage = $localStorage;

            self.sceneArraystore = function () {

                // helperService.set(self.sceneArray);
                var scArray = [];
                for (i = 0; i < self.scenes.length; i++) {
                    scArray.push(self.scenes[i].id)
                }

                helperService.set(scArray);
                // $rootScope.$storage.scArray = scArray;

                console.log(helperService.get());
                // self.sceneArray = [];
            };

            self.sceneArrayClear = function () {
                console.log("scene arrray cleared!");
                if (($rootScope.$storage != undefined) && ($rootScope.$storage.scArray != undefined)) {
                    delete $rootScope.$storage.scArray;
                }


            };

            self.nextPage = function (currentPage) {
                // self.sceneArrayClear();
                console.log("scene-list: nextPage function triggered!");

                input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    actor: self.actor,
                    sceneTag: self.sceneTag,
                    website: self.website,
                    folder: self.folder,
                    searchTerm: self.searchTerm,
                    sortBy: self.sortBy,
                    isRunnerUp: self.runnerUp
                };

                self.scrollBusy = true;


                self.actorsToadd = pagerService.getNextPage(input
                );

                if (self.actorsToadd != undefined) {
                    self.actorsToadd.$promise.then(function (res) {

                        // self.actorsToadd = res[0];

                        var paginationInfo = {
                            pageType: input.pageType,
                            pageInfo: res[1]
                        };

                        scopeWatchService.paginationInit(paginationInfo);

                        self.scenes = helperService.resourceToArray(res[0]);

                        self.sceneArraystore();


                    });
                }

            };


            if (self.mainPage) {
                console.log("main page is true! + " + self.mainPage);
                self.nextPage(0);
            }

            if (self.treeFolder != undefined) {
                self.folder = self.treeFolder;
                self.nextPage(0);
            }

            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType) {
                    self.nextPage(pageInfo.page)
                }


            });


            $scope.$on("actorLoaded", function (event, actor) {
                self.actor = actor;
                self.nextPage(0);
            });

            $scope.$on("sceneTagLoaded", function (event, sceneTag) {
                self.sceneTag = sceneTag;
                self.nextPage(0);
            });


            var findIndexOfSceneInList = function (sceneToFind) {
                var found = false;
                var ans = null;
                for (var i = 0; i < self.scenes.length && !found; i++) {
                    if (sceneToFind.id == self.scenes[i].id) {
                        found = true;
                        ans = i
                    }
                }
                return ans;

            };


            self.patchScene = function (sceneToPatchId, patchType, patchData) {

                var type = {};
                type[patchType] = patchData;

                Scene.patch({sceneId: sceneToPatchId}, type)


            };

            self.removeItem = function (scene, itemToRemove, typeOfItemToRemove) {

                var sceneIndex = findIndexOfSceneInList(scene);

                var resId = [];
                var resObj = [];

                for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToRemove].length; i++) {
                    if (itemToRemove.id != self.scenes[sceneIndex][typeOfItemToRemove][i].id) {
                        resId.push(self.scenes[sceneIndex][typeOfItemToRemove][i].id);
                        resObj.push(self.scenes[sceneIndex][typeOfItemToRemove][i]);
                    }
                }

                self.scenes[sceneIndex][typeOfItemToRemove] = resObj;
                self.patchScene(self.scenes[sceneIndex].id, typeOfItemToRemove, resId)


            };

            self.addItem = function (scene, itemToAdd, typeOfItemToAdd) {

                var sceneIndex = findIndexOfSceneInList(scene);

                if (self.scenes[sceneIndex][typeOfItemToAdd] == undefined) {
                    self.scenes[sceneIndex][typeOfItemToAdd] = [];
                }


                if (itemToAdd.id != '-1') {


                    self.scenes[sceneIndex][typeOfItemToAdd].push(itemToAdd);

                    var patchData = [];
                    for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToAdd].length; i++) {
                        patchData.push(self.scenes[sceneIndex][typeOfItemToAdd][i].id);
                    }


                    self.patchScene(scene.id, typeOfItemToAdd, patchData)

                } else {
                    var newItem;
                    if (typeOfItemToAdd == 'actors') {
                        newItem = new Actor();
                        newItem.thumbnail = 'media/images/actor/Unknown/profile/profile.jpg'; //need to change this to a constant!
                        newItem.scenes = [];
                    } else if (typeOfItemToAdd == 'scene_tags') {
                        newItem = new SceneTag();
                        newItem.scenes = [];
                        newItem.websites = [];
                    } else if (typeOfItemToAdd == 'websites') {
                        newItem = new Website;
                        newItem.scenes = [];
                    }

                    newItem.name = itemToAdd.value;

                    newItem.$save().then(function (res) {


                        self.scenes[sceneIndex][typeOfItemToAdd].push(res);

                        var patchData = [];
                        for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToAdd].length; i++) {
                            patchData.push(self.scenes[sceneIndex][typeOfItemToAdd][i].id);
                        }


                        self.patchScene(scene.id, typeOfItemToAdd, patchData);

                        // self.updateActor(self.actor);
                    })
                }


            };

            // $scope.$on("sceneTagSelected", function (event, object) {
            //
            // };

            $scope.$on("actorSelected", function (event, object) {

                var selectedObject = object['selectedObject'];
                var originalObject = object['originalObject'];

                self.addItem(originalObject, selectedObject, 'actors');

            });


            $scope.$on("sceneTagSelected", function (event, object) {

                var selectedObject = object['selectedObject'];
                var originalObject = object['originalObject'];

                self.addItem(originalObject, selectedObject, 'scene_tags');

            });

            $scope.$on("websiteSelected", function (event, object) {

                var selectedObject = object['selectedObject'];
                var originalObject = object['originalObject'];

                self.addItem(originalObject, selectedObject, 'websites');

            });

            $scope.$on("websiteLoaded", function (event, website) {
                self.website = website;
                self.nextPage(0);
            });

            $scope.$on("folderOpened", function (event, folder) {
                console.log("scene-list: folderOpened broadcast was caught");
                self.scenes = [];
                self.folder = folder;
                // self.scenes = [];
                self.nextPage(0);
            });

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                self.scenes = [];
                self.searchTerm = searchTerm;
                self.nextPage(0);

            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                console.log("Sort Order Changed!");
                self.scenes = [];
                self.sortBy = sortOrder;
                self.nextPage(0);
            });

            $scope.$on("runnerUpChanged", function (event, runnerUp) {
                console.log("Sort Order Changed!");
                self.scenes = [];
                self.runnerUp = runnerUp;

                self.nextPage(0);
            });


            self.sceneArrayPush = function (sceneId) {

                self.sceneArray.push(sceneId);
                // console.log("Scene-List: sceneArray is:" +  angular.toJson(self.sceneArray))
            };


        }
    ]
});