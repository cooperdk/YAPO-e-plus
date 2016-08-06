angular.module('core.actor').factory('Actor', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/actor/:actorId/', {}, {
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