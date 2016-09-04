angular.module('core.actorTag').factory('ActorTag', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/actor-tag/:actorTagId/', {}, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data, headers) {

                    return helperService.packageDataAndHeaders(data, headers);
                }

            }, update: {
                method: 'PUT'
            },
            patch: {
                method: 'PATCH'
            }
        });
    }
]);