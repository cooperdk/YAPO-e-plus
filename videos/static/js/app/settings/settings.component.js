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
                //self.tpdb_enabled = false;
                //self.tpdb_website_logos = false;
                //self.tpdb_autorename = false;
                //self.tpdb_add_actors = false;
                //self.tpdb_add_photo = false;
                self.tpdb_force = false;
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
                            pathToVlc: "",
                            yapoURL: "",
                            tpdb_enabled: false,
                            tpdb_website_logos: false,
                            tpdb_autorename: false,
                            tpdb_actors: false,
                            tpdb_photos: false,
                            tpdb_websites: false,
                            tpdb_tags: 0
                        }
                }).then(function (response) {
                    //alert(angular.toJson(response));
                    //self.response = response.data.vlc_path;
                    self.pathToVLC = response.data.vlc_path;
                    self.yapoURL = response.data.yapo_url;
                    self.tpdb_enabled = response.data.tpdb_enabled;
                    self.tpdb_website_logos = response.data.tpdb_website_logos;
                    self.tpdb_autorename = response.data.tpdb_autorename;
                    self.tpdb_actors = response.data.tpdb_actors;
                    self.tpdb_photos = response.data.tpdb_photos;
                    self.tpdb_websites = response.data.tpdb_websites;
                    self.tpdb_tags = response.data.tpdb_tags;

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
                        self.addAlert('OK, the VLC path is now saved.', 'success', '3000');
                    }, function errorCallback(response) {
                        self.addAlert("There was an error changing the VLC path. Click to confirm.", 'danger', '1000000');
                    });
                };

                self.updateYAPOurl = function () {

                    $http.get('settings/', {
                        params: {
                            yapo_url: self.yapoURL
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        self.response = response.data.yapo_url;
                        self.yapoURL = response.data.yapo_url;
                        self.addAlert('OK, the URL is stored. If it is an address with a port specification, your browser will now open automatically on startup.', 'success', '3000');
                    }, function errorCallback(response) {
                        //alert(self.yapoURL);
                        self.addAlert("There was an error changing the YAPO url. Click to confirm.", 'danger', '1000000');
                    });
                };

                self.TpDB = function () {

                    $http.get('settings/', {
                        params: {
                            tpdb_settings: true,
                            tpdb_enabled: self.tpdb_enabled,
                            tpdb_websitelogos: self.tpdb_website_logos,
                            tpdb_autorename: self.tpdb_autorename,
                            tpdb_actors: self.tpdb_actors,
                            tpdb_photos: self.tpdb_photos,
                            tpdb_websites: self.tpdb_websites,
                            tpdb_tags
                        }

                    }).then(function (response) {
                        // alert(angular.toJson(response));
                        self.response = response.data.tpdb_enabled;
                        self.tpdb_enabled = response.data.tpdb_enabled;
                        self.response = response.data.tpdb_website_logos;
                        self.tpdb_website_logos = response.data.tpdb_website_logos;
                        self.response = response.data.tpdb_autorename;
                        self.tpdb_autorename = response.data.tpdb_autorename;
                        self.response = response.data.tpdb_actors;
                        self.tpdb_actors = response.data.tpdb_actors;
                        self.response = response.data.tpdb_photos;
                        self.tpdb_photos = response.data.tpdb_photos;
                        //$window.location.reload(forceGet);
                        //alert("Got response from server: " + self.pathToFolderToAdd);
                        self.addAlert("OK, TpDB settings are changed.", 'success', '3000');
                    }, function errorCallback(response) {
                        self.addAlert("There was an error changing this option. Click to confirm.", 'danger', '1000000');
                    });
                };

                self.tpdb_scan_all = function () {
                    if(self.tpdb_enabled == false) { self.addAlert("TpDB scanning is disabled. Please enable it first.", 'warning', '3000'); }
                    else if (confirm("Are you sure? This may take a long time. The process can only be interrupted by force quitting YAPO.")) {
                        self.addAlert("Starting TpDB scan, please hold on...", 'info', '5000');
                        $http.get('settings/', {
                            params: {
                                tpdb_scan_all: 'True',
                                force: self.tpdb_force
                            }

                        }   ).then(function (response) {
                            // alert(angular.toJson(response));
                            // self.response = response.data.vlc_path;
                            // self.pathToVLC = response.data.vlc_path;
                            // alert("Got response from server: " + self.pathToFolderToAdd);
                            self.addAlert("Done scanning with TpDB.", 'success', '1000000');
                        }, function errorCallback(response) {
                            self.addAlert("Something went wrong while scanning. Click to confirm.", 'danger', '1000000');
                        });
                    }
                };

                self.checkDupe = function () {

                if (confirm("Are you sure? Any identical copies of your videos will be removed, leaving only one copy."))		{
                            self.addAlert("Starting check, please hold on...", 'info', '5000');
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
                            self.addAlert("Done checking for duplicate files.", 'success', '10000000');
                        }, function errorCallback(response) {
                            //alert("Something went wrong!");
                            self.addAlert("Something went wrong while checking for dupes! Click to confirm.", 'danger', '10000');
                        });
                }
                    };
                
                self.scrapAllActor = function () {
                    if (confirm("Are you sure? This may take a long time. The process can only be interrupted by force quitting YAPO.")) {
                       self.addAlert("Starting scrape, please hold on...", 'info', '5000');
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
                        self.addAlert("Done scraping actors.", 'success', '10000000');
                        }, function errorCallback(response) {
                        self.addAlert("Something went wrong. Click to confirm.", 'danger', '1000000');
                        });
                    }
                };
                
                
                self.tagAllScenes = function () {

                    if (confirm("Are you sure? This may take a long time. The process can only be interrupted by force quitting YAPO.")) {
                        self.addAlert("Beginning tagging ... this may take some time, check the console.", 'info', '5000');
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
                            self.addAlert("Re-tagging complete. Click to confirm.", 'success', '40000000');
                        }, function errorCallback(response) {
                            self.addAlert("Something went wrong. Click to confirm.", 'danger', '1000000');
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
                        self.addAlert("Re-tagging complete. Click to confirm.", 'success', '40000000');
                    }, function errorCallback(response) {
                        self.addAlert("Something went wrong. Click to confirm.", 'danger', '1000000');
                    });
                }  
                };
				
                self.cleanDatabase = function () {
			    if (confirm("Please ensure that all of your drives are connected, otherwise scene data will be deleted from YAPO.")) {
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
                }
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
                    self.addAlert("Beginning scan...", 'info', '3000');
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