angular.module('core.sceneTag').factory('SceneTag', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/scene-tag/:sceneTagId/', {}, {
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