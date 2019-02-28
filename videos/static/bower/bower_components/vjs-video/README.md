# vjs-video

An angular.js directive for video.js

[![Build Status](https://travis-ci.org/LonnyGomes/vjs-video.svg)](https://travis-ci.org/LonnyGomes/vjs-video)
[![npm version](https://badge.fury.io/js/vjs-video.svg)](https://badge.fury.io/js/vjs-video)
[![Bower version](https://badge.fury.io/bo/vjs-video.svg)](https://badge.fury.io/bo/vjs-video)
[![styled with prettier](https://img.shields.io/badge/styled_with-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

With `vjs-video`, you can easily incorporate video and audio into your Angular projects using the robust HTML video player `video.js`.

The `vjs-video` directive handles all of the complexity involved with using `video.js` within an AngularJS Single Page App (SPA) and includes the following features:

- bootstrapping `video.js` after the view is ready
- properly disposing the video when the current Angular view is out of scope
- loading and hot swaping videos using Angular data binding
- audio support (for video.js versions >= 4.9)
- responsive container (for video.js 4.x versions)

## Dependencies

* video.js (4.x or 5.x)
* angular.js >= 1.3

## Installation

The `vjs-video` directive avaible via both npm and bower.


## Bower

The `vjs-video` directive is available via bower with built in dependencies for `video.js` and `angular`. Be sure to run `npm install -g bower` if you don't already have bower installed then run the following to install `vjs-video` into your project.

```bash
bower install --save vjs-video
```
> If you leverage [wiredep](https://github.com/stephenplusplus/grunt-wiredep) in your build workflow, all the required script and stylesheet includes are automatically injected into your html file.

## Webpack

Use npm to install `vjs-video`. The angular and video.js modules will also be installed as dependencies if they aren't already defined.

```bash
npm install --save vjs-video
```

> See [here](https://github.com/LonnyGomes/vjs-video-webpack-example) for an example of using `vjs-video` with webpack.

## RequireJS

The AMD module loading pattern employed by [require.js](http://requirejs.org) is supported by `vjs-video` but you must shim `angular` and define `videojs` as a path as seen in the following example.

**scripts/main.js**
```js
//requirejs configuration
requirejs.config({
    baseUrl: 'bower_components',
    shim: {
        angular: {
            exports: 'angular'
        }
    },
    paths: {
        angular: 'angular/angular',
        videojs: 'video.js/dist/video-js/video',
        'vjs-video': '../scripts/directives/vjs.directive'
    }
});

//require angular and vjs-video
require(['angular', 'vjs-video'], function (angular) {
    angular.module('app', ['vjs.video'])
        .controller('MainCtrl', ['$scope', function (scope) {
            scope.$on('vjsVideoReady', function(e, data) {
                //data contains `id`, `vid`, `player` and `controlBar`
            });
        }]);
});

```

## Manual Install

Download the [latest vjs-video build](https://raw.githubusercontent.com/LonnyGomes/vjs-video/master/dist/vjs-video.min.js) as well as [Angular](https://angularjs.org) and [video.js](http://videojs.com). Then, include `angular`, `video.js`, and `vjs-video` as script tags along with it's corresponding css into your HTML page.

```html
<html ng-app="app">
  <head>
    <link rel="stylesheet" href="bower_components/video.js/dist/video-js/video-js.css" />
  </head>
  <body ng-app="app">
    <script src="bower_components/angular/angular.js"></script>
    <script src="bower_components/video.js/dist/video.js"></script>
    <script src="bower_components/vjs-video/dist/vjs-video.js"></script>
</body>
</html>
```

## Basic usage

The `vjs-video` directive is designed to be non-invasive; to use it, include `vjs-video` as a dependency and add the directive to a video or audio tag styled for `video.js`.


First include `vjs-video` as a dependency within your angular app:

```javascript
angular.module('app', [ 'vjs.video']);

```

Next, add the `vjs-video` directive to a video or audio tag styled for `video.js`:

```html
<video class="video-js vjs-default-skin" controls preload="auto"
       width="640" height="264" poster="poster.jpg" vjs-video>
    <source src="example_video.mp4" type="video/mp4">
</video>
```

## Responsive Container

The `vjs-video-container` directive implements responsive sizing for the 4.x version of `video.js` 4.x. A custom aspect ratio can be defined with the default being the 16:9 wide screen ratio.

__NOTE:__ The `vjs-video-container` is meant to be used with version 4.x of `video.js`; `video.js` 5.x natively supports video. If used with 5.0, the `vjs-video-container` aspect ratio values are passed through to `video.js`.

The following example wraps a `video.js` instance within a responsive container with a ratio of `4:3`:

```html
<vjs-video-container vjs-ratio="4:3">
    <video class="video-js vjs-default-skin" controls preload="auto" poster="poster.jpg">
        <source src="example_video.mp4" type="video/mp4">
    </video>
</vjs-video-container>
```

> When using `vjs-video-container` be sure to attach all the directive attributes (such as `vjs-setup` or `vjs-media`) to the `vjs-video-container` element rather than on the enclosed video or audio tag. The attributes only should be attached when using in conjunction with the `vjs-video` directive on a video or audio tag.

> Also, make sure you never mix usage of `vjs-video-container` with `vjs-video`. The `vjs-video` directive accepts the same directive attributes but shouldn't be used if a video or audio tag is wrapped inside of a `vjs-video-container`.

## Directive Attributes

The `vjs-video` directive includes additional attributes that leverage AngularJS's strengths.

* vjs-setup - accepts an object as alternative to using data-setup on the video element
* vjs-media - accepts a bindable object that defines sources and tracks
* vjs-ratio - defines the aspect ratio in the format width:height

> _*NOTE:*_ the `vjs-ratio` attribute support is limited to usage with the `vjs-video-container` item when using `video.js` < 5.0. In 5.0 and above, `vjs-ratio` can be used with the `vjs-video` directive as well.

### vjs-setup

You can use `vjs-setup` instead of the `data-setup` attribute `video.js` uses if you would prefer to define all of the properties on the scope vs an inline JSON string.

The following example will set the loop option for the `video.js` instance using the `vjs-setup` attribute:

_HTML_

```html
<video class="video-js vjs-default-skin" controls preload="auto"
       width="640" height="264" vjs-video vjs-setup="options">
    <source src="http://video-js.zencoder.com/oceans-clip.mp4" type='video/mp4' />
</video>
```

_JavaScript_

```javascript
angular.module('app')
    .controller('MainCtrl', ['$scope', function (scope) {

        scope.options = {
            loop: true
        };
    }]);
```

### vjs-media

The `vjs-media` option expects a reference to an object that contains a `sources`, `tracks`, and/or `poster` element. Whenever the `vjs-media` value is changed, `video.js` is reinitialized given the new data.

The following example defines a poster image, two sources and one track in a scope variable that is processed by `vjs-video`.

_HTML_

```html
<video class="video-js vjs-default-skin" controls preload="auto"
       width="592" height="252" vjs-video vjs-media="mediaToggle">
</video>
```
_JavaScript_

```javascript
angular.module('app')
    .controller('MainCtrl', ['$scope', function (scope) {
        scope.mediaToggle = {
            sources: [
                {
                    src: 'images/happyfit2.mp4',
                    type: 'video/mp4'
                },
                {
                    src: 'images/happyfit2.webm',
                    type: 'video/webm'
                }
            ],
            tracks: [
                {
                    kind: 'subtitles',
                    label: 'English subtitles',
                    src: 'assets/subtitles.vtt',
                    srclang: 'en',
                    default: true
                }
            ],
            poster: 'images/screen.jpg'
        };

        //listen for when the vjs-media object changes
        scope.$on('vjsVideoMediaChanged', function (e, data) {
            console.log('vjsVideoMediaChanged event was fired');
        });
    }]);
```
> In the event that the `vjs-media` object changes, a `vjsVideoMediaChanged` event is fired within the scope context as seen in the above example.

### vjs-ratio

The `vjs-ratio` attribute only works in conjunction with the `vjs-video-container` directive when using `video.js` 4.x but can be used with either the `vjs-video` or `vjs-video-container` directives when using version 5 of `video.js.` The value should list width and then height separated by a `:` `(w:h)`. The value can be the actual width and height or the least common denominator such as `16:9`.

## Getting a reference to the video.js instance

There are times you will want to get access to the video object that `video.js` creates. The `vjs-video` directive dispatches an event after initialization and can be accessed by listening on the scope for the `vjsVideoReady` event.

```javascript
angular.module('app')
    .controller('MainCtrl', ['$scope', function (scope) {
        scope.$on('vjsVideoReady', function (e, data) {
            //data contains `id`, `vid`, `player` and `controlBar`
            //NOTE: vid is depricated, use player instead
            console.log('video id:' + data.id);
            console.log('video.js player instance:' + data.player);
            console.log('video.js controlBar instance:' + data.controlBar);
        });
    }]);
```

The second parameter of the callback is a data object which contains the following:

* __id__: the CSS id value for the video
* __player__: the video.js player object instance
* __vid__: the video.js player object instance _(**deprecated**, use `player` instead)_
* __controlBar__: the controlBar element of the video.js object

## Build & development

Run `grunt` for building and `grunt serve` for preview. All code modifications should be run through prettier by using an IDE pluggin or by running `npm run prettier`.

## Testing

Running `grunt test` will run the unit tests with karma.

## Release History

**_v0.1.11_**

* formatted code with prettier (#77)
* fixed issue where vjs-video did not work with video-js-contrib-ads; contribution by @MZeeshanSiddique (#75)
* updated filepaths in README; contribution by @tiagomsmagalhaes

**_v0.1.10_**

* fixes regression which broke webpack support (#64)

**_v0.1.9_**

* fixed bug that broke RequireJS support (#61)
* added documentation for using RequireJS with `vjs-video`

**_v0.1.8_**

* fixed error where v0.1.7 failed to include proper minified files (#58)
* added `video.js` and `angular` dependencies to the package.json (#59)
* updated README regaurding dependencies on `video.js` and `angular`

**_v0.1.7_**

* added support for CommonJS and AMD module loaders (#42)
* updated documentation for legibility and clarity (#56)

**_v0.1.6_**

* added support for using `vjs-video` with the audio tag; contribution by @cvn (#36)
* updated documentation to fix typos and better explain how `vjs-video` works (#27)


**_v0.1.5_**

* added player object to `vjsVideoReady` callback and deprecated the `vid` object

**_v0.1.4_**

* added vjs-ratio support to vjs-video directive when using video.js >= 5.x (#19)

**_v0.1.3_**

* fixed issue where vjs-ratio threw an angular error in certain cases (#15)
* added reference to a video's controlBar in the vjsVideoReady callback (#17)

**_v0.1.2_**

* added checks for mixed use of the `vjs-video` and `vjs-video-container` directives (#13)
* updated documentation for clarity and fixed typos

**_v0.1.1_**

* fixed issue where `vjs-video` didn't consistently work on mobile devices (#10)
* updated GitHub pages site to be more mobile friendly

**_v0.1.0_**

* initial release of vjs-video
