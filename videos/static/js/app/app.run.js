var app = angular.module('yapoApp', ['xeditable']);


app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});


