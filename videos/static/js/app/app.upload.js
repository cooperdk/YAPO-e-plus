// https://uncorkedstudios.com/blog/multipartformdata-file-upload-with-angularjs

var myApp = angular.module('fileUpload', []);

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function () {
                scope.$apply(function () {
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function (file, uploadingObject, uploadingObjectID) {
        var fd = new FormData();
        fd.append('file', file);
        fd.append('type', uploadingObject);
        fd.append('id', uploadingObjectID);
        $http.post('/upload/', fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
            .success(function () {
            })
            .error(function () {
            });
    }
}]);

myApp.controller('myCtrl', ['$scope', 'fileUpload', function ($scope, fileUpload) {

    $scope.uploadFile = function (uploadingObject) {
        // console.log("Is cropper in scope?" +  $scope.cropper.croppedImage)
        // var file = $scope.myFile;
        var file = $scope.cropper.croppedImage;
        console.log('file is ');
        console.dir(file);
        // var uploadingObject = $scope.modelContent;
        var uploadingObjectID = $scope.modelContent.id;
        fileUpload.uploadFileToUrl(file, uploadingObject, uploadingObjectID);
    };

}]);
