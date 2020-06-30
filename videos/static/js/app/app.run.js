var app = angular.module('yapoApp', ['xeditable','$rootScope']);


app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});




