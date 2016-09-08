angular.module('addItems').component('addItems', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/add-items/add-items.template.html',
    controller: ['$scope', 'ActorTag', 'pagerService', 'scopeWatchService', 'helperService', '$http',
        function AddItemsController($scope, ActorTag, pagerService, scopeWatchService, helperService, $http) {

            var self = this;

            //Input areas:
            self.textareaInputContent = "";
            self.folderInputContent = "";

            var foldersToAdd = "";

            var actorsToAdd = "";

            var sceneTagsToAdd = "";

            var websitesToAdd = "";

            self.createSampleVideo = false;

            var httpRequest = function () {
                return $http.get('add-items/', {
                    params: {
                        actorsToAdd: actorsToAdd,
                        sceneTagsToAdd: sceneTagsToAdd,
                        websitesToAdd:  websitesToAdd,
                        folderToAddPath: foldersToAdd,
                        createSampleVideo: self.createSampleVideo

                    }
                }).then(function (response) {
                    // alert(angular.toJson(response))
                    // alert("Adding folders and files inside: " + self.pathToFolderToAdd);
                }, function errorCallback(response) {
                    alert("Something went wrong!");
                });
            };

            var clearFields = function () {
                foldersToAdd = "";

                actorsToAdd = "";

                sceneTagsToAdd = "";

                websitesToAdd = "";

            };

            self.addFolderClicked = function () {
                clearFields();
                foldersToAdd = self.folderInputContent;
                httpRequest();

            };

            self.addActorsClicked = function () {
                clearFields();
                actorsToAdd = self.textareaInputContent;
                httpRequest();

            };
            
            self.addSceneTagsClicked = function () {
                clearFields();
                sceneTagsToAdd = self.textareaInputContent;
                httpRequest();
            };
            
            self.websitesToAddClicked = function () {
                clearFields();
                websitesToAdd = self.textareaInputContent;
                httpRequest();
            } 
        }
    ]
});


