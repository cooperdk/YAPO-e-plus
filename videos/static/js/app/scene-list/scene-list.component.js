// Register `phoneList` component, along with its associated controller and template
angular.module('sceneList').component('sceneList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: ['$element', '$attrs', function ($element, $attrs) {

        // if ($attrs.viewStyle == 'grid') {
        //     return 'static/js/app/scene-list/scene-list-grid.template.html'
        // } else {
            return 'static/js/app/scene-list/scene-list.template.html';
        // }


    }],
    bindings: {
        mainPage: '=',
        treeFolder: '='
    },
    controller: ['$scope', 'Scene', 'helperService', 'scopeWatchService', 'pagerService', 'Actor', 'Website', 'SceneTag', '$http', '$rootScope',
        function SceneListController($scope, Scene, helperService, scopeWatchService, pagerService, Actor, Website, SceneTag, $http, $rootScope) {

            var self = this;
            var actorLoaded = false;
            var sceneTagLoaded = false;
            var websiteLoaded = false;
            var folderLoaded = false;

            self.sceneArray = [];

            self.scenesToAdd = [];

            self.pageType = 'Scene';

            self.selectedScenes = [];

            self.selectAllStatus = false;

            self.tagMultiple = false;

            self.multiTag = function () {

                if (self.tagMultiple) {
                    self.tagMultiple = false;
                } else {
                    self.tagMultiple = true;
                }

            };
            
            
            self.gridView = false;


            var checkGridOption = function () {
                if ((helperService.getGridView() != undefined) && (helperService.getGridView()['scene'] != undefined)) {
                    self.gridView = helperService.getGridView()['scene']
                }
            };

            checkGridOption();

            $scope.$on("gridViewOptionChnaged", function (event, pageInfo) {
                checkGridOption()
            });


            self.selectAll = function () {

                self.selectedScenes = [];
                for (var i = 0; i < self.scenes.length; i++) {
                    self.scenes[i].selected = true;
                    self.selectedScenes.push(self.scenes[i].id)
                }

            };


            self.selectNone = function () {

                for (var i = 0; i < self.scenes.length; i++) {
                    self.scenes[i].selected = false;
                }
                self.selectedScenes = [];

            };

            self.sceneSelectToggle = function (scene) {

                var found = false;

                for (var i = 0; i < self.selectedScenes.length; i++) {
                    if (scene.id == self.selectedScenes[i]) {
                        found = true;
                    }

                }

                if (!found) {
                    self.selectedScenes.push(scene.id)

                }

                if (found) {
                    self.selectedScenes.splice(self.selectedScenes.indexOf(scene.id), 1)
                }

                // alert(angular.toJson(self.selectedScenes))

            };


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

                var input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    actor: self.actor,
                    sceneTag: self.sceneTag,
                    website: self.website,
                    folder: self.folder,
                    searchTerm: self.searchTerm,
                    searchField: self.searchField,
                    sortBy: self.sortBy,
                    isRunnerUp: self.runnerUp,
                    recursive: self.recursive
                };

                self.scrollBusy = true;


                self.actorsToadd = pagerService.getNextPage(input
                );


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


            // This is necessery for now because sometimes  the "actorLoaded" event is fired before
            // this script is loaded so we miss it and don't load any scenes.
            // This workaround fire an event that checks if an actor was loaded if it was it then fire the
            // actorLoaded event that we can catch.


            $scope.$on("actorLoaded", function (event, actor) {
                self.actor = actor;

                self.nextPage(0);
                actorLoaded = true;
            });

            if (!actorLoaded) {
                scopeWatchService.didActorLoad("a");
            }


            $scope.$on("sceneTagLoaded", function (event, sceneTag) {
                self.sceneTag = sceneTag;
                self.nextPage(0);
                sceneTagLoaded = true;
            });

            if (!sceneTagLoaded) {
                scopeWatchService.didSceneTagLoad("a");
            }

            $scope.$on("websiteLoaded", function (event, website) {
                self.website = website;
                self.nextPage(0);
                websiteLoaded = true
            });

            if (!websiteLoaded) {
                scopeWatchService.didWebsiteLoad('a');
            }

            $scope.$on("folderOpened", function (event, folder) {
                console.log("scene-list: folderOpened broadcast was caught");
                self.scenes = [];
                self.folder = folder['dir'];
                self.recursive = folder['recursive'];
                // alert(folder['recursive']);
                // self.scenes = [];
                self.nextPage(0);
                folderLoaded = true;
            });

            if (!folderLoaded) {
                scopeWatchService.didFolderLoad('a');
            }


            var findIndexOfSceneInList = function (sceneToFind) {
                var found = false;
                var ans = null;
                for (var i = 0; i < self.scenes.length && !found; i++) {
                    if (sceneToFind == self.scenes[i].id) {
                        found = true;
                        ans = i
                    }
                }
                return ans;

            };


            self.updateScenesOnRemove = function (scenes, itemToRemove, typeOfItemToRemove) {
                var resId = [];
                var resObj = [];
                if (typeOfItemToRemove == 'delete') {

                    for (var x = 0; x < scenes.length; x++) {
                        self.removeSceneFromList(scenes[x]);
                    }

                } else {


                    for (var j = 0; j < scenes.length; j++) {

                        var sceneIndex = findIndexOfSceneInList(scenes[j]);


                        for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToRemove].length; i++) {
                            if (itemToRemove.id != self.scenes[sceneIndex][typeOfItemToRemove][i].id) {
                                resId.push(self.scenes[sceneIndex][typeOfItemToRemove][i].id);
                                resObj.push(self.scenes[sceneIndex][typeOfItemToRemove][i]);
                            }
                        }

                        self.scenes[sceneIndex][typeOfItemToRemove] = resObj;

                        resObj = [];

                    }

                }


                return resId


            };

            self.removeSceneFromList = function (sceneToRemvoe) {

                var index_of_scene = -1;

                if (typeof sceneToRemvoe === 'object') {
                    index_of_scene = findIndexOfSceneInList(sceneToRemvoe.id);
                } else {
                    index_of_scene = findIndexOfSceneInList(sceneToRemvoe);
                }

                self.scenes.splice(index_of_scene, 1);

            };

            self.removeItem = function (scene, itemToRemove, typeOfItemToRemove, permDelete) {


                var resId = [];
                var sceneIndex = findIndexOfSceneInList(scene.id);


                if (self.selectedScenes.length > 0 && checkIfSceneSelected(scene)) {
                    if (typeOfItemToRemove != 'delete') {
                        var itToRemove = [];
                        itToRemove.push(itemToRemove.id);
                    }

                    self.patchScene(self.scenes[sceneIndex].id, typeOfItemToRemove, itToRemove, 'remove', true, permDelete)
                } else {
                    
                    self.patchScene(self.scenes[sceneIndex].id, typeOfItemToRemove, resId, 'remove', false, permDelete)
                }

                if (self.selectedScenes.length > 0 && checkIfSceneSelected(scene)) {

                    self.updateScenesOnRemove(self.selectedScenes, itemToRemove, typeOfItemToRemove)
                } else {
                    if (typeOfItemToRemove != 'delete') {
                        var scenes = [];
                        scenes.push(scene.id);
                        resId = self.updateScenesOnRemove(scenes, itemToRemove, typeOfItemToRemove)
                    } else {
                        if (!permDelete){
                            self.removeSceneFromList(scene)    
                        }
                        

                    }

                }


                self.selectNone()


            };

            var updateSceneOnPageOnAdd = function (sceneIndex, typeOfItemToAdd, itemToAdd) {

                var found = false;
                for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToAdd].length && !found; i++) {
                    if (self.scenes[sceneIndex][typeOfItemToAdd][i].id == itemToAdd.id) {
                        found = true;
                    }
                }

                if (!found) {
                    self.scenes[sceneIndex][typeOfItemToAdd].push(itemToAdd);
                }
            };

            var updateScenesOnPageOnAdd = function (itemToAdd, typeOfItemToAdd) {

                for (var i = 0; i < self.selectedScenes.length; i++) {

                    var sceneIndex = findIndexOfSceneInList(self.selectedScenes[i]);
                    updateSceneOnPageOnAdd(sceneIndex, typeOfItemToAdd, itemToAdd);


                }
            };

            var checkIfSceneSelected = function (scene) {
                var found = false;
                for (var i = 0; i < self.selectedScenes.length && !found; i++) {
                    if (scene.id == self.selectedScenes[i]) {
                        found = true;
                    }

                }

                return found

            };


            self.addItem = function (scene, itemToAdd, typeOfItemToAdd) {

                var sceneIndex = findIndexOfSceneInList(scene.id);

                if (self.scenes[sceneIndex][typeOfItemToAdd] == undefined) {
                    self.scenes[sceneIndex][typeOfItemToAdd] = [];
                }


                if (itemToAdd.id != '-1') {





                    // console.log(self.scenes[sceneIndex][typeOfItemToAdd].indexOf(itemToAdd));
                    // if (self.scenes[sceneIndex][typeOfItemToAdd].indexOf(itemToAdd) == '-1'){
                    //     self.scenes[sceneIndex][typeOfItemToAdd].push(itemToAdd);
                    // }

                    var patchData = [];
                    if (self.selectedScenes.length > 0 && checkIfSceneSelected(scene)) {
                        updateScenesOnPageOnAdd(itemToAdd, typeOfItemToAdd);


                        patchData.push(itemToAdd.id);


                        self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add', true)
                    } else {
                        updateSceneOnPageOnAdd(sceneIndex, typeOfItemToAdd, itemToAdd);


                        for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToAdd].length; i++) {
                            patchData.push(self.scenes[sceneIndex][typeOfItemToAdd][i].id);
                        }

                        self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add', false)
                    }


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


                        // self.scenes[sceneIndex][typeOfItemToAdd].push(res);
                        //
                        // var patchData = [];
                        // for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToAdd].length; i++) {
                        //     patchData.push(self.scenes[sceneIndex][typeOfItemToAdd][i].id);
                        // }
                        //
                        // if (self.selectedScenes.length > 0 && checkIfSceneSelected(scene)) {
                        //     updateScenesOnPageOnAdd(itemToAdd, typeOfItemToAdd);
                        //     self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add', true)
                        // } else {
                        //     updateSceneOnPageOnAdd(sceneIndex, typeOfItemToAdd, itemToAdd);
                        //     self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add', false)
                        // }

                        // self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add');

                        // self.updateActor(self.actor);

                        var patchData = [];
                        if (self.selectedScenes.length > 0 && checkIfSceneSelected(scene)) {
                            updateScenesOnPageOnAdd(res, typeOfItemToAdd);


                            patchData.push(res.id);


                            self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add', true)
                        } else {
                            updateSceneOnPageOnAdd(sceneIndex, typeOfItemToAdd, res);


                            for (var i = 0; i < self.scenes[sceneIndex][typeOfItemToAdd].length; i++) {
                                patchData.push(self.scenes[sceneIndex][typeOfItemToAdd][i].id);
                            }

                            self.patchScene(scene.id, typeOfItemToAdd, patchData, 'add', false)
                        }


                    })
                }


            };

            self.patchScene = function (sceneToPatchId, patchType, patchData, addOrRemove, multiple, permDelete) {

                var type = {};
                type[patchType] = patchData;


                if (multiple) {

                    $http.post('tag-multiple-items/', {
                        params: {
                            type: 'scene',
                            patchType: patchType,
                            patchData: patchData,
                            itemsToUpdate: self.selectedScenes,
                            addOrRemove: addOrRemove,
                            permDelete: permDelete
                        }
                    }).then(function (response) {
                        console.log("Update finished successfully")
                    }, function errorCallback(response) {
                        alert("Something went wrong!");
                    });


                } else {
                    if (patchType == 'delete') {
                        if (!permDelete){
                            Scene.remove({sceneId: sceneToPatchId});    
                        }

                    } else {
                        Scene.patch({sceneId: sceneToPatchId}, type)
                    }

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

                var selectedWebsite = object['selectedObject'];
                var scene = object['originalObject'];

                self.addItem(scene, selectedWebsite, 'websites');


            });


            $scope.$on("searchTermChanged", function (event, searchTerm) {

                if (searchTerm['sectionType'] == 'SceneList') {
                    self.scenes = [];
                    self.searchTerm = searchTerm['searchTerm'];
                    self.searchField = searchTerm['searchField'];
                    self.nextPage(0);
                }

            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                if (sortOrder['sectionType'] == 'SceneList') {
                    console.log("Sort Order Changed!");
                    self.scenes = [];
                    self.sortBy = sortOrder['sortBy'];
                    self.nextPage(0);
                }

            });

            $scope.$on("runnerUpChanged", function (event, runnerUp) {
                if (runnerUp['sectionType'] == 'SceneList') {
                    console.log("Sort Order Changed!");
                    self.scenes = [];
                    self.runnerUp = runnerUp['runnerUp'];
                    self.nextPage(0);
                }

            });


            self.sceneRunnerUpToggle = function (scene) {

                self.patchScene(scene.id, 'is_runner_up', scene.is_runner_up, 'add', false)

            };


            self.sceneRatingPatch = function (scene) {

                self.patchScene(scene.id, 'rating', scene.rating, 'add', false)

            };


            self.sceneArrayPush = function (sceneId) {

                self.sceneArray.push(sceneId);
                // console.log("Scene-List: sceneArray is:" +  angular.toJson(self.sceneArray))
            };

            self.playScene = function (scene) {

                return $http.get('play-scene/', {
                    params: {
                        sceneId: scene.id
                    }
                })
            };


            self.deleteScene = function (sceneToRemove) {

                if (self.selectedScenes == [] || self.selectedScenes.indexOf(sceneToRemove.id) == -1) {
                    Scene.remove({sceneId: sceneToRemove.id});

                    var index_of_scene = findIndexOfSceneInList(sceneToRemove.id);
                    self.scenes.splice(index_of_scene, 1);
                }


            };


        }
    ]
});