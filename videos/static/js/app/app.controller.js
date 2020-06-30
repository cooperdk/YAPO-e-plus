// image crop controller from https://github.com/AllanBishop/angular-img-cropper


angular.module('yapoApp').controller("ImageCropperCtrl", ['$scope', '$rootScope', function ($scope, $rootScope) {
    $rootScope.cropper = {};
    $rootScope.cropper.sourceImage = null;
    $rootScope.cropper.croppedImage = null;
    $rootScope.bounds = {};
    $rootScope.bounds.left = 0;
    $rootScope.bounds.right = 0;
    $rootScope.bounds.top = 0;
    $rootScope.bounds.bottom = 0;
}]);


// Modal controller from angular bootstrap https://angular-ui.github.io/bootstrap/
angular.module('yapoApp').controller('ModalCtrl', function ($scope, $uibModal, $log, helperService) {

    $scope.items = ['item1', 'item2', 'item3'];

    // $scope.actor2 = undefined;


    $scope.animationsEnabled = true;

    $scope.open = function (size) {

        // console.log(angular.toJson($scope.items));
        // console.log(angular.toJson($scope.actor));
        // console.log(angular.toJson($scope.actor.name));
        //
        // $scope.items.push($scope.actor.name);
        // $scope.actor2 = $scope.actor;


        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: 'static/js/app/detail-profile-image/modal-content.html',
            controller: 'ModalInstanceCtrl',
            size: size,
            resolve: {
                items: function () {
                    return $scope.items;
                },
                modelContent: function () {
                    console.log("app-controller: ModalCtrl: modelContent is " + angular.toJson(helperService.get2()));
                    return helperService.get2();

                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };

});

// Please note that $uibModalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

angular.module('yapoApp').controller('ModalInstanceCtrl', function ($scope, $rootScope, $uibModalInstance, items, modelContent) {

    $scope.items = items;
    $scope.modelContent = modelContent;
    $scope.selected = {
        item: $scope.items[0]
    };

    $scope.ok = function (uploadingObject) {
        $rootScope.uploadFile(uploadingObject);
        $uibModalInstance.close();
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };


});