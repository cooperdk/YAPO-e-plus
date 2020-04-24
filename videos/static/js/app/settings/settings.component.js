angular.module('settings').component('settings', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/settings/settings.template.html',
        controller: ['$scope', '$rootScope', 'scopeWatchService', '$http','helperService',
            function SettingsController($scope, $rootScope, scopeWatchService, $http, helperService) {

                var self = this;
                self.response = "";
                self.ignore_last_lookup = false;

                // self.pathToVLC = "";

                self.itemsPerPage = 50;
                self.mediaRootFolders = null;

                
                var x = helperService.getNumberOfItemsPerPaige();
                if (helperService.getNumberOfItemsPerPaige() != undefined){
                    self.itemsPerPage = helperService.getNumberOfItemsPerPaige()
                }
                
                self.changeNumberOfItemsPerPage = function () {
                    helperService.setNumberOfItemsPerPaige(self.itemsPerPage);
                    // scopeWatchService.numberOfItemsPerPageChanged('a');
                };
                
                
                self.settings = $http.get('settings/', {
                    params: {
                            pathToVlc: ""
                        }
                }).then(function (response) {
                    // alert(angular.toJson(response));
                    self.response = response.data.vlc_path;
                    self.pathToVLC = response.data.vlc_path;
                    // alert("Got response from server: " + self.pathToFolderToAdd);
                }, function errorCallback(response) {
                    alert("Something went wrong!");
                });


                self.updateVlcPath = function () {

                    $http.get('settings/', {
                        params: {
                            pathToVlc: self.pathToVLC
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        self.response = response.data.vlc_path;
                        self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!");
                    });
                };


            self.checkDupe = function () {
 
            if (confirm("Are you sure? Any identical copies of your videos will be removed, leaving only one copy."))		{
                        $http.get('settings/', {
                        params: {
                            checkDupes: 'True'
                        }

			        }).then(function (response) {

                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
						alert("Done checking for dupes, check the console.");
                    }, function errorCallback(response) {
                        alert("Something went wrong!");
                    });
			}
                };
                
                self.scrapAllActor = function () {
                     $http.get('settings/', {
                        params: {
                            scrapAllActors: 'True'
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!");
                    });
                };
                
                
                self.tagAllScenes = function () {
                    $http.get('settings/', {
                        params: {
                            tagAllScenes: 'True',
                            ignoreLastLookup: self.ignore_last_lookup
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!");
                    });
                    
                };
                
				
                self.cleanDatabase = function () {
                    $http.get('settings/', {
                        params: {
                            cleanDatabase: true
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!" + angular.toJson(response));
                    });
                    
                };
                
                
                var getRootMediaPaths = function () {
                    $http.get('/api/folder-local/', {
                    }).then(function (response) {

                        self.mediaRootFolders = response.data;
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!" + angular.toJson(response));
                    });
                };

                getRootMediaPaths();
                
                
                self.removeFolderFromList = function (folder) {
                    
                    var index = helperService.getObjectIndexFromArrayOfObjects(folder,self.mediaRootFolders);
                    
                    if (index != null){
                        self.mediaRootFolders.splice(index,1);    
                    }

                    $http.delete('/api/folder-local/' + folder.id, {
                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!" + angular.toJson(response));
                    });
                    
                    
                };
                
                
                self.rescanFolders = function (folder) {

                    if (folder != ''){
                        folder = folder.id
                    }

                    $http.get('settings/', {
                        params: {
                            folderToScan: folder
                            
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        alert("Something went wrong!" + angular.toJson(response));
                    });
                    
                }
                


            }
        ]
    }
);