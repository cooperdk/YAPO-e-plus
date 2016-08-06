angular.module('pagination').component('pagination', {
    templateUrl: 'static/js/app/pagination/pagination.template.html',
    bindings: {
        pageType: '='
    },
    controller: ['$routeParams', 'Scene', 'helperService', '$scope', 'SceneTag', 'Actor', 'Website', '$http', '$rootScope', 'scopeWatchService',
        function PaginationController($routeParams, Scene, helperService, $scope, SceneTag, Actor, Website, $http, $rootScope, scopeWatchService) {

            var self = this;


            self.itemsPerPage = 50;
            self.bigCurrentPage = "";
            self.maxSize = "";
            self.totalItems = "";
            self.onePageOnly = true;


            self.pageChange = function () {
                // alert(self.bigCurrentPage);


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