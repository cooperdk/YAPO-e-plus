angular.module('dbFolderTree').component('dbFolderTree', {
    templateUrl: 'static/js/app/db-folder-tree/db-folder-tree.template.html',
    bindings: {
        // parent: '=',
        route: '=',
        mainPage: '='
    },
    controller: ['$scope', '$routeParams', 'DbFolder', '$rootScope', 'scopeWatchService', 'helperService','pagerService',
        function DbFolderTreeController($scope, $routeParams, DbFolder, $rootScope, scopeWatchService, helperService, pagerService) {
            var self = this;
            var redirectedFromNav = false;
            $rootScope.title = "Folders";
            self.currentDir;
            self.pageType = 'DbFolder';
            self.nav = [];
            self.recursive = false;
            // self.parent = 0;

            self.routParam = $routeParams.parentId;
            
            self.nextPage = function (currentPage) {


                input = {
                    currentPage: currentPage,
                    pageType: self.pageType,
                    parent: self.parentFolder,
                    searchTerm: self.searchTerm,
                    searchField: self.searchField,
                    sortBy: self.sortBy,
                    isRunnerUp: self.runnerUp

                };


                self.actorsToadd = pagerService.getNextPage(input);

                    self.actorsToadd.$promise.then(function (res) {

                        // self.actorsToadd = res[0];

                        var paginationInfo = {
                            pageType: input.pageType,
                            pageInfo: res[1]
                        };

                        scopeWatchService.paginationInit(paginationInfo);

                        self.dbFolders = helperService.resourceToArray(res[0]);


                    });


            };

            $scope.$on("searchTermChanged", function (event, searchTerm) {
                if (searchTerm['sectionType'] == 'DbFolder'){
                    self.dbFolders = [];
                    self.searchTerm = searchTerm['searchTerm'];
                    self.searchField = searchTerm['searchField'];
                    self.nextPage(0);
                }


            });

            $scope.$on("sortOrderChanged", function (event, sortOrder) {
                if (sortOrder['sectionType'] == 'DbFolder'){
                    console.log("Sort Order Changed!");
                    self.dbFolders = [];
                    self.sortBy = sortOrder['sortBy'];
                    self.nextPage(0);
                }

            });

            $scope.$on("runnerUpChanged", function (event, runnerUp) {
                if (runnerUp['sectionType'] == 'DbFolder') {
                    console.log("Sort Order Changed!");
                    self.dbFolders = [];
                    self.runnerUp = runnerUp['runnerUp'];
                    self.nextPage(0);
                }
            });


            $scope.$on("paginationChange", function (event, pageInfo) {
                if (pageInfo.pageType == self.pageType){
                    self.nextPage(pageInfo.page)
                }
            });
            self.appendFolders = function (clickedFolder) {
                // alert(clickedFolder)
                self.currentDir = clickedFolder;
                self.parentFolder = clickedFolder;
                // alert(this.dbFolders.toString())
                self.dbFoldersToAppend = [];
                self.nextPage(0);
                
                // self.dbFoldersToAppend = DbFolder.query({
                //     parent: clickedFolder.id, offset: '0',
                //     limit: '100'
                // });
                //
                // self.dbFoldersToAppend.$promise.then(function (result) {
                //
                //     self.dbFoldersToAppend = helperService.resourceToArray(result[0]);
                //
                //
                //
                //     self.dbFolders = self.dbFoldersToAppend;
                //
                //
                // });


                scopeWatchService.folderOpened({'dir': self.currentDir, 'recursive':self.recursive});


            };
            
            self.recursiveToggle = function () {
                scopeWatchService.folderOpened({'dir': self.currentDir, 'recursive':self.recursive});
            };





            if (self.route != undefined) {
                var temp = DbFolder.query({
                    id: $routeParams.parentId, offset: '0',
                    limit: '100'
                });

                var currentFolder = undefined;
                var x = temp.$promise.then(function (res) {

                    // res is a 2d array. In the [0] is another array of the result folders,
                    // while [1] is header info from the request.
                    var currentFolder = res[0][0];
                    self.parentFolder = currentFolder;


                    for (var z in currentFolder.path_id) {
                        console.log("Name is: " + currentFolder.path_id[z].name);
                        console.log("id is: " + currentFolder.path_id[z].id);
                        var temp = {
                            'last_folder_name_only': currentFolder.path_id[z].name,
                            'id': currentFolder.path_id[z].id
                        };
                        self.nav.push(temp)
                    }

                    self.appendFolders(currentFolder);


                })


            } else {

                self.dbFolders = DbFolder.query({level: '0'}).$promise.then(function (res) {
                    self.dbFolders = helperService.resourceToArray(res[0]);


                    var paginationInfo = {
                        pageType: self.pageType,
                        pageInfo: res[1]
                    };

                    scopeWatchService.paginationInit(paginationInfo);


                });
            }


            //
            //     self.nav = []
            // } else {
            //     console.log("db-folder-tree: folder tree parent is " + $routeParams.parentId);
            //     self.dbFolders = self.dbFolders.concat(DbFolder.query({
            //         parent: $routeParams.parentId
            //     }));
            // }


            self.navClick = function (clickedFolder) {
                redirectedFromNav = true;
                console.log("Clicked item is: " + clickedFolder.last_folder_name_only);
                console.log("Nav length is: " + self.nav.length);
                var found = false;
                console.log("found is: " + found.toString());

                for (i = 0; i < self.nav.length; i++) {

                    if (found == true) {
                        console.log("Deleting item on index: " + i);
                        self.nav.splice(i, self.nav.length - i);
                        console.log("Nav length is: " + self.nav.length);
                    }

                    if (self.nav[i] === clickedFolder) {
                        console.log("found clicked itme on index " + i);
                        found = true;
                    }

                }

                self.appendFolders(clickedFolder);
            };

            self.getDirs = function () {
                if (self.currentDir == undefined) {
                    return false;
                } else if (self.currentDir.scenes.length == 0) {
                    return false;

                } else {


                    console.log('%c currentDir is not undefined or empty it is ' + angular.toJson(self.currentDir), 'background: #232; color: #bada55'
                    );

                    scopeWatchService.folderOpened(self.currentDir);
                    return true;
                }
            };


        }
    ]
});