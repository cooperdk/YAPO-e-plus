angular.module('actorTagDetail').component('actorTagDetail', {
    templateUrl: 'static/js/app/actor-tag-detail/actor-tag-detail.template.html',
    controller: ['$routeParams', 'ActorTag', '$rootScope', 'scopeWatchService', '$http', '$scope',
        function ActorTagDetailController($routeParams, ActorTag, $rootScope, scopeWatchService, $http, $scope) {
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
            self.actorTag = ActorTag.get({actorTagId: $routeParams.actorTagId});

            self.actorTag.$promise.then(function (result) {

                self.actorPks = result.actors.toString();

                scopeWatchService.actorTagLoaded(result);
                
                $rootScope.title = result.name;
                gotPromise = true;

                // alert(self.actorPks)
            });

                self.getCurrentTag = function () {
                self.actorTag = ActorTag.get({actorTagId: $routeParams.actorTagId}).$promise.then(function (res) {
                    self.currentTag = res.id;
                    console.log("ActorTag detail: current id is " + angular.toJson(self.currentTag));
                    self.actorTag = res;
                    gotPromise = true;
                    scopeWatchService.actorTagLoaded(res);

                });

            };

             $scope.$on("didActorTagLoad", function (event, scene) {

                if (gotPromise){
                    scopeWatchService.actorTagLoaded(self.actorTag)
                }

            });

             self.scanTag = function () {
                console.log('Scanning actor tag ID '+self.actorTag.id);
                console.log('Force: '+self.forceScan);
                return $http.get('get-tag/', {
                    params: {
                        tag_id: self.actorTag.id,
                        tag_type: 'ActorTag',
                        force: self.forceScan
                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    self.addAlert(response.data, 'success', '3000');
                    self.getCurrentTag()
                }, function errorCallback(response) {
                    self.addAlert(response.data, 'warning', '20000');
                    console.log(angular.toJson(response))
                });
            };


            self.update = function () {
                ActorTag.update({actorTagId: self.actorTag.id}, self.actorTag)
            };

        }
    ]
});