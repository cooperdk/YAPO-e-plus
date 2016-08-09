angular.module('websiteDetail').component('websiteDetail', {
    templateUrl: 'static/js/app/website-detail/website-detail.template.html',
    controller: ['$routeParams', 'Website', 'scopeWatchService', '$rootScope',
        function WebsiteDetailController($routeParams, Website, scopeWatchService, $rootScope) {
            var self = this;
            self.website = Website.get({websiteId: $routeParams.websiteId}).$promise.then(function (res) {

                scopeWatchService.websiteLoaded(res);
                self.website = res;
                // alert(res.name);
                $rootScope.title = res.name;
            })

        }
    ]
});