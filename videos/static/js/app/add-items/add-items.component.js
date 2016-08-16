angular.module('addItems').component('addItems', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/add-items/add-items.template.html',
    controller: ['$scope', 'ActorTag', 'pagerService', 'scopeWatchService', 'helperService', '$http',
        function AddItemsController($scope, ActorTag, pagerService, scopeWatchService, helperService, $http) {

            var self = this;

            self.pathToFolderToAdd = "";

            self.actorsToAdd = "";
            
            self.createSampleVideo = false;
            
            self.addFolderClicked = function () {

                return $http.get('add-items/', {
                    params: {
                        actorsToAdd: self.actorsToAdd,
                        folderToAddPath: self.pathToFolderToAdd,
                        createSampleVideo: self.createSampleVideo
                        
                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    // alert("Adding folders and files inside: " + self.pathToFolderToAdd);
                }, function errorCallback(response) {
                    alert("Something went wrong!");
                });


            };

            self.addActorsClicked = function () {

                return $http.get('add-items/', {
                    params: {
                        actorsToAdd: self.actorsToAdd,
                        folderToAddPath: self.pathToFolderToAdd
                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    alert("Finished adding actors successfully...");
                }, function errorCallback(response) {
                    alert("Something went wrong!");
                });

            };
        }
    ]
});


