angular.module('actorDetail').component('actorDetail', {
    templateUrl: '/static/js/app/actor-detail/actor-detail.template.html',
    controller: [
        '$routeParams',
        'Actor',
        'ActorAlias',
        'ActorTag',
        '$http',
        '$scope',
        'helperService',
        '$rootScope',
        'scopeWatchService',
        function ActorDetailController($routeParams,
                                       Actor,
                                       ActorAlias,
                                       ActorTag,
                                       $http,
                                       $scope,
                                       helperService,
                                       $rootScope,
                                       scopeWatchService) {


            var self = this;
            var counter = 0;
            var gotPromise = false;
            var changingView = false;

            self.birthdate = null;

            $scope.popup1 = {
                opened: false
            };

            $scope.open1 = function () {
                $scope.popup1.opened = true;
            };


            self.addItem = function (actor, itemToAdd, typeOfItemToAdd) {

                var patchData = [];


                if (itemToAdd.id != '-1') {
                    patchData.push(itemToAdd.id);
                    self.actor = $rootScope.addItemToScene(self.actor, itemToAdd, typeOfItemToAdd);
                    // function (sceneToPatchId, patchType, patchData, addOrRemove, multiple, permDelete)
                    $rootScope.patchEntity('actor', self.actor.id, typeOfItemToAdd, patchData, 'add', false, false, null);
                } else {
                    var newItem = $rootScope.createNewItem(typeOfItemToAdd, itemToAdd.value);
                    newItem.$save().then(function (res) {
                        self.scene = $rootScope.addItemToScene(self.actor, res, typeOfItemToAdd);
                        patchData.push(res.id);
                        $rootScope.patchEntity('actor', self.actor.id, typeOfItemToAdd, patchData, 'add', false, false, null);
                    });

                }

            };

            self.removeItem = function (itemToRemove, typeOfItemToRemove) {
                var patchData = [];
                patchData.push(itemToRemove.id);
                self.actor = $rootScope.removeItemFromScene(self.actor, itemToRemove, typeOfItemToRemove);
                $rootScope.patchEntity('actor', self.actor.id, typeOfItemToRemove, patchData, 'remove', false, false, null);
            };


            self.hideDetail = false;
            self.hideDetailButtomLable = 'Hide Detail';

            var checkHideDetailButton = function () {
                if (self.hideDetail) {
                    self.hideDetailButtomLable = 'Show Detail';
                } else {
                    self.hideDetailButtomLable = 'Hide Detail';
                }
            };

            self.hideDetailClick = function () {
                if (self.hideDetail) {
                    self.hideDetail = false;
                    self.hideDetailButtomLable = "Hide Detail";
                } else {
                    self.hideDetail = true;
                    self.hideDetailButtomLable = "Show Detail";
                }
            };


            var checkGridOption = function () {
                if ((helperService.getGridView() !== undefined) && (helperService.getGridView()['scene'] !== undefined)) {
                    self.hideDetail = helperService.getGridView()['scene'];
                    checkHideDetailButton();
                }
            };


            checkGridOption();

            $scope.$on("gridViewOptionChnaged", function (event, pageInfo) {
                checkGridOption();
                checkHideDetailButton();
                changingView = true
            });

            self.selectedActorTag = null;
            self.alerts = [];
            self.updateImage = true;
            self.forceScrape = false;

            self.addAlert = function (msg, type, timeout) {
                self.alerts.push({msg: msg, type: type, timeout: timeout});
            };

            self.closeAlert = function (index) {
                self.alerts.splice(index, 1);
            };


            $scope.$on("actorTagSelected", function (event, actorTag) {
                // alert(angular.toJson(actorTag));
                self.addItem(self.actor, actorTag, 'actor_tags');
                self.actorTagSelect(actorTag);


            });

            $scope.$on("actorChaned", function (event, actor) {
                self.actor = actor;
                self.updateActor(self.actor);


            });


            $scope.$on("addActorTagToList", function (event, actorTag) {
                self.actorTagSelect(actorTag);


            });


            $scope.$on("didActorLoad", function (event, actor) {

                if (gotPromise) {

                    scopeWatchService.actorLoaded(self.actor);


                    changingView = false;
                }
            });


            console.log("1 actor-detail self.actor is :" + angular.toJson(self.actor));
            self.getActor = function () {
                self.actor = Actor.get({actorId: $routeParams.actorId}).$promise.then(function (res) {
                    self.actor = res;
                    console.log("2 actor-detail self.actor is :" + angular.toJson(self.actor.name));
                    helperService.set2(self.actor);
                    scopeWatchService.actorLoaded(res);
                    $rootScope.actorLoaded = true;
                    $rootScope.loadedActor = res;
                    $rootScope.title = res.name;

                    var d = new Date(res.date_of_birth);
                    d.setMinutes(d.getMinutes() + d.getTimezoneOffset());
                    self.birthdate = d;
                    //alert(self.birthdate);
                    //self.birthdate = new Date(res.date_of_birth);
                    //alert(self.birthdate);

                    gotPromise = true;
                    // $scope.actor = res;
                });
            };

            self.getActor();


            self.imageWidth = 240;
            self.zoomUp = function zoomUp(zoomfactor) {
                self.imageWidth = self.imageWidth * zoomfactor
            };

            self.zoomDown = function zoomDown(zoomfactor) {
                self.imageWidth = self.imageWidth / zoomfactor
            };

            self.updateBirthday = function (actor) {

                var dd = self.birthdate.getDate();
                var mm = self.birthdate.getMonth() + 1; //January is 0!
                var yyyy = self.birthdate.getFullYear();

                actor.date_of_birth = yyyy + '-' + mm + '-' + dd;

                $rootScope.patchEntity('actor', self.actor.id, 'date_of_birth', self.actor.date_of_birth, 'add',
                    false, false, null)
                //self.updateActor(actor);
            };

            self.updateActor = function (object) {

                // var id = object.id + '/';
                // alert(id);

                Actor.update({actorId: object.id}, object);
                // return alert(object.id + ' ' + object.name + ' input: ' + input);
            };

            self.test2 = function (object, object2) {

                alert("Actor name is: " + object.name + " And Alias is " + object2.name + " " + object2.id);
                ActorAlias.update({actorAliasId: object2.id}, object2)
            };

            self.aliasInput = function (a) {

                var newAlias = new ActorAlias();
                newAlias.name = a;
                newAlias.$save().then(function (res) {
                    //alert(newAlias.id)
                    //alert(self.actor.actor_aliases.toString());
                    self.actor.actor_aliases.push(newAlias.id);
                    //alert(self.actor.actor_aliases.toString());
                    self.updateActor(self.actor);
                    scopeWatchService.addAliasToList(newAlias);
                });
            };

            self.states = [];

            var _selected;

            self.selectedTag = null;

            self.tagInput = function () {
                alert(angular.toJson(self.selectedTag))
            };

            self.actorTagSelect = function (actorTag) {
                // alert("item " +
                // angular.toJson($item) +
                // "model:" + angular.toJson($model) +
                // "lable:" + angular.toJson($label)
                //
                // );
                if (actorTag.id != '-1') {
                    // alert("This is not a create statement");
                    var found = false;
                    for (var i = 0; i < self.actor.actor_tags.length && !found; i++) {
                        if (actorTag.id == self.actor.actor_tags[i]) {
                            found = true;
                        }
                    }
                    if (!found) {
                        self.actor.actor_tags.push(actorTag.id);
                        self.updateActor(self.actor);

                        scopeWatchService.addActorTagToList(actorTag);

                    }


                } else {

                    // alert("This is a create statment");
                    var newActorTag = new ActorTag();
                    newActorTag.name = actorTag.value;
                    newActorTag.actors = [];
                    newActorTag.actors.push(self.actor.id);
                    // alert("New actorTag name is:" + $item.value);
                    // alert(angular.toJson(newActorTag));
                    newActorTag.$save().then(function (res) {
                        self.actor.actor_tags.push(res.id);

                        self.updateActor(self.actor);

                        scopeWatchService.addActorTagToList(res);

                        // self.updateActor(self.actor);
                    });

                }
            };

            self.st = function (v) {
                // alert(self.states.toString());
                return self.states;

            };

            self.getTags = function (val) {
                return $http.get('/api/actor-tag/', {
                    params: {
                        search: val

                    }
                }).then(function (response) {

                    var a = response.data.map(function (item) {
                        return item;
                    });


                    var b = [];
                    var found = false;
                    for (var i = 0; i < a.length; i++) {
                        console.log("Res to check:" + angular.toJson(a[i]));
                        for (var j = 0; j < self.actor.actor_tags.length && !found; j++) {
                            console.log("To check against:" + angular.toJson(self.actor.actor_tags[j]));
                            if (a[i].id == self.actor.actor_tags[j]) {
                                console.log("Match found: " + angular.toJson(a[i]) + " Matches: " + angular.toJson(self.actor.actor_tags[j]));
                                found = true;


                            }
                        }

                        if (!found) {
                            console.log("Res to push:" + angular.toJson(a[i]));
                            b.push(a[i]);
                            console.log("Res to array:" + angular.toJson(b));

                        }
                        found = false;
                    }

                    var createVal = {"id": -1, "name": "Create: " + "\"" + val + "\"", "value": val};
                    b.push(createVal);

                    // alert(angular.toJson(a));
                    return b;
                });


                // var res = [];
                //
                //
                // // alert(val);
                // var p = ActorTag.query({search: val}).$promise;
                //
                // var r = p.then(function (response) {
                //     // alert(angular.toJson(response));
                //     // alert(angular.toJson(response.data));
                //
                //     response.map(function (item) {
                //         // alert(angular.toJson(item));
                //         res.push(item.name);
                //     });
                //
                //     // alert(res.toString());
                //
                // });
                // self.states = res;
                // return self.states;
            };

            self.actorNameDelimiter = function (delimiter, imageSearch) {
                if (gotPromise) {
                    var newName = self.actor.name;
                    newName = newName.replace("+", "");
                    newName = newName.trim();
                    newName = newName.replace(/ /g, delimiter);
                    // console.log("Name with delimeter " + delimiter + " is " + newName);
                    if (imageSearch) {
                        newName = "%22" + newName + "%22" + delimiter + "XXX";
                    }

                    console.log("Name with delimiter is:" + newName);
                    return newName;
                }

            };

            self.StrSplit = function (nts) {
                if (gotPromise) {
                    var arr = self.actor.official_pages.split(',');
                    return (arr[nts]);
                }

            };

            self.isNotEmpty = function (fieldToCheck) {
                if (gotPromise) {

                    var ans = false;
                    // console.log("Actor-detail: isEmpty: fieldToCheck is" + fieldToCheck + "self.actor.fieldToCheck != undefined  is" + self.actor.fieldToCheck != undefined  )
                    //    if (self.actor.fieldToCheck != undefined || self.actor.fieldToCheck != null) {
                    if (self.actor.fieldToCheck.length > 0) {
                        ans = true;
                    }
                    //     }
                    return ans;
                }


            };

            self.scrapeActor = function (scrapeSite) {

                return $http.get('scrape-actor/', {
                    params: {
                        actor: self.actor.id,
                        scrapeSite: scrapeSite,
                        force: self.forceScrape

                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    self.updateImage = false;
                    self.addAlert("Succesfully scraped: " + self.actor.name + " from " + scrapeSite, 'success', '5000');
                    self.getActor()
                    self.updateImage = true;
                }, function errorCallback(response) {
                    self.addAlert(scrapeSite + " could not find: " + self.actor.name + " - Try a different scraper or try looking manually! ", 'warning', '5000');
                    console.log(angular.toJson(response));
                });


            };


            self.ageYears = function (dateTime) { // Will return the correct age in years based on today's date
                var birthday = new Date(dateTime);
                var today = new Date();
                var age = ((today - birthday) / (31557600000));
                age = Math.floor( age );
                console.log("Actor Age:" + age);
                return age;
                };

            self.howOld = function (datetime) { // Deprecated. The previous function works,
                                                // this one will make an actor a year older already on New Years Day.
                var actorDob = new Date(datetime);
                var actorDobYear = actorDob.getFullYear();

                var dt = new Date();
                var nowYear = dt.getFullYear();

                // Display the month, day, and year. getMonth() returns a 0-based number.

                console.log("Actor Age:" + nowYear - actorDobYear);

                return (nowYear - actorDobYear);

            };

            self.heightConvertInches = function (val) {

                var totalInches = Math.round(val / 2.54);

                var inches = totalInches % 12;
                var feet = Math.floor(totalInches / 12);

                var ans = {'inches': inches, 'feet': feet};

                return (ans);

            };

            self.weightConvertPounds = function (val) {

                var pounds = Math.round(val * 2.2);

                return (pounds);

            };

        }
    ]
})
;
