angular.module('sceneTagDetail').component('sceneTagDetail', {
    templateUrl: 'static/js/app/scene-tag-detail/scene-tag-detail.template.html',
    controller: ['$routeParams', 'SceneTag', 'scopeWatchService', '$rootScope', '$scope',
        function SceneTagDetailController($routeParams, SceneTag, scopeWatchService, $rootScope, $scope) {
            var self = this;
            var gotPromise = false;
            self.sceneTag = SceneTag.get({sceneTagId: $routeParams.sceneTagId}).$promise.then(function (res) {
                scopeWatchService.sceneTagLoaded(res);
                self.sceneTag = res;
                // alert(res.name);
                $rootScope.title = res.name;
                gotPromise = true
            });

            $scope.$on("didSceneTagLoad", function (event, sceneTag) {
                if (gotPromise){
                    scopeWatchService.sceneTagLoaded(self.sceneTag);
                }
            });
            
            self.update = function () {
              SceneTag.update({sceneTagId: self.sceneTag.id}, self.sceneTag)
            }

        }
    ]
});