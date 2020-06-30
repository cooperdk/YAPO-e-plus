angular.module('navBar', []).component('navBar', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/nav-bar/nav-bar.template.html',
    bindings: {},
    controller: ['$scope', '$rootScope', 'Actor', 'SceneTag', 'Website', 'ActorTag', 'helperService', '$http','Playlist',
        function NavBarController($scope, $rootScope, Actor, SceneTag, Website, ActorTag, helperService, $http, Playlist ) {
            
            // Global function to create new item
            $rootScope.createNewItem = function (typeOfItemToAdd, newItemName) {
                    var newItem;
                    if (typeOfItemToAdd == 'actors') {
                        newItem = new Actor();
                        newItem.thumbnail = 'media/images/actor/Unknown/profile/profile.jpg'; //need to change this to a constant!
                        newItem.scenes = [];
                    } else if (typeOfItemToAdd == 'scene_tags') {
                        newItem = new SceneTag();
                        newItem.scenes = [];
                        newItem.websites = [];
                    } else if (typeOfItemToAdd == 'websites') {
                        newItem = new Website;
                        newItem.scenes = [];
                    } else if (typeOfItemToAdd == 'actor_tags'){
                        newItem = new ActorTag;
                        newItem.actors = [];
                    } else if (typeOfItemToAdd == 'playlists'){
                        newItem = new Playlist;
                        newItem.scenes = []
                    }
    
                    newItem.name = newItemName;
    
                    return newItem
                };
            
            $rootScope.patchEntity = function (entityToPatchType, entityToPatchId, patchType, patchData, addOrRemove,
                                              multiple, permDelete, selectedScenes) {

                var type = {};
                type[patchType] = patchData;

                var itemsToUpdate = [];
                if (multiple) {
                    itemsToUpdate = selectedScenes
                } else {
                    itemsToUpdate.push(entityToPatchId)
                }


                // if (multiple) {

                $http.post('tag-multiple-items/', {
                    params: {
                        type: entityToPatchType,
                        patchType: patchType,
                        patchData: patchData,
                        itemsToUpdate: itemsToUpdate,
                        addOrRemove: addOrRemove,
                        permDelete: permDelete
                    }
                }).then(function (response) {
                    console.log("Update finished successfully")
                }, function errorCallback(response) {
                    alert("Something went wrong!");
                });
            };
            
            $rootScope.addItemToScene = function (scene, itemToAdd, typeOfItemToAdd) {

                if (scene[typeOfItemToAdd] == undefined) {
                    scene[typeOfItemToAdd] = [];
                }
                
                var found = helperService.getObjectIndexFromArrayOfObjects(itemToAdd, scene[typeOfItemToAdd]);
                
                 if (found == null) {
                    scene[typeOfItemToAdd].push(itemToAdd);
                }
                
                if (typeOfItemToAdd == 'websites' && itemToAdd.scene_tags_with_names.length > 0) {
                    for (var i = 0; i < itemToAdd.scene_tags_with_names.length; i++) {
                        $rootScope.addItemToScene(scene, itemToAdd.scene_tags_with_names[i], 'scene_tags')
                    }
                }

                if (typeOfItemToAdd == 'actors' && itemToAdd.actor_tags.length > 0) {
                    for (var z = 0; z < itemToAdd.actor_tags.length; z++) {
                        if (itemToAdd.actor_tags[z].scene_tags.length > 0){
                            $rootScope.addItemToScene(scene, itemToAdd.actor_tags[z].scene_tags[0], 'scene_tags')
                        }

                    }
                }
                
                return scene
                
            };
            
            $rootScope.removeItemFromScene = function (scene, itemToRemove, typeOfItemToRemove) {
                var resId = [];
                var resObj = [];

                if (scene[typeOfItemToRemove] == undefined){
                    scene[typeOfItemToRemove] = [];
                }

                for (var i = 0; i < scene[typeOfItemToRemove].length; i++) {
                    if (itemToRemove.id != scene[typeOfItemToRemove][i].id) {
                        resId.push(scene[typeOfItemToRemove][i].id);
                        resObj.push(scene[typeOfItemToRemove][i]);
                    }
                }

                scene[typeOfItemToRemove] = resObj;

                resObj = [];


                if (typeOfItemToRemove == 'websites' && itemToRemove.scene_tags_with_names.length > 0) {
                    for (var k = 0; k < itemToRemove.scene_tags_with_names.length; k++) {
                        $rootScope.removeItemFromScene(scene, itemToRemove.scene_tags_with_names[k], 'scene_tags')
                    }
                }
                
                if (typeOfItemToRemove == 'actors' && itemToRemove.actor_tags.length > 0) {
                    for (var z = 0; z < itemToRemove.actor_tags.length; z++) {
                        if (itemToRemove.actor_tags[z].scene_tags.length > 0){
                            $rootScope.removeItemFromScene(scene, itemToRemove.actor_tags[z].scene_tags[0], 'scene_tags')
                        }

                    }
                }

                return scene
            };


        }]
});








