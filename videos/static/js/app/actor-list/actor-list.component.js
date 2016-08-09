// Register `phoneList` component, along with its associated controller and template
angular.module('actorList').component('actorList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/actor-list/actor-list.template.html',
    bindings: {

        mainPage: '='

    },
    controller: ['$scope', 'Actor', 'pagerService', 'Scene', 'ActorTag', 'scopeWatchService','helperService',
        function ActorListController($scope, Actor, pagerService, Scene, ActorTag, scopeWatchService, helperService) {


            var self = this;

            self.actors = [];

            self.ordering = "name";
            self.pageType = 'Actor';




            self.nextPage = function (currentPage) {


                input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    actorTag: self.actorTag,
                    scene: self.scene,
                    searchTerm: self.searchTerm,
                    sortBy: self.sortBy,
                    isRunnerUp: self.runnerUp

                };


                self.actorsToadd = pagerService.getNextPage(input);

                    self.actorsToadd.$promise.then(function (res) {

                        // self.actorsToadd = res[0];

                        var paginationInfo = {
                            pageType: input.pageType,
                            pageInfo: res[1]
                        };

                        scopeWatchService.paginationInit(paginationInfo);

                        self.actors = helperService.resourceToArray(res[0]);


                    });


            };

            if (self.mainPage) {
                console.log("main page is true! + " + self.mainPage);
                self.actorsToadd = self.nextPage(0);
            }

            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType){
                    self.nextPage(pageInfo.page)
                }
            });

            $scope.$on("addActorToList", function (event, changedActor) {
                self.actors.push((changedActor));
            });

            $scope.$on("actorTagLoaded", function (event, loadedActorTag) {
                self.actors = [];
                self.actorTag = loadedActorTag;
                self.nextPage(0);
            });

            $scope.$on("sceneLoaded", function (event, scene) {

                self.actors = [];
                self.scene = scene;
                self.nextPage(0);

            });


            

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                self.actors = [];
                self.searchTerm = searchTerm;
                self.nextPage(0);

            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                console.log("Sort Order Changed!");
                self.actors = [];
                self.sortBy = sortOrder;
                self.nextPage(0);
            });

            $scope.$on("runnerUpChanged", function (event, runnerUp) {
                console.log("Sort Order Changed!");
                self.scenes = [];
                self.runnerUp = runnerUp;


                self.nextPage(0);
            });

            self.removeActorFromScene = function (actorToRemove) {
                console.log("actor-list: function removeActorFromScene was triggered");
                if (angular.isObject(self.scene)) {
                    // self.pk.splice(self.pk.indexOf(aliasToDelete.id), 1);
                    // alert(angular.toJson(self.actor.actor_tags));
                    // alert(angular.toJson(tagToDelete));
                    // alert(angular.toJson(self.actor.actor_tags.indexOf(tagToDelete.id)));
                    var resId = [];
                    var resObj = [];

                    for (var i = 0; i < self.actors.length; i++) {
                        if (self.actors[i].id != actorToRemove.id) {
                            resId.push(self.actors[i].id);
                            resObj.push(self.actors[i]);
                        }
                    }


                    self.scene.actors = resId;

                    scopeWatchService.sceneChanged(self.scene);

                    self.actors = resObj;
                    // self.pk = res;


                    // self.actor.actor_tags.splice(self.actor.actor_tags.indexOf(tagToDelete.id,1));
                    // alert(angular.toJson(self.actor.actor_tags));
                }
            };
            
            self.deleteActor = function (actorToRemove) {
                Actor.remove({actorId: actorToRemove.id});

                var resId = [];
                    var resObj = [];

                    for (var i = 0; i < self.actors.length; i++) {
                        if (self.actors[i].id != actorToRemove.id) {
                            resId.push(self.actors[i].id);
                            resObj.push(self.actors[i]);
                        }
                    }


                    // self.scene.actors = resId;

                    // scopeWatchService.sceneChanged(self.scene);

                    self.actors = resObj;
            }

        }
    ]
});