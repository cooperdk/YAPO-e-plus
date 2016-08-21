angular.module('websiteDetail').component('websiteDetail', {
    templateUrl: 'static/js/app/website-detail/website-detail.template.html',
    controller: ['$routeParams', 'Website', 'scopeWatchService', '$rootScope','$scope',
        function WebsiteDetailController($routeParams, Website, scopeWatchService, $rootScope, $scope) {
            var self = this;
            var gotPromise = false;
            self.website = Website.get({websiteId: $routeParams.websiteId}).$promise.then(function (res) {

                scopeWatchService.websiteLoaded(res);
                self.website = res;
                // alert(res.name);
                $rootScope.title = res.name;
                gotPromise = true;
            });

            $scope.$on("didWebsiteLoad", function (event, website) {
                if (gotPromise){
                    scopeWatchService.websiteLoaded(self.website);
                }
            });

        }
    ]
});