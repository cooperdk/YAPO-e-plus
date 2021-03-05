angular.module('sceneTagDetail').component('sceneTagDetail', {
    templateUrl: 'static/js/app/scene-tag-detail/scene-tag-detail.template.html',
    controller: ['$routeParams', 'SceneTag', 'scopeWatchService', '$rootScope', '$http', '$scope',
        function SceneTagDetailController($routeParams, SceneTag, scopeWatchService, $rootScope, $http, $scope) {
            var self = this;
            var gotPromise = false;
            self.forceScan = false;
            self.alerts = [];
            self.addAlert = function (msg, type, timeout) {
                self.alerts.push({msg: msg, type: type, timeout: timeout});
            };

            self.closeAlert = function (index) {
                self.alerts.splice(index, 1);
            };

            self.sceneTag = SceneTag.get({sceneTagId: $routeParams.sceneTagId}).$promise.then(function (res) {
                scopeWatchService.sceneTagLoaded(res);
                self.sceneTag = res;
                // alert(res.name);
                $rootScope.title = res.name;
                gotPromise = true
            });

                self.getCurrentTag = function () {
                self.sceneTag = SceneTag.get({sceneTagId: $routeParams.sceneTagId}).$promise.then(function (res) {
                    self.currentTag = res.id;
                    console.log("SceneTag detail: current id is " + angular.toJson(self.currentTag));
                    self.sceneTag = res;
                    gotPromise = true;
                    scopeWatchService.sceneTagLoaded(res);

                });
                };

            $scope.$on("didSceneTagLoad", function (event, sceneTag) {
                if (gotPromise){
                    scopeWatchService.sceneTagLoaded(self.sceneTag);
                }
            });


            self.scanTag = function () {
            console.log('Scanning scene tag ID '+self.sceneTag.id);
            console.log('Force: '+self.forceScan);
            return $http.get('get-tag/', {
                params: {
                    tag_id: self.sceneTag.id,
                    tag_type: 'SceneTag',
                    force: self.forceScan

                }
            }).then(function (response) {
                // alert(angular.toJson(response))
                self.addAlert(response.data, 'success', '3000');
                self.getCurrentTag()
            }, function errorCallback(response) {
                self.addAlert(response.data, 'warning', '10000');
                console.log(angular.toJson(response))
            });
        };


            self.update = function () {
              SceneTag.update({sceneTagId: self.sceneTag.id}, self.sceneTag)
            }

        }
    ]
});