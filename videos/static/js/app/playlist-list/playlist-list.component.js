angular.module('playlistList').component('playlistList', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: ['$element', '$attrs', function ($element, $attrs) {

        // if ($attrs.viewStyle == 'grid') {
        //     return 'static/js/app/scene-list/scene-list-grid.template.html'
        // } else {
        return 'static/js/app/playlist-list/playlist-list.template.html';
        // }


    }],
    bindings: {
        mainPage: '=',
        treeFolder: '='
    },
    controller: ['$scope', '$http', '$rootScope', 'Playlist', 'helperService',
        function PlaylistListController($scope, $http, $rootScope, Playlist, helperService) {

            var self = this;
            
            
            
            
            $http.get('api/playlist/', {}).then(function (response) {
                // alert(angular.toJson(response));
                self.playlists = response.data;
                self.response = response;
                // alert("Got response from server: " + self.pathToFolderToAdd);
            }, function errorCallback(response) {
                alert("Something went wrong!");
            });


            self.removePlaylist = function (playlistToRemove) {

                Playlist.remove({playlistId: playlistToRemove.id});

                var found = helperService.getObjectIndexFromArrayOfObjects(playlistToRemove,self.playlists);

                if(found != null){
                    self.playlists.splice(found,1)
                }



            }

        }]
});