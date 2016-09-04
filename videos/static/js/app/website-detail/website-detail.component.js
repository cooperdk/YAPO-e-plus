angular.module('websiteDetail').component('websiteDetail', {
    templateUrl: 'static/js/app/website-detail/website-detail.template.html',
    controller: ['$routeParams', 'Website', 'scopeWatchService', '$rootScope', '$scope', 'helperService',
        function WebsiteDetailController($routeParams, Website, scopeWatchService, $rootScope, $scope, helperService) {
            var self = this;
            var gotPromise = false;
            self.website = Website.get({websiteId: $routeParams.websiteId}).$promise.then(function (res) {

                scopeWatchService.websiteLoaded(res);
                self.website = res;
                // alert(res.name);
                $rootScope.title = res.name;
                gotPromise = true;
            });

            $scope.$on("didWebsiteLoad", function (event, website) {
                if (gotPromise) {
                    scopeWatchService.websiteLoaded(self.website);
                }
            });


            $scope.$on("sceneTagSelected", function (event, object) {

                if (object['sendingObjectType'] == 'Website-Detail') {

                    var originalObject = object['originalObject'];
                    var selectedObject = object['selectedObject'];
                    // alert(angular.toJson(object));

                    var patchContent = {'scene_tags': ''};
                    // Means the selected item does not exist in the db
                    if (selectedObject.id == '-1') {
                        var newItem =  $rootScope.createNewItem("scene_tags", selectedObject.value);

                        newItem.$save().then(function (res) {
                            self.website.scene_tags_with_names.push(res);
                            self.website.scene_tags.push(res.id);

                            patchContent['scene_tags'] = self.website.scene_tags;
                            Website.patch({websiteId: self.website.id}, patchContent)
                        })
                    } else {

                        var objectIndex = helperService.getObjectIndexFromArrayOfObjects(selectedObject, self.website.scene_tags_with_names);

                        if (objectIndex == null) {
                            self.website.scene_tags_with_names.push(selectedObject);
                            self.website.scene_tags.push(selectedObject.id);
                            patchContent['scene_tags'] = self.website.scene_tags;
                            Website.patch({websiteId: self.website.id}, patchContent)

                        }
                    }


                }


                // self.sceneTagSelect(sceneTag['selectedObject']);
            });


            self.modifyWebsiteAlias = function (website) {

                var patchContent = {'website_alias': website.website_alias};
                alert(angular.toJson(patchContent));
                patchWebsite(website, patchContent)


            };

            var patchWebsite = function (website_to_patch, patchContent) {
                Website.patch({websiteId: website_to_patch.id}, patchContent)
            };
            
            
            self.removeSceneTag = function (sceneTag) {
                
                var ans = helperService.removeObjectFromArrayOfObjects(sceneTag,self.website.scene_tags_with_names);
                var patchContent = {'scene_tags': ans['resId']};
                self.website.scene_tags_with_names = ans['resObject'];
                 
                Website.patch({websiteId: self.website.id}, patchContent)
                
                
                
                
            };

            self.update = function () {
                Website.update({websiteId: self.website.id}, self.website)
            }

        }
    ]
});