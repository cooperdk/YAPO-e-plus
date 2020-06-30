angular.module('asyncTypeahead').component('asyncTypeahead', {
    // Note: The URL is relative to our `index.html` file
    templateUrl: 'static/js/app/async-typeahead/async-typeahead.template.html',
    bindings: {
        pk: '=',
        object: '=',
        objectType: '@?',
        sendingObject: '=',
        sendingObjectType: '@?',
        selectedObject: '&',
        isMany: '&'
    },
    controller: ['$scope', 'Actor', '$http', 'scopeWatchService',
        function AsyncTypeaheadController($scope, Actor, $http, scopeWatchService) {

            var self = this;

            var actor_tagsURL = '/api/actor-tag/';
            var scenesURL = '/api/scene/';
            var sceneTagsURL = '/api/scene-tag/';
            var actorsURL = '/api/actor/';
            var websiteURL = 'api/website/';
            var playlistURL = 'api/playlist/';
            var httpGETUrl = null;


            self.getTags = function (val) {
                // console.log("async-typeahead input is: " + val);
                // console.log("async-typeahead object is: " + angular.toJson(self.object));
                //
                // console.log("async-typeahead type is: " + angular.toJson(self.objectType));
                // console.log("async-typeahead type is: " + angular.toJson(self.sendingObjectType));
                // console.log("async-typeahead sending object is: " + angular.toJson(self.sendingObject));
                // console.log(attributes.objectType);
                // console.log("async-typeahead object Type is: " + self.object.prototype.toString.call(t));
                if (self.objectType == 'actor_tags') {
                    httpGETUrl = actor_tagsURL;
                } else if (self.objectType == 'scenes') {
                    httpGETUrl = scenesURL;
                } else if (self.objectType == 'scene_tags') {
                    httpGETUrl = sceneTagsURL;
                } else if (self.objectType == 'actors') {
                    httpGETUrl = actorsURL;
                } else if (self.objectType == 'websites') {
                    httpGETUrl = websiteURL;
                } else if (self.objectType == 'playlists') {
                    httpGETUrl = playlistURL;
                }

                return $http.get(httpGETUrl, {
                    params: {
                        search: val,
                        searchField: 'name'

                    }
                }).then(function (response) {

                    var a = response.data.map(function (item) {
                        return item;
                    });

                    if (self.object == 'search') {
                        return a
                    }else{


                        var b = [];
                    var found = false;
                    for (var i = 0; i < a.length; i++) {
                        // console.log("Res to check:" + angular.toJson(a[i]));

                        if (self.object != undefined){
                            for (var j = 0; j < self.object.length && !found; j++) {
                            // console.log("To check against:" + angular.toJson(self.object[j]));
                            if (a[i].id == self.object[j]) {
                                console.log("Match found: " + angular.toJson(a[i]) + " Matches: " + angular.toJson(self.object[j]));
                                found = true;


                            }
                        }
                        }


                        if (!found) {
                            // console.log("Res to push:" + angular.toJson(a[i]));
                            b.push(a[i]);
                            // console.log("Res to array:" + angular.toJson(b));

                        }
                        found = false;
                    }

                    var createVal = {"id": -1, "name": "Create: " + "\"" + val + "\"", "value": val};
                    b.push(createVal);

                    // alert(angular.toJson(a));
                    return b;

                    }

                });


                // var res = [];
                //
                //
                // // alert(val);
                // var p = ActorTag.query({search: val}).$promise;
                //
                // var r = p.then(function (response) {
                //     // alert(angular.toJson(response));
                //     // alert(angular.toJson(response.data));
                //
                //     response.map(function (item) {
                //         // alert(angular.toJson(item));
                //         res.push(item.name);
                //     });
                //
                //     // alert(res.toString());
                //
                // });
                // self.states = res;
                // return self.states;
            };


            self.onSelect = function ($item, $model, $label) {
                // console.log("async-typeaeahd selected object is " + angular.toJson($item));
                // console.log("typeaheadActorTag object before assingment is " + angular.toJson( $scope.typeaheadActorTag));
                console.log("async-typeaeahd onSelect triggered");
                self.selectedObject({$event: {selected: $item}});

                var ans = {
                    'originalObject': self.object,
                    'selectedObject': $item,
                    'sendingObjectType': self.sendingObjectType
                };

                if (self.objectType == 'actor_tags') {
                    scopeWatchService.actorTagSelected($item);
                } else if (self.objectType == 'scenes') {
                    httpGETUrl = scenesURL;
                } else if (self.objectType == 'scene_tags') {
                    scopeWatchService.sceneTagSelected(ans)
                } else if (self.objectType == 'actors') {
                    scopeWatchService.actorSelected(ans)
                } else if (self.objectType == 'websites') {
                    scopeWatchService.websiteSelected(ans)
                } else if (self.objectType == 'playlists') {
                    scopeWatchService.playlistSelected(ans)
                }
                // console.log("typeaheadActorTag object afyer assingment is " + angular.toJson( $scope.typeaheadActorTag));
            };
            // alert("item " +
            // angular.toJson($item) +
            // "model:" + angular.toJson($model) +
            // "lable:" + angular.toJson($label)
            //
            // );
            //     if ($item.id != '-1') {
            //         // alert("This is not a create statement");
            //         var found = false;
            //         for (var i = 0; i < self.sendingObject.self.objectType.length && !found; i++) {
            //             if ($item.id == self.sendingObject.self.objectType[i]) {
            //                 found = true;
            //             }
            //         }
            //         if (!found) {
            //             self.sendingObject.self.objectType.push($item.id);
            //             self.updateActor(self.actor);
            //         }
            //
            //
            //     } else {
            //
            //         // alert("This is a create statment");
            //         var newActorTag = new ActorTag();
            //         newActorTag.name = $item.value;
            //         newActorTag.actors = [];
            //         newActorTag.actors.push(self.actor.id);
            //         // alert("New actorTag name is:" + $item.value);
            //         // alert(angular.toJson(newActorTag));
            //         newActorTag.$save().then(function (res) {
            //             self.actor.actor_tags.push(res.id);
            //             // self.updateActor(self.actor);
            //         })
            //
            //     }
            // };


        }]
});