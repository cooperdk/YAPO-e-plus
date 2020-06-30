angular.module('core').filter('checkmark', function () {
    return function (input) {
        if (input === 'M') {
            return '\u2642'
        } else {
            return '\u2640'

        }

    };
});