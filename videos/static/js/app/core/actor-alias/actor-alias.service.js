angular.module('core.actorAlias').factory('ActorAlias', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('/api/actor-alias/:actorAliasId/', {}, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data, headers) {

                    return helperService.packageDataAndHeaders(data, headers);
                }

            },
            update: {
                method: 'PUT'
            }

        });
    }
]);