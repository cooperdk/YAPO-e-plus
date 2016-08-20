// Register `phoneList` component, along with its associated controller and template
angular.module('actorTagList').component('actorTagList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/actor-tag-list/actor-tag-list.template.html',
    bindings: {
        mainPage: '='
    },
    controller: ['$scope', 'ActorTag', 'pagerService', 'scopeWatchService','helperService',
        function ActorTagListController($scope, ActorTag, pagerService, scopeWatchService, helperService) {

            // this.tags = ActorTag.query();


            var self = this;
            self.pageType = 'ActorTag';
            



            self.nextPage = function (currentPage) {


                var input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    actor: self.actor,
                    searchTerm: self.searchTerm,
                    searchField: self.searchField,
                    sortBy: self.sortBy
                };

                self.actorsToadd = pagerService.getNextPage(input);
                if (self.actorsToadd != undefined) {
                    self.actorsToadd.$promise.then(function (res) {

                        // self.actorsToadd = res[0];

                        var paginationInfo = {
                            pageType: input.pageType,
                            pageInfo: res[1]
                        };

                        scopeWatchService.paginationInit(paginationInfo);

                        self.tags = helperService.resourceToArray(res[0]);


                    });
                }

            };

            if (self.mainPage) {
                console.log("main page is true! + " + self.mainPage);
                self.nextPage(0);
            }


            $scope.$on("actorLoaded", function (event, actor) {
                self.actor = actor;

                self.nextPage(0);


            });

            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType){
                    self.nextPage(pageInfo.page)
                }


            });

            $scope.$on("addActorTagToList", function (event, actorTag) {
                self.tags.push(actorTag)


            });

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                if (searchTerm['sectionType'] == 'ActorTagList'){
                    self.tags = [];
                    self.searchTerm = searchTerm['searchTerm'];
                    self.searchField = searchTerm['searchField'];
                    self.nextPage(0);
                }

            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                if (sortOrder['sectionType'] == 'ActorTagList'){
                    console.log("Sort Order Changed!");
                    self.tags = [];
                    self.sortBy = sortOrder['sortBy'];
                    self.nextPage(0);
                }

            });


            self.deleteActorTag = function (tagToDelete) {

                if (angular.isObject(self.actor)) {
                    // self.pk.splice(self.pk.indexOf(aliasToDelete.id), 1);
                    // alert(angular.toJson(self.actor.actor_tags));
                    // alert(angular.toJson(tagToDelete));
                    // alert(angular.toJson(self.actor.actor_tags.indexOf(tagToDelete.id)));

                    var resId = [];
                    var resObject = [];
                    for (i = 0; i < self.tags.length; i++) {
                        if (self.tags[i].id != tagToDelete.id) {
                            resId.push(self.tags[i].id);
                            resObject.push(self.tags[i]);
                        }
                    }

                    self.actor.actor_tags = resId;


                    scopeWatchService.actorChaned(self.actor);

                    self.tags = resObject;


                    // self.actor.actor_tags.splice(self.actor.actor_tags.indexOf(tagToDelete.id,1));
                    // alert(angular.toJson(self.actor.actor_tags));
                }
            }
        }
    ]
});