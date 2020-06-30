// Register `phoneList` component, along with its associated controller and template
angular.module('actorAliasList').component('actorAliasList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/actor-alias-list/actor-alias-list.template.html',
    bindings: {
        pk: '='
    },
    controller: ['$scope', 'ActorAlias', 'pagerService', 'scopeWatchService', 'helperService',
        function ActorAliasListController($scope, ActorAlias, pagerService, scopeWatchService, helperService) {
            var self = this;
            var counter = 0;
            // self.aliases = [];
            self.pageType = 'ActorAlias';


            self.nextPage = function (currentPage) {


                var input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    actor: self.actor


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

                        self.aliases = helperService.resourceToArray(res[0]);


                    });
                }

            };


            $scope.$on("actorLoaded", function (event, actor) {
                self.actor = actor;
                self.nextPage(0);


            });

            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType) {
                    self.nextPage(pageInfo.page)
                }


            });


            $scope.$on("addAliasToList", function (event, alias) {
                self.aliases.push(alias);

            });


            self.deleteAlias = function (aliasToDelete) {
                // alert(aliasToDelete.id +  aliasToDelete.name)

                // alert(self.pk.indexOf(aliasToDelete.id));
                // console.log("actor-alias-list.componenet: newValue is: "  + )
                ActorAlias.remove({actorAliasId: aliasToDelete.id});

                var resId = [];
                var resObjects = [];

                for (var i = 0; i < self.aliases.length; i++) {
                    if (self.aliases[i].id != aliasToDelete.id) {

                        resId.push(self.aliases[i].id);
                        resObjects.push(self.aliases[i]);


                    }
                }

                self.aliases = resObjects;


            };
            self.isOneWord = function (alias) {

                return !(alias.name.indexOf(' ') > -1)

            };

            self.updateActorAlias = function (object) {

                //
                // var id = object.id + '/';
                // alert(id);

                ActorAlias.update({actorAliasId: object.id}, object);
                // return alert(object.id + ' ' + object.name + ' input: ' + input);
            };
        }
    ]
});