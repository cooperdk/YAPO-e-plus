// Register `phoneList` component, along with its associated controller and template
angular.module('websiteList').component('websiteList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/website-list/website-list.template.html',
    bindings: {
        mainPage: '='
    },
    controller: ['Website', '$scope', 'pagerService', 'scopeWatchService', 'helperService',

        function websiteListController(Website, $scope, pagerService, scopeWatchService, helperService) {
            // this.websites = Website.query();
            // this.orderProp = 'name';


            var self = this;
            var didSectionListWrapperLoad = false;
            self.pageType = 'Website';


            self.nextPage = function (currentPage) {


                var input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    scene: self.scene,
                    searchTerm: self.searchTerm,
                    searchField: self.searchField,
                    sortBy: self.sortBy
                };

                self.actorsToadd = pagerService.getNextPage(input);
                if (self.actorsToadd != undefined) {
                    self.actorsToadd.$promise.then(function (res) {

                        // self.actorsToadd = res[0];

                        var paginationInfo = {
                            pageType: input.pageType,
                            pageInfo: res[1]
                        };

                        scopeWatchService.paginationInit(paginationInfo);

                        self.websites = helperService.resourceToArray(res[0]);


                    });
                }

            };


            // if (self.mainPage) {
            //     console.log("main page is true! + " + self.mainPage);
            //     self.nextPage(0);
            // }

            $scope.$on("sceneLoaded", function (event, scene) {
                self.scene = scene;
                self.nextPage(0);


            });

            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType){
                    self.nextPage(pageInfo.page)
                }
            });

            $scope.$on("addWebsiteToList", function (event, website) {
                self.websites.push(website)


            });

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                if (searchTerm['sectionType'] == 'WebsiteList'){
                    self.websites = [];
                    self.searchTerm = searchTerm['searchTerm'];
                    self.searchField = searchTerm['searchField'];
                    self.nextPage(0);    
                }
                


            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                if (sortOrder['sectionType'] == 'WebsiteList'){
                    console.log("Sort Order Changed!");
                    self.websites = [];
                    self.sortBy = sortOrder['sortBy'];
                    if (sortOrder.mainPage == undefined || sortOrder.mainPage == true ) {
                        self.nextPage(0);
                    }
                    didSectionListWrapperLoad = true;
                }

            });

            if (!didSectionListWrapperLoad) {
                scopeWatchService.didSectionListWrapperLoaded('WebsiteList')
            }


            self.removeWebsiteFromScene = function (siteToDelete) {
                if (angular.isObject(self.scene)) {
                    // self.pk.splice(self.pk.indexOf(aliasToDelete.id), 1);
                    // alert(angular.toJson(self.actor.actor_tags));
                    // alert(angular.toJson(tagToDelete));
                    // alert(angular.toJson(self.actor.actor_tags.indexOf(tagToDelete.id)));
                    var res = helperService.removeObjectFromArrayOfObjects(siteToDelete, self.websites);
                    
                    self.scene.websites = res['resId'];
                    self.websites = res['resObject'];

                    scopeWatchService.sceneChanged(self.scene);

                    // self.actor.actor_tags.splice(self.actor.actor_tags.indexOf(tagToDelete.id,1));
                    // alert(angular.toJson(self.actor.actor_tags));
                }
            };
            
            self.deleteWebsiteFromDb = function (siteToDelete) {
                
                Website.remove({websiteId: siteToDelete.id});

                var ans = helperService.removeObjectFromArrayOfObjects(siteToDelete,self.websites);

                self.websites = ans['resObject'];
                
            }

        }
    ]
});