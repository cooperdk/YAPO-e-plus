angular.module('index').component('index', {
        // Note: The URL is relative to our `index.html` file
        templateUrl: 'static/js/app/index/index.template.html',
        controller: ['$scope', '$rootScope', 'scopeWatchService', '$http','helperService',
            function indexController($scope, $rootScope, scopeWatchService, $http, helperService) {

                var self = this;
                self.response = "";
            }
        ]
    }
);