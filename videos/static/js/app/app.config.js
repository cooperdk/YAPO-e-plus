app.config(['$sceProvider', '$locationProvider', '$routeProvider', '$httpProvider', '$resourceProvider', 
    function config($sceProvider, $locationProvider, $routeProvider, $httpProvider, $resourceProvider) {

        // disable SCE completely (https://docs.angularjs.org/api/ng/service/$sce)
        $sceProvider.enabled(false);

        $locationProvider.hashPrefix('!');


        $routeProvider.when('/actor', {
            template: '<section-list-wrapper main-page="true" section-type="\'ActorList\'"></section-list-wrapper>'
        }).when('/actor/:actorId', {
            template: '<actor-detail></actor-detail>'
        }).when('/scene/', {
            template: '<section-list-wrapper main-page="true" section-type="\'SceneList\'"></section-list-wrapper>'
        }).when('/scene/:sceneId', {
            template: '<scene-detail></scene-detail>'
        }).when('/actor-tag/', {
            template: '<section-list-wrapper main-page="true" section-type="\'ActorTagList\'"></section-list-wrapper>'
        }).when('/actor-tag/:actorTagId', {
            template: '<actor-tag-detail></actor-tag-detail>'
        }).when('/scene-tag/', {
            template: '<section-list-wrapper main-page="true" section-type="\'SceneTagList\'"></section-list-wrapper>'
        }).when('/scene-tag/:sceneTagId', {
            template: '<scene-tag-detail></scene-tag-detail>'
        }).when('/website/', {
            template: '<section-list-wrapper main-page="true"section-type="\'WebsiteList\'"></section-list-wrapper>'
        }).when('/website/:websiteId', {
            template: '<website-detail></website-detail>'
        }).when('/folder/', {
            template: '<section-list-wrapper main-page="true"section-type="\'DbFolder\'"></section-list-wrapper>'
            // template: '<db-folder-tree></db-folder-tree>'
        }).when('/folder/:parentId', {
            template: '<section-list-wrapper main-page="true"section-type="\'DbFolder\'"></section-list-wrapper>'
            // template: '<db-folder-tree></db-folder-tree>'
        }).when('/add/', {
            template: '<add-items></add-items>'
        }).when('/settings/', {
            template: '<settings></settings>'
        }).otherwise('/'), {
            template: '<br><br><br><br><h1> This is temp index</h1>'

        };
        //
        // // disable SCE completely (https://docs.angularjs.org/api/ng/service/$sce)
        // $sceProvider.enabled(false);

        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        // This only works in angular 3!
        // It makes dealing with Django slashes at the end of everything easier.

        $resourceProvider.defaults.stripTrailingSlashes = false;
    }

]);

app.run(function (editableOptions) {
    editableOptions.theme = 'bs3';
});
