angular.module('core.website').factory('Website', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/website/:websiteId/', {}, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data, headers) {

                    return helperService.packageDataAndHeaders(data, headers);
                }
            }
        });
    }
]);