angular.module('dbFolderTree').component('dbFolderTree', {
    templateUrl: 'static/js/app/db-folder-tree/db-folder-tree.template.html',
    bindings: {
        parent: '=',
        currentDirId: '='
    },
    controller: ['$scope', '$routeParams', 'DbFolder', '$rootScope', 'scopeWatchService', 'helperService',
        function DbFolderTreeController($scope, $routeParams, DbFolder, $rootScope, scopeWatchService, helperService) {
            var self = this;
            var redirectedFromNav = false;
            $rootScope.title = "Folders";
            self.currentDir;
            self.pageType = 'DbFolder';

            self.routParam = $routeParams.parentId;


            if ($routeParams.parentId != undefined) {
                self.dbFolders = DbFolder.query({
                    id: $routeParams.parentId, offset: '0',
                    limit: '100'
                });

                var x = self.dbFolders.$promise.then(function (res) {


                    var y = res[0];


                    for (var z in y[0].path_id) {
                        console.log("Name is: " + y[0].path_id[z].name);
                        console.log("id is: " + y[0].path_id[z].id);
                        var temp = {'last_folder_name_only': y[0].path_id[z].name, 'id': y[0].path_id[z].id};
                        self.nav.push(temp)
                    }


                })
            }
            //     // alert("Route Params are:" + $routeParams.parentId);
            //
            //     scopeWatchService.folderOpened($routeParams.parentId);
            //
            //
            // } else {
            if (angular.isUndefined(this.parent)) {
                // alert("Parent is undefined")
                // self.dbFolders = DbFolder.query({level: '0'});
                self.dbFolders = DbFolder.query({level: '0'}).$promise.then(function (res) {
                    self.dbFolders = helperService.resourceToArray(res[0]);


                    // self.actorsToadd = res[0];

                    var paginationInfo = {
                        pageType: self.pageType,
                        pageInfo: res[1]
                    };

                    scopeWatchService.paginationInit(paginationInfo);


                });


                //self.actors = Actor.query({pk: self.pk.toString()});
                // this.orderProp = 'level';
                self.nav = []
            } else {
                console.log("db-folder-tree: folder tree parent is " + $routeParams.parentId);
                self.dbFolders = self.dbFolders.concat(DbFolder.query({
                    parent: $routeParams.parentId
                }));
            }
            // }

            self.appendFolders = function (clickedFolder) {
                // alert(clickedFolder)
                self.currentDir = clickedFolder;
                // alert(this.dbFolders.toString())
                self.dbFoldersToAppend = [];
                self.dbFoldersToAppend = DbFolder.query({
                    parent: clickedFolder.id, offset: '0',
                    limit: '100'
                });

                self.dbFoldersToAppend.$promise.then(function (result) {

                    self.dbFoldersToAppend = helperService.resourceToArray(result[0]);

                    // alert(self.dbFoldersToAppend)
                    if (redirectedFromNav == false) {
                        self.nav.push(clickedFolder)
                    }
                    redirectedFromNav = false;

                    // self.dbFolders = self.dbFolders.concat(self.dbFoldersToAppend)

                    self.dbFolders = self.dbFoldersToAppend;

                    // alert(self.dbFolders.toString())
                });

                // scopeWatchService.folderOpened(self.currentDir);
                scopeWatchService.folderOpened(self.currentDir);


            };


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