angular.module('actorTagDetail').component('actorTagDetail', {
    templateUrl: 'static/js/app/actor-tag-detail/actor-tag-detail.template.html',
    controller: ['$routeParams', 'ActorTag', '$rootScope', 'scopeWatchService', '$scope',
        function ActorTagDetailController($routeParams, ActorTag, $rootScope, scopeWatchService, $scope) {
            var self = this;
            var gotPromise = false;

            self.actorTag = ActorTag.get({actorTagId: $routeParams.actorTagId});

            self.actorTag.$promise.then(function (result) {

                self.actorPks = result.actors.toString();

                scopeWatchService.actorTagLoaded(result);
                
                $rootScope.title = result.name;
                gotPromise = true;

                // alert(self.actorPks)
            });

             $scope.$on("didSceneLoad", function (event, scene) {

                if (gotPromise){
                    scopeWatchService.actorTagLoaded(self.actorTag)
                }

            });

        }
    ]
});