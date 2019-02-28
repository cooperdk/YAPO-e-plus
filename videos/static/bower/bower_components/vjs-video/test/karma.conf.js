// Karma configuration
// http://karma-runner.github.io/0.12/config/configuration-file.html
// Generated on 2015-08-15 using
// generator-karma 0.9.0

module.exports = function(config) {
    'use strict';

    var configuration = {
        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,

        // base path, that will be used to resolve files and exclude
        basePath: '../',

        // testing framework to use (jasmine/mocha/qunit/...)
        frameworks: ['mocha', 'chai'],

        preprocessors: {
            'app/scripts/**/*.html': ['ng-html2js']
        },
        // list of files / patterns to load in the browser
        files: [
            // bower:js
            'bower_components/jquery/dist/jquery.js',
            'bower_components/angular/angular.js',
            'bower_components/video.js/dist/video-js/video.js',
            'bower_components/angular-mocks/angular-mocks.js',
            'bower_components/sinonjs/sinon.js',
            'bower_components/bootstrap-css/js/bootstrap.min.js',
            'bower_components/angular-gist/angular-gist.min.js',
            // endbower
            'app/scripts/**/*.js',
            'test/mock/**/*.js',
            'test/spec/**/*.js',
            'app/scripts/**/*.html'
        ],

        // list of files / patterns to exclude
        exclude: [],

        // web server port
        port: 8080,

        // Start these browsers, currently available:
        // - Chrome
        // - ChromeCanary
        // - Firefox
        // - Opera
        // - Safari (only Mac)
        // - PhantomJS
        // - IE (only Windows)
        browsers: ['Chrome'],

        reporters: ['mocha'],

        // Continuous Integration mode
        // if true, it capture browsers, run tests and exit
        singleRun: false,

        colors: true,

        // level of logging
        // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
        logLevel: config.LOG_INFO,

        // Uncomment the following lines if you are using grunt's server to run the tests
        // proxies: {
        //   '/': 'http://localhost:9000/'
        // },
        // URL root prevent conflicts with the site root
        // urlRoot: '_karma_'
        ngHtml2JsPreprocessor: {
            // strip this from the file path
            stripPrefix: 'app/'
        },
        //configuration to get travis-ci to run Chrome
        customLaunchers: {
            Chrome_travis_ci: {
                base: 'Chrome',
                flags: ['--no-sandbox']
            }
        }
    };

    if (process.env.TRAVIS) {
        configuration.browsers = ['Chrome_travis_ci'];
    }

    config.set(configuration);
};
