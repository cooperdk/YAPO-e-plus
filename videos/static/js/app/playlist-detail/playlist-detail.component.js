angular.module('playlistDetail').component('playlistDetail', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: ['$element', '$attrs', function ($element, $attrs) {

        // if ($attrs.viewStyle == 'grid') {
        //     return 'static/js/app/scene-list/scene-list-grid.template.html'
        // } else {
        return 'static/js/app/playlist-detail/playlist-detail.template.html';
        // }


    }],
    bindings: {
        mainPage: '='
    },
    controller: ['$scope', '$http', '$rootScope', '$routeParams', 'scopeWatchService', 'Playlist',
        function PlaylistListController($scope, $http, $rootScope, $routeParams, scopeWatchService, Playlist) {

            var self = this;

            var routParam = $routeParams.playlistId;
            var gotPromise = false;
            
            
            $http.get('api/playlist/' + routParam, {}).then(function (response) {
                // alert(angular.toJson(response));
                self.playlist = response.data;
                scopeWatchService.playlistLoaded(self.playlist);
                gotPromise = true;
                
                // alert("Got response from server: " + self.pathToFolderToAdd);
            }, function errorCallback(response) {
                alert("Something went wrong!");
            });

            $scope.$on("didPlaylistLoad", function (event, actor) {

                if (gotPromise) {

                    scopeWatchService.playlistLoaded(self.playlist);


                    
                }
            });
            
            self.update = function () {
                Playlist.update({playlistId: self.playlist.id}, self.playlist)
            }





        }]
});