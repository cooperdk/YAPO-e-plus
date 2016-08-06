angular.module('core.scene').factory('Scene', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/scene/:sceneId/', {}, {
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