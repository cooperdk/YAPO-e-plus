// Register `phoneList` component, along with its associated controller and template
angular.module('detailProfileImage').component('detailProfileImage', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/detail-profile-image/detail-profile-image.template.html',
    bindings: {
        pk: '=',
        actor: '='
    },
    controller: ['$scope',
        function DetailProfileImageController($scope) {
            $scope.modelContent = this.actor;
        }]
});




