angular.module('actorTagDetail').component('actorTagDetail', {
    templateUrl: 'static/js/app/actor-tag-detail/actor-tag-detail.template.html',
    controller: ['$routeParams', 'ActorTag', '$rootScope', 'scopeWatchService',
        function ActorTagDetailController($routeParams, ActorTag, $rootScope, scopeWatchService) {
            var self = this;

            self.actorTag = ActorTag.get({actorTagId: $routeParams.actorTagId});

            self.actorTag.$promise.then(function (result) {

                self.actorPks = result.actors.toString();

                scopeWatchService.actorTagLoaded(result);
                
                $rootScope.title = result.name;

                // alert(self.actorPks)
            })

        }
    ]
});