angular.module('core.dbFolder').factory('DbFolder', ['$resource', 'helperService',
    function ($resource, helperService) {
        return $resource('api/folder/:dbFolderId/', {}, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data, headers) {
                    console.log("we are in db-folder service");

                    return helperService.packageDataAndHeaders(data, headers);
                }

            }
        });
    }
]);