angular.module('settings').component('settings', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/settings/settings.template.html',
        controller: ['$scope', '$rootScope', 'scopeWatchService', '$http',
            function SettingsController($scope, $rootScope, scopeWatchService, $http) {

                var self = this;
                self.response = "";
                self.ignore_last_lookup = false;

                // self.pathToVLC = "";


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
                
                self.scrapAllActors = function () {
                     $http.get('settings/', {
                        params: {
                            scrapAllActor: 'True'
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
                            tagAllScenes: 'true',
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
                


            }
        ]
    }
);