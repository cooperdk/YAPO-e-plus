// Register `phoneList` component, along with its associated controller and template
angular.module('actorList').component('actorList', {
    // Note: The URL is relative to our `index.html` file
    bindings: {

        mainPage: '='

    },
    templateUrl:   ['$element', '$attrs', function($element, $attrs) {


        if ($attrs.sceneDetail == 'true'){
           return 'static/js/app/actor-list/actor-list-row.template.html'
        }else{
            return 'static/js/app/actor-list/actor-list.template.html'    
        }

        
    } ],

    controller: ['$scope', 'Actor', 'pagerService', 'Scene', 'ActorTag', 'scopeWatchService','helperService',
        function ActorListController($scope, Actor, pagerService, Scene, ActorTag, scopeWatchService, helperService) {


            var self = this;
            
            var didSceneLoad = false;



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
                    searchField: self.searchField,
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
                didSceneLoad = true;

            });
            
            if (!didSceneLoad){
                scopeWatchService.didSceneLoad('a')
            }


            

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                if (searchTerm['sectionType'] == 'ActorList'){
                    self.actors = [];
                    self.searchTerm = searchTerm['searchTerm'];
                    self.searchField = searchTerm['searchField'];
                    self.nextPage(0);    
                }


            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                if (sortOrder['sectionType'] == 'ActorList'){
                    console.log("Sort Order Changed!");
                    self.actors = [];
                    self.sortBy = sortOrder['sortBy'];
                    self.nextPage(0);
                }

            });

            $scope.$on("runnerUpChanged", function (event, runnerUp) {
                if (runnerUp['sectionType'] == 'ActorList'){
                    console.log("Sort Order Changed!");
                    self.actors = [];
                    self.runnerUp = runnerUp['runnerUp'];
                    self.nextPage(0);    
                }
                
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
            };
            
            self.patchActor =function (actorToPatch, patchInfo) {
                
                 Actor.patch({actorId: actorToPatch.id}, patchInfo)
            };
            
            self.setRating = function (actor) {
              var patchInfo = {'rating': actor.rating};
                
                self.patchActor(actor,patchInfo)
                
            };
            
            self.toggleRunnerUp = function (actor) {
              var patchInfo = {'is_runner_up': actor.is_runner_up};
                
                self.patchActor(actor,patchInfo)
                
            };



        }

    ]
});