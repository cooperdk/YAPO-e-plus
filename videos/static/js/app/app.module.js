// Define the `phonecatApp` module
var app = angular.module('yapoApp', [
    // ...which depends on the `phoneList` module
    'ngRoute',
    // 'djangoRESTResources',
    'xeditable',
    'actorList',
    'actorDetail',
    'sceneList',
    'sceneDetail',
    'actorTagList',
    'actorTagDetail',
    'sceneTagList',
    'sceneTagDetail',
    'websiteList',
    'websiteDetail',
    'dbFolderTree',
    // 'ui.tree',
    'actorAliasList',
    'ui.bootstrap',
    'ngAnimate',
    'angular-img-cropper',
    'detailProfileImage',
    'fileUpload',
    'helper',
    'asyncTypeahead',
    'sectionListWrapper',
    'navBar',
    'pager',
    'scopeWatch',
    'pagination',
    'ngStorage',
    // 'mgcrea.ngStrap',
    'core',
    'addItems',
    'settings'


]);