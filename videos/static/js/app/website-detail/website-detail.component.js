angular.module('websiteDetail').component('websiteDetail', {
    templateUrl: 'static/js/app/website-detail/website-detail.template.html',
    controller: ['$routeParams', 'Website', 'scopeWatchService', '$rootScope', '$scope',
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
                if (gotPromise) {
                    scopeWatchService.websiteLoaded(self.website);
                }
            });


            self.modifyWebsiteAlias = function (website) {

                var patchContent = {'website_alias': website.website_alias};
                alert(angular.toJson(patchContent));
                patchWebsite(website, patchContent)


            };

            var patchWebsite = function (website_to_patch, patchContent) {
                Website.patch({websiteId: website_to_patch.id}, patchContent)
            };
            
            self.update = function () {
              Website.update({websiteId: self.website.id}, self.website)
            }

        }
    ]
});