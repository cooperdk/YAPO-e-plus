/*global describe, beforeEach, module, inject, it, angular, expect */
/*jslint nomen: true */
describe('Directive: vjs.directive.js', function() {
    'use strict';

    // load the directive's module
    beforeEach(module('vjsVideoApp'));

    var vidStr = '<video vjs-video></video>',
        vidWithIdStr = "<video id='vidId' vjs-video></video>",
        multipleVidStr =
            '<div><video vjs-video></video><video vjs-video></video></div>',
        audioStr = '<audio vjs-video></audio>',
        nonVidStr = '<div vjs-video>',
        vidContainerStr = '<div vjs-video-container><video></video></div>',
        vidElementContainerStr =
            '<vjs-video-container><video></video></vjs-video-container>',
        vidElementContainerVjsVidStr =
            '<vjs-video-container><video vjs-video></video></vjs-video-container>',
        vidElementContainerVjsSetupStr =
            '<vjs-video-container><video vjs-setup></video></vjs-video-container>',
        vidElementContainerVjsMediaStr =
            '<vjs-video-container><video vjs-media></video></vjs-video-container>',
        vidElementContainerVjsRatioStr =
            '<vjs-video-container><video vjs-ratio></video></vjs-video-container>',
        audioContainerStr = '<div vjs-video-container><audio></audio></div>',
        nonVidContainerStr = '<div vjs-video-container></div>',
        multVidsContainerStr =
            '<div vjs-video-container><video></video><video></video></div>',
        multMixedContainerStr =
            '<div vjs-video-container><video></video><audio></audio></div>',
        vidContainerWithDimsStr =
            "<div vjs-video-container><video id='vid-dim' width='320' height='320'></video></div>",
        vidRatioCharStr =
            "<div vjs-video-container vjs-ratio='asdf'><video></video></div>",
        vidRatioInvalidStr =
            "<div vjs-video-container vjs-ratio='1920:1080:720'><video></video></div>",
        vidRatioInvalidWStr =
            "<div vjs-video-container vjs-ratio='O:1080'><video></video></div>",
        vidRatioInvalidHStr =
            "<div vjs-video-container vjs-ratio='1080:*'><video></video></div>",
        vidRatioHeightZeroStr =
            "<div vjs-video-container vjs-ratio='0:640'><video></video></div>",
        vidRatioWidthZeroStr =
            "<div vjs-video-container vjs-ratio='640:0'><video></video></div>",
        vidWithMediaNoVals = "<video vjs-video vjs-media='testMedia'></video>",
        scope,
        $compile;

    beforeEach(
        inject(function($rootScope, _$compile_) {
            scope = $rootScope.$new();
            $compile = _$compile_;
        })
    );

    function compileAndLink(htmlStr, s) {
        var el = angular.element(htmlStr);

        el = $compile(el)(s);
        scope.$digest();

        return el;
    }

    describe('vjs-video', function() {
        it('should attach videojs to the video tag', function() {
            //videojs should add at vjs-tech class to the element
            var el = compileAndLink(vidStr, scope);
            expect(el.hasClass('vjs-tech')).to.be.true;
        });

        it('should attach videojs to the audio tag', function() {
            //videojs should add at vjs-tech class to the element
            var el = compileAndLink(audioStr, scope);
            expect(el.hasClass('vjs-tech')).to.be.true;
        });

        it('should attach videojs to multiple video tags', function() {
            //videojs should add at vjs-tech class to the element
            var el = compileAndLink(multipleVidStr, scope);
            expect(el[0].querySelectorAll('.vjs-tech').length).to.equal(2);
        });

        it('should throw an error if not attached to a video tag', function() {
            expect(function() {
                var el = compileAndLink(nonVidStr, scope);
            }).throws(Error);

            expect(function() {
                var el = compileAndLink(vidStr, scope);
            }).to.not.throw(Error);
        });

        it('should dispatch a ready event upon successful load', function(
            done
        ) {
            var el;
            scope.$on('vjsVideoReady', function(e, data) {
                expect(data.id).to.exist;
                expect(data.vid).to.exist;
                expect(data.controlBar).to.exist;
                expect(data.player).to.exist;
                expect(data.id).to.match(/^vidId/);
                expect(data.controlBar).to.equal(data.vid.controlBar);
                //vid is deprecated but we want to make sure the player referenced
                //in vid matched the player supplied in the callback
                expect(data.player).to.equal(data.vid.player());
                done();
            });
            el = compileAndLink(vidWithIdStr, scope);
        });

        describe('vjs-media attribute', function() {
            it("should throw an error if vjs-media doesn't contain sources or tracks", function() {
                scope.testMedia = {}; //set scope w/o defining sources or tracks elements
                expect(function() {
                    compileAndLink(vidWithMediaNoVals, scope);
                }).throws(
                    Error,
                    'a sources and/or tracks element must be defined for the vjs-media attribute'
                );
            });

            it('should throw an error if vjs-media sources is not an array', function() {
                scope.testMedia = {
                    sources: 'invalid'
                };
                expect(function() {
                    compileAndLink(vidWithMediaNoVals, scope);
                }).throws(
                    Error,
                    'sources must be an array of objects with at least one item'
                );
            });

            it('should throw an error if vjs-media tracks is not an array', function() {
                scope.testMedia = {
                    tracks: 'invalid'
                };
                expect(function() {
                    compileAndLink(vidWithMediaNoVals, scope);
                }).throws(
                    Error,
                    'tracks must be an array of objects with at least one item'
                );
            });

            it('should generate source DOM elements', function() {
                scope.testMedia = {
                    sources: [
                        { src: 'video.mp4', type: 'mp4/video' },
                        { src: 'video.ogg', type: 'ogg/video' }
                    ]
                };

                var el = compileAndLink(vidWithMediaNoVals, scope),
                    children = el.children(),
                    curIdx,
                    curChild;

                expect(el.children().length).to.equal(2);

                for (curIdx = 0; curIdx < el.children().length; curIdx += 1) {
                    curChild = el.children()[curIdx];

                    expect(curChild.nodeName).to.equal('SOURCE');
                    expect(curChild.getAttribute('src')).to.equal(
                        scope.testMedia.sources[curIdx].src
                    );
                    expect(curChild.getAttribute('type')).to.equal(
                        scope.testMedia.sources[curIdx].type
                    );
                }
            });

            it('should generate track DOM elements', function() {
                scope.testMedia = {
                    tracks: [
                        {
                            kind: 'subtitles',
                            label: 'english subtitles',
                            src: 'subtitles.vtt',
                            srclang: 'en'
                        }
                    ]
                };

                var el = compileAndLink(vidWithMediaNoVals, scope),
                    children = el.children(),
                    curChild = el.children()[0];

                expect(el.children().length).to.equal(1);
                expect(curChild.nodeName).to.equal('TRACK');
                expect(curChild.getAttribute('kind')).to.equal('subtitles');
                expect(curChild.getAttribute('label')).to.equal(
                    'english subtitles'
                );
                expect(curChild.getAttribute('src')).to.equal('subtitles.vtt');
                expect(curChild.getAttribute('srclang')).to.equal('en');
            });

            it('should generate multiple track DOM elements when specified', function() {
                scope.testMedia = {
                    tracks: [
                        {
                            kind: 'subtitles',
                            label: 'english subtitles',
                            src: 'subtitles.vtt',
                            srclang: 'en'
                        },
                        {
                            kind: 'captions',
                            label: 'portuguese subtitles',
                            src: 'subtitles_pt.vtt',
                            srclang: 'pt'
                        }
                    ]
                };

                var el = compileAndLink(vidWithMediaNoVals, scope),
                    children = el.children(),
                    curIdx,
                    curChild;

                expect(el.children().length).to.equal(2);

                for (curIdx = 0; curIdx < el.children().length; curIdx += 1) {
                    curChild = el.children()[curIdx];

                    expect(curChild.nodeName).to.equal('TRACK');
                    expect(curChild.getAttribute('kind')).to.equal(
                        scope.testMedia.tracks[curIdx].kind
                    );
                    expect(curChild.getAttribute('label')).to.equal(
                        scope.testMedia.tracks[curIdx].label
                    );
                    expect(curChild.getAttribute('src')).to.equal(
                        scope.testMedia.tracks[curIdx].src
                    );
                    expect(curChild.getAttribute('srclang')).to.equal(
                        scope.testMedia.tracks[curIdx].srclang
                    );
                }
            });

            it('should generate track DOM element with default tag when specified', function() {
                scope.testMedia = {
                    tracks: [
                        {
                            default: true
                        }
                    ]
                };

                var el = compileAndLink(vidWithMediaNoVals, scope),
                    children = el.children(),
                    curChild = el.children()[0];

                expect(el.children().length).to.equal(1);
                expect(curChild.nodeName).to.equal('TRACK');
                expect(curChild.getAttribute('default')).to.exist;
            });

            it('should generate track DOM element without default tag if false', function() {
                scope.testMedia = {
                    tracks: [
                        {
                            default: false
                        }
                    ]
                };

                var el = compileAndLink(vidWithMediaNoVals, scope),
                    children = el.children(),
                    curChild = el.children()[0];

                expect(el.children().length).to.equal(1);
                expect(curChild.nodeName).to.equal('TRACK');
                expect(curChild.getAttribute('default')).to.not.exist;
            });
        });
    });

    describe('vjs-video-container', function() {
        var vjsAttributeErrStr =
            'directive attributes should not be used on ' +
            'the video tag when using vjs-video-container!';

        it('should throw an error if container does not have a video tag defined', function() {
            expect(function() {
                var el = compileAndLink(nonVidContainerStr, scope);
            }).throws(
                Error,
                'video tag must be defined within container directive!'
            );
        });

        it('should throw an error if container defines more than one video tag', function() {
            expect(function() {
                compileAndLink(multVidsContainerStr, scope);
            }).throws(
                Error,
                'only one video can be defined within the container directive!'
            );
        });

        it('should throw an error if container defines more than one media tag', function() {
            expect(function() {
                compileAndLink(multMixedContainerStr, scope);
            }).throws(
                Error,
                'only one video can be defined within the container directive!'
            );
        });

        it('should attach videojs to the video tag', function() {
            //videojs should add at vjs-tech class to the element
            var el = compileAndLink(vidContainerStr, scope);
            expect(el.find('video').hasClass('vjs-tech')).to.be.true;
        });

        it('should attach videojs to the audio tag', function() {
            //videojs should add at vjs-tech class to the element
            var el = compileAndLink(audioContainerStr, scope);
            expect(el.find('audio').hasClass('vjs-tech')).to.be.true;
        });

        it('should register as the vjs-video-container element', function() {
            //videojs should add at vjs-tech class to the element
            var el = compileAndLink(vidElementContainerStr, scope);
            expect(el.find('video').hasClass('vjs-tech')).to.be.true;
        });

        it('should set width and height of included video to auto', function() {
            //video.js normally adds a style attribute to the surrounding
            //container if the video has a width or height
            //we want to confirm that no style tag exists

            //NOTE:It is probably crossing into too much of testing
            //video.js, I just haven't figure out a great way to stub
            //the functionality since it's critical for the directive
            var el = compileAndLink(vidContainerWithDimsStr, scope),
                vid = el.find('#vid-dim');

            expect(vid.attr('style')).to.not.exist;
        });

        it('should throw an error is vjs-video is defined on the video tag', function() {
            expect(function() {
                var el = compileAndLink(vidElementContainerVjsVidStr, scope);
            }).throws(
                Error,
                'vjs-video should not be used on the video tag when using vjs-video-container!'
            );
        });

        it('should throw an error is vjs-setup is defined on the video tag', function() {
            expect(function() {
                var el = compileAndLink(vidElementContainerVjsSetupStr, scope);
            }).throws(Error, vjsAttributeErrStr);
        });

        it('should throw an error is vjs-media is defined on the video tag', function() {
            expect(function() {
                var el = compileAndLink(vidElementContainerVjsMediaStr, scope);
            }).throws(Error, vjsAttributeErrStr);
        });

        it('should throw an error is vjs-ratio is defined on the video tag', function() {
            expect(function() {
                var el = compileAndLink(vidElementContainerVjsRatioStr, scope);
            }).throws(Error, vjsAttributeErrStr);
        });

        describe('vjs-ratio', function() {
            var ratioErrMsg =
                    'the ratio must either be "wide", "standard" or decimal values in the format of w:h',
                ratioZeroErrMsg =
                    'neither the width or height ratio can be zero!';

            it('should throw an error if an invalid string is provided', function() {
                expect(function() {
                    var el = compileAndLink(vidRatioCharStr, scope);
                }).to.throw(Error, ratioErrMsg);
            });

            it('should throw an error if invalid ratio is supplied', function() {
                expect(function() {
                    var el = compileAndLink(vidRatioInvalidStr, scope);
                }).to.throw(Error, ratioErrMsg);
            });

            it('should throw an error if width is a string', function() {
                expect(function() {
                    var el = compileAndLink(vidRatioInvalidWStr, scope);
                }).to.throw(Error, ratioErrMsg);
            });

            it('should throw an error if height is a string', function() {
                expect(function() {
                    var el = compileAndLink(vidRatioInvalidHStr, scope);
                }).to.throw(Error, ratioErrMsg);
            });

            it('should throw an error if width is zero', function() {
                expect(function() {
                    var el = compileAndLink(vidRatioWidthZeroStr, scope);
                }).to.throw(Error, ratioZeroErrMsg);
            });

            it('should throw an error if height is zero', function() {
                expect(function() {
                    var el = compileAndLink(vidRatioHeightZeroStr, scope);
                }).to.throw(Error, ratioZeroErrMsg);
            });
        });
    });

    describe('missing library', function() {
        it('should throw an error if videojs is not loaded', function() {
            //TOOD: currently, this must be the last test
            //      because it destroys the reference to videojs
            //      find a way to fix that
            expect(function() {
                var vjs = window.videojs,
                    el;

                window.videojs = undefined;
                el = compileAndLink(vidStr, scope);
                window.videojs = vjs;
            }).throws(Error);
        });
    });
});
