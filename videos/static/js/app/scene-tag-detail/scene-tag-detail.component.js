angular.module('sceneTagDetail').component('sceneTagDetail', {
    templateUrl: 'static/js/app/scene-tag-detail/scene-tag-detail.template.html',
    controller: ['$routeParams', 'SceneTag', 'scopeWatchService', '$rootScope',
        function SceneTagDetailController($routeParams, SceneTag, scopeWatchService, $rootScope) {
            var self = this;

            self.sceneTag = SceneTag.get({sceneTagId: $routeParams.sceneTagId}).$promise.then(function (res) {
                scopeWatchService.sceneTagLoaded(res);
                self.sceneTag = res;
                // alert(res.name);
                $rootScope.title = res.name
            })

        }
    ]
});