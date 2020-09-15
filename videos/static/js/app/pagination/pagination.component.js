angular.module('pagination').component('pagination', {
    templateUrl: 'static/js/app/pagination/pagination.template.html',
    bindings: {
        pageType: '='
    },
    controller: ['$routeParams', 'log', 'Scene', 'helperService', '$scope', 'SceneTag', 'Actor', 'Website', '$http', '$rootScope', 'scopeWatchService',
        function PaginationController($routeParams, log, Scene, helperService, $scope, SceneTag, Actor, Website,  $http, $rootScope, scopeWatchService) {
            var self = this;

            if (helperService.getNumberOfItemsPerPage() == undefined) {
                self.itemsPerPage = 50;
                helperService.setNumberOfItemsPerPage(self.itemsPerPage)
            } else {
                self.itemsPerPage = helperService.getNumberOfItemsPerPage()
            }

            self.bigCurrentPage = "";
            self.maxSize = "";
            self.totalItems = "";
            self.onePageOnly = true;

            self.pageChange = function () {
                var ans = {
                    pageType: this.pageType,
                    page: self.bigCurrentPage
                };
                scopeWatchService.paginationChange(ans);
            };


            function getMaxPageFromLinkHeader(linkHeader) {
                self.totalItems = parseInt(linkHeader.replace(/.*<(\d+)>; rel="count".*/, '$1'));
            }


            $scope.$on("paginationInit", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType) {
                    if (pageInfo.pageInfo != '-6') {
                        self.onePageOnly = false;
                        getMaxPageFromLinkHeader(pageInfo.pageInfo);
                    } else {
                        self.onePageOnly = true;
                    }
                }
            });

        }]
});
