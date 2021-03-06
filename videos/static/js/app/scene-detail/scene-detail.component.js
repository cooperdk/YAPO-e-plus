angular.module('sceneDetail').component('sceneDetail', {
    templateUrl: 'static/js/app/scene-detail/scene-detail.template.html',
    controller: ['$routeParams', 'Scene', 'helperService', '$scope', 'SceneTag', 'Actor', 'Website', '$http', '$rootScope', 'scopeWatchService', '$localStorage', '$sessionStorage',
        function SceneDetailController($routeParams, Scene, helperService, $scope, SceneTag, Actor, Website, $http, $rootScope, scopeWatchService, $localStorage,
                                       $sessionStorage) {
            var self = this;
            var sceneList = helperService.get();

            var counter = 0;

            self.samplePath = "";

            var gotPromise = false;
            var askedForSample = false;

            self.next = null;
            self.prev = null;
            self.callerPage = null;
            self.selectedSceneTag = null;
            self.selectedActor = null;
            self.selectedWebsite = null;

            self.isSampleExists = false;
            self.updatedSample = true;
            self.forceScan = false;
            self.alerts = [];
            self.addAlert = function (msg, type, timeout) {
                self.alerts.push({msg: msg, type: type, timeout: timeout});
            };

            self.closeAlert = function (index) {
                self.alerts.splice(index, 1);
            };

            self.addItem = function (itemToAdd, typeOfItemToAdd) {

                var patchData = [];
               

                if (itemToAdd.id != '-1') {
                    patchData.push(itemToAdd.id);
                    self.scene = $rootScope.addItemToScene(self.scene, itemToAdd, typeOfItemToAdd);
                    // function (sceneToPatchId, patchType, patchData, addOrRemove, multiple, permDelete)
                    $rootScope.patchEntity('scene',self.scene.id, typeOfItemToAdd, patchData, 'add', false, false, null)
                } else {
                    var newItem = $rootScope.createNewItem(typeOfItemToAdd, itemToAdd.value);
                    newItem.$save().then(function (res) {
                        self.scene = $rootScope.addItemToScene(self.scene, res, typeOfItemToAdd);
                        patchData.push(res.id);
                        $rootScope.patchEntity('scene', self.scene.id, typeOfItemToAdd, patchData, 'add', false, false, null)
                    });

                }

            };
            
            self.removeItem = function (itemToRemove, typeOfItemToRemove) {
                var patchData = [];
                patchData.push(itemToRemove.id);
                self.scene = $rootScope.removeItemFromScene(self.scene,itemToRemove,typeOfItemToRemove);
                $rootScope.patchEntity('scene',self.scene.id,typeOfItemToRemove,patchData,'remove',false,false,null)
            };


            $scope.$on("sceneChanged", function (event, scene) {
                console.log("scene-detail: sceneChanged was triggered. Scene is: " + angular.toJson(scene));
                self.updateScene(scene);
            });


            $scope.$on("actorSelected", function (event, selectedActor) {
                self.actor = selectedActor['selectedObject'];
                // self.actorSelect(self.actor);
                self.addItem(selectedActor['selectedObject'], 'actors')
            });


            $scope.$on("websiteSelected", function (event, website) {
                self.website = website['selectedObject'];
                // self.websiteSelect(self.website);
                self.addItem(website['selectedObject'], 'websites')

            });

            $scope.$on("sceneTagSelected", function (event, sceneTag) {
                // self.sceneTagSelect(sceneTag['selectedObject'], true);
                self.addItem(sceneTag['selectedObject'], 'scene_tags')
            });


            // self.currentScene;
            console.log("scene-detail: Helper service data is " + angular.toJson(sceneList));
            console.log("scene-detail: Helper service data is " + sceneList);

            self.getCurrentScene = function () {

                self.scene = Scene.get({sceneId: $routeParams.sceneId}).$promise.then(function (res) {
                    self.currentScene = res.id;
                    console.log("Scene detail: current id is " + angular.toJson(self.currentScene));
                    self.scene = res;
                    gotPromise = true;
					self.scene.framerate = self.scene.framerate.toFixed(2);

                    self.samplePath = '/media/scenes/' + res.id + '/sample/sample.mp4';
                    $rootScope.title = res.name;
                    self.sheetPath = '/media/scenes/' + res.id + '/sheet.jpg';

                    scopeWatchService.sceneLoaded(res);

                    self.getNext();
                    self.getPrev();
                });

            };

            $scope.$on("didSceneLoad", function (event, scene) {

                if (gotPromise) {
                    scopeWatchService.sceneLoaded(self.scene)
                }

            });

            self.getCurrentScene();


            self.didGetPromise = function () {
                alert("gotPromise = " + gotPromise);
                return gotPromise;
            };

            self.updateScene = function (scene) {
                Scene.update({sceneId: scene.id}, scene);
            };

            self.sceneTagSelect = function (sceneTag, isSourceOfRequest) {
                // alert("item " +
                // angular.toJson($item) +
                // "model:" + angular.toJson($model) +
                // "lable:" + angular.toJson($label)
                //
                // );
                if (sceneTag.id != '-1') {
                    // alert("This is not a create statement");
                    var found = false;
                    for (var i = 0; i < self.scene.scene_tags.length && !found; i++) {
                        if (sceneTag.id == self.scene.scene_tags[i]) {
                            found = true;
                        }
                    }
                    if (!found) {
                        self.scene.scene_tags.push(sceneTag.id);

                        if (isSourceOfRequest) {
                            self.updateScene(self.scene);
                        }


                        scopeWatchService.addSceneTagToList(sceneTag);

                    }


                } else {

                    // alert("This is a create statment");
                    var newSceneTag = new SceneTag();
                    newSceneTag.name = sceneTag.value;
                    newSceneTag.scenes = [];
                    newSceneTag.websites = [];
                    newSceneTag.scenes.push(self.scene.id);

                    newSceneTag.$save().then(function (res) {
                        self.scene.scene_tags.push(res.id);
                        self.updateScene(self.scene);

                        res.name = sceneTag.value;
                        scopeWatchService.addSceneTagToList(res);

                    })

                }
            };

            self.websiteSelect = function (website) {

                if (website.id != '-1') {
                    // alert("This is not a create statement");
                    var found = false;
                    for (var i = 0; i < self.scene.websites.length && !found; i++) {
                        if (website.id == self.scene.websites[i]) {
                            found = true;
                        }
                    }
                    if (!found) {

                        self.scene.websites.push(website.id);

                        if (website.scene_tags_with_names.length > 0) {
                            for (var i = 0; i < website.scene_tags_with_names.length; i++) {
                                self.sceneTagSelect(website.scene_tags_with_names[i], false)
                            }
                        }

                        self.updateScene(self.scene);
                        scopeWatchService.addWebsiteToList(website);


                    }


                } else {

                    // alert("This is a create statment");
                    var newWebsite = new Website();
                    newWebsite.name = website.value;
                    newWebsite.scenes = [];
                    newWebsite.scenes.push(self.scene.id);
                    newWebsite.scene_tags = [];


                    // newActor.scenes.push(self.scene.id);
                    // alert("New actorTag name is:" + $item.value);
                    // alert(angular.toJson(newActorTag));
                    newWebsite.$save().then(function (res) {
                        self.scene.websites.push(res.id);
                        self.updateScene(self.scene);
                        scopeWatchService.addWebsiteToList(res);


                        // self.updateActor(self.actor);
                    })

                }

            };


            self.actorSelect = function (actor) {
                // alert("item " +
                // angular.toJson($item) +
                // "model:" + angular.toJson($model) +
                // "lable:" + angular.toJson($label)
                //
                // );
                if (actor.id != '-1') {
                    // alert("This is not a create statement");
                    var found = false;
                    for (var i = 0; i < self.scene.actors.length && !found; i++) {
                        if (actor.id == self.scene.actors[i]) {
                            found = true;
                        }
                    }
                    if (!found) {
                        console.log("scene-detail: self.scene.actors: " + angular.toJson(self.scene.actors));
                        // if (self.scene.actors == '-1') {
                        //     self.scene.actors = [];
                        // }
                        console.log("%c scene-detail: self.scene is " + angular.toJson(self.scene), 'background: #380; color: #bada55');


                        console.log("%c scene-detail: self.scene actors before push are: " + angular.toJson(self.scene.actors), 'background: #380; color: #bada55');
                        self.scene.actors.push(actor.id);
                        console.log("%c scene-detail: self.scene actors after push are: " + angular.toJson(self.scene.actors), 'background: #380; color: #bada55');


                        self.updateScene(self.scene);

                        scopeWatchService.addActorToList(actor);
                    }


                } else {

                    // alert("This is a create statment");
                    var newActor = new Actor();
                    newActor.name = actor.value;
                    newActor.scenes = [];
                    newActor.websites = [];
                    newActor.thumbnail = 'media/images/actor/Unknown/profile/profile.jpg';

                    // newActor.scenes.push(self.scene.id);
                    // alert("New actorTag name is:" + $item.value);
                    // alert(angular.toJson(newActorTag));
                    newActor.$save().then(function (res) {

                        self.scene.actors.push(res.id);
                        self.updateScene(self.scene);


                        scopeWatchService.addActorToList(res);
                        // self.updateActor(self.actor);
                    })

                }
            };

            self.videoWidth = 720;
            self.zoomUp = function zoomUp(zoomfactor) {
                self.videoWidth = self.videoWidth * zoomfactor
            };

            self.zoomDown = function zoomDown(zoomfactor) {
                self.videoWidth = self.videoWidth / zoomfactor
            };

            self.getNext = function () {
                console.log("scene-detail.componenet: sceneList is: " + angular.toJson(sceneList));
                if (sceneList.length > 1) {
                    var currentIndex = sceneList.indexOf(self.currentScene);
                    console.log("indexOf current is " + angular.toJson(sceneList.indexOf(self.currentScene)));
                    if (currentIndex < sceneList.length - 1) {
                        self.next = sceneList[currentIndex + 1];

                    } else {
                        self.next = sceneList[0];
                    }
                    console.log("scene-detail: next id is " + angular.toJson(self.next));
                }

            };


            self.getPrev = function () {
                if (sceneList.length > 1) {
                    var currentIndex = sceneList.indexOf(self.currentScene);
                    if (currentIndex > 0) {
                        self.prev = sceneList[currentIndex - 1];

                    } else {
                        self.prev = sceneList[sceneList.length - 1];
                    }
                    console.log("scene-detail: prev id is " + angular.toJson(self.prev));
                }

            };

            self.playScene = function () {

                return $http.get('play-scene/', {
                    params: {
                        sceneId: self.scene.id

                    }
                })
            };

            self.rename = function () {

                return $http.get('rename-scene/', {
                    params: {
                        sceneId: self.scene.id,
                        force: self.forceScan

                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    self.addAlert(response.data, 'success', '5000');
                    self.getCurrentScene()
                }, function errorCallback(response) {
                    self.addAlert(response.data, 'warning', '10000');
                    console.log(angular.toJson(response))
                });

            };

            self.openFolder = function () {

                return $http.get('open-folder/', {
                    params: {
                        path: self.scene.path_to_file
                    }
                })
            };

            self.scanScene = function (scanSite) {

                return $http.get('scan-scene/', {
                    params: {
                        scene: self.scene.id,
                        scanSite: scanSite,
                        force: self.forceScan

                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    self.addAlert(response.data, 'success', '10000');
                    self.getCurrentScene()
                }, function errorCallback(response) {
                    self.addAlert(response.data, 'warning', '20000');
                    console.log(angular.toJson(response))
                });


            };

            self.generateSampleVideo = function (scene) {
                self.addAlert("Generating sample video, please wait...", 'info', '100000');
                $http.get('ffmpeg/', {
                    params: {
                        generateSampleVideo: true,
                        sceneId: scene.id
                    }
                }).then(function (response) {
                    self.updatedSample = false;
                    self.updatedSample = true;
                    self.closeAlert();
                    self.getCurrentScene()
                    self.addAlert("Successfully generated the sample video.", 'success', '5000');
                }, function errorCallback(response) {
                    self.closeAlert();
                    self.addAlert("Something went wrong while generating the sample video, please check the console.", 'danger', '100000');
                });
            };
            
            
            $scope.$on("playlistSelected", function (event, object) {

                var selectedPlaylist = object['selectedObject'];
                var scene = object['originalObject'];


                self.addItem(selectedPlaylist, 'playlists');


            });


        }
    ]
});