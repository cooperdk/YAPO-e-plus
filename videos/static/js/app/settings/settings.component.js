angular.module('settings').component('settings', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/settings/settings.template.html',
        controller: ['$scope', '$rootScope', 'scopeWatchService', '$http','helperService',
            function SettingsController($scope, $rootScope, scopeWatchService, $http, helperService) {

                var self = this;
                self.response = "";
                //self.ignore_last_lookup = true;

                // self.pathToVLC = "";

                self.itemsPerPage = 50;
                self.mediaRootFolders = null;
                self.forceScrape = false;
                self.alerts = [];
                self.addAlert = function (msg, type, timeout) {
                    self.alerts.push({msg: msg, type: type, timeout: timeout});
                };

                self.closeAlert = function (index) {
                    self.alerts.splice(index, 1);
                };
                
                var x = helperService.getNumberOfItemsPerPaige();
                if (helperService.getNumberOfItemsPerPaige() != undefined){
                    self.itemsPerPage = helperService.getNumberOfItemsPerPaige()
                }
                
                self.changeNumberOfItemsPerPage = function () {
                    helperService.setNumberOfItemsPerPaige(self.itemsPerPage);
					self.addAlert("OK. changing items per page to "+self.itemsPerPage+".", 'success', '3000');
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
						self.addAlert("OK.", 'success', '3000');
                    }, function errorCallback(response) {
                        self.addAlert("Please check that program location.", 'warning', '1000000');
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
						//alert("Done checking for dupes, check the console.");
						self.addAlert("Done checking for duplicate files.", 'success', '10000');
                    }, function errorCallback(response) {
                        //alert("Something went wrong!");
						self.addAlert("Something went wrong while checking for dupes!", 'warning', '10000');
                    });
			}
                };
                
                self.scrapAllActor = function () {
                    if (confirm("Are you sure? This may take a long time. The process can only be interrupted by force quitting YAPO.")) {
                       self.addAlert("Starting scrape, please hold on...", 'success', '5000');
                        $http.get('settings/', {
                            params: {
                                scrapAllActors: 'True',
                                force: self.forceScrape
                            }

                    }   ).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                        //self.addAlert("Done scraping actors.", 'success', '10000');
                        }, function errorCallback(response) {
                        self.addAlert("Something went wrong.", 'warning', '1000000');
                        });
                    }
                };
                
                
                self.tagAllScenes = function () {

                    if (confirm("Are you sure? This may take a long time. The process can only be interrupted by force quitting YAPO.")) {
                        self.addAlert("Beginning tagging ... this may take some time, check the console.", 'success', '5000');
                        $http.get('settings/', {
                            params: {
                                tagAllScenes: 'True',
                                ignore_last_lookup: 'False'
                            }

                        }).then(function (response) {
                            // alert(angular.toJson(response));
                            // self.response = response.data.vlc_path;
                            // self.pathToVLC = response.data.vlc_path;
                            // alert("Got response from server: " + self.pathToFolderToAdd);
                            //self.addAlert("Done tagging scenes.", 'success', '10000');
                        }, function errorCallback(response) {
                            self.addAlert("Something went wrong.", 'warning', '1000000');
                        });
                    }
                };
                
                self.tagAllScenesIgnore = function () {
			    if (confirm("Are you sure? This may take a long time. The process can only be interrupted by force quitting YAPO."))		{
                    $http.get('settings/', {
                        params: {
                            tagAllScenesIgnore: 'True',
                            ignore_last_lookup: 'True'
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
                    }, function errorCallback(response) {
                        self.addAlert("Something went wrong.", 'warning', '1000000');
                    });
                }  
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
						self.addAlert("Done cleaning the system.", 'success', '10000');
                    }, function errorCallback(response) {
                        self.addAlert("Something went wrong while cleaning the system.", 'warning', '1000000');
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
						self.addAlert("Folder deleted.", 'success', '4000');
                    }, function errorCallback(response) {
                        //alert("Something went wrong!" + angular.toJson(response));
						self.addAlert("Something went wrong while removing the folder.", 'danger', '1000000');
                    });
                    
                    
                };
                
                
                self.rescanFolders = function (folder) {

                    if (folder != ''){
                        folder = folder.id
						
                    }
                    self.addAlert("Beginning scan...", 'success', '3000');
                    $http.get('settings/', {
                        params: {
                            folderToScan: folder
                            
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        // self.response = response.data.vlc_path;
                        // self.pathToVLC = response.data.vlc_path;
                        // alert("Got response from server: " + self.pathToFolderToAdd);
						self.addAlert("Scanning complete.", 'success', '10000');
                    }, function errorCallback(response) {
                        self.addAlert("Something went wrong while scanning.", 'warning', '1000000');
                    });
                    
                }
                


            }
        ]
    }
);