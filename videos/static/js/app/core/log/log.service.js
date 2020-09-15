angular.module('core.log').factory('log', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/log/:LogId/', {}, {
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
