angular.module('core.playlist').factory('Playlist', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/playlist/:playlistId/', {}, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data, headers) {

                    return helperService.packageDataAndHeaders(data, headers);
                }

            },

            update: {
                method: 'PUT'
            },

            patch: {
                method: 'PATCH'
            }


        });
    }
]);