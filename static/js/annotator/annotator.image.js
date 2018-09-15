Annotator.Plugin.Image = function(element, types) {
    if ($('img', element).length === 0)
        return;
    return {
        traceMouse: false,
        pluginInit: function() {
            if (!Annotator.supported())
                return;
            let annotator = this.annotator;
            var startPoint = null;
            var activeRect = null;
            var imgWidth = $('img', element).width();
            var imgHeight = $('img', element).height();
            var type_count = 0;
            var highlights = [];
            var isTouchSupported = 'ontouchstart' in window;
            var prevTouch = null;
            for (let xi in types)
                type_count++;

            function modifyHighlightColor(annotation) {
                let highlight = highlights['d' + annotation.id];
                if (highlight && type_count > 0) {
                    $(highlight.div).css('border-color', types['t' + annotation.atype].color);
                }
            }

            function createHighlight(left, top, width, height, annotation) {
                var div = document.createElement('div');
                $(div).addClass('annotator-hl annotator-img-rect').css({
                    left: left + 'px',
                    top: top + 'px',
                    width: width + 'px',
                    height: height + 'px',
                });
                $('.annotator-wrapper', element).append(div);
                if (annotation) {
                    $(div).data('annotation', annotation)
                        .data('annotation-id', annotation.id);
                    div.rect = {
                        left: left,
                        top: top,
                        right: left + width,
                        bottom: top + height
                    };
                    highlights['d' + annotation.id] = {
                        'div': div,
                        'annotation': annotation
                    };
                    modifyHighlightColor(annotation);
                    $(div).off('mouseover');
                    $(div).on('mouseover', function(event) {
                        var pos = $(event.target).position();
                        var x = pos.left + event.offsetX;
                        var y = pos.top + event.offsetY;
                        var annotations = [];
                        for (let i in highlights) {
                            let highlight = highlights[i];
                            let rect = highlight.div.rect;
                            if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom)
                                annotations.push(highlight.annotation);
                        }
                        if (annotations.length > 1) {
                            window.setTimeout(function() {
                                annotator.showViewer(annotations, {
                                    left: x,
                                    top: y
                                });
                            }, 100);
                        }
                    });
                } else {
                    $(div).off('mouseover');
                    $(div).on('mouseover', function(event) {
                        event.preventDefault();
                        return false;
                    });
                    $(div).off('mousemove');
                    $(div).on('mousemove', function(event) {
                        event.preventDefault();
                        return false;
                    });
                }
                return div;
            }

            function markStart(point) {
                annotator.editor.hide();
                self.traceMouse = true;
                startPoint = {
                    x: point.x,
                    y: point.y
                };
                activeRect = createHighlight(point.x, point.y, 0, 0, null);
            }

            function markEnd(point) {
                self.traceMouse = false;
                startPoint = null;
                annotator.viewer.hide();
                annotator.showEditor({
                    text: ''
                }, {
                    left: point.x,
                    top: point.y
                });
            }

            function markMove(point) {
                $(activeRect).css({
                    left: Math.min(point.x, startPoint.x),
                    top: Math.min(point.y, startPoint.y),
                    width: Math.abs(point.x - startPoint.x) + 'px',
                    height: Math.abs(point.y - startPoint.y) + 'px'
                });
            }

            $('img', element).on('mousedown', function(e) {
                if (!annotator.options.readOnly && e.which === 1) {
                    markStart({
                        x: e.offsetX,
                        y: e.offsetY
                    });
                }
                return false;
            });

            $('img', element).on('mouseup', function(e) {
                if (!annotator.options.readOnly) {
                    markEnd({
                        x: e.offsetX,
                        y: e.offsetY
                    });
                }
                return false;
            });

            $('img', element).on('mousemove', function(e) {
                if (self.traceMouse) {
                    markMove({
                        x: e.offsetX,
                        y: e.offsetY
                    });
                    if (e.originalEvent.buttons === 0) {
                        e.type = 'mouseup';
                        $('img', element).trigger(e);
                    }
                }
                return false;
            });

            if (isTouchSupported) {
                $('img', element).on('touchstart', function(e) {
                    if (!annotator.options.readOnly) {
                        e.preventDefault();
                        markStart({
                            x: e.touches[0].pageX - e.target.x,
                            y: e.touches[0].pageY - e.target.y
                        });
                    }
                });
                $('img', element).on('touchend', function(e) {
                    if (!annotator.options.readOnly) {
                        e.preventDefault();
                        markEnd(prevTouch);
                    }
                });
                $('img', element).on('touchmove', function(e) {
                    if (self.traceMouse) {
                        e.preventDefault();
                        prevTouch = {
                            x: e.touches[0].pageX - e.target.x,
                            y: e.touches[0].pageY - e.target.y
                        };
                        markMove(prevTouch);
                    }
                });
            }

            this.annotator.subscribe("annotationsLoaded", function(annotations) {
                for (let i in annotations) {
                    let item = annotations[i];
                    var rect = item.shapes[0].geometry;
                    createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, item);
                }
            });

            this.annotator.subscribe('annotationEditorSubmit', function(editor, annotation) {
                var aid = annotation.id || 0;
                if (!aid) {
                    var rect = {
                        left: parseInt($(activeRect).css('left').slice(0, -2)),
                        top: parseInt($(activeRect).css('top').slice(0, -2)),
                        width: $(activeRect).width(),
                        height: $(activeRect).height(),
                    };
                    annotation.shapes = [{
                        geometry: {
                            y: rect.top / imgHeight,
                            x: rect.left / imgWidth,
                            width: rect.width / imgWidth,
                            height: rect.height / imgHeight,
                        },
                        style: {},
                    }];
                    annotator.publish('annotationCreated', annotation);
                } else
                    annotator.publish('annotationUpdated', annotation);
            });

            this.annotator.subscribe('annotationCreated', function(annotation) {
                var rect = annotation.shapes[0].geometry;
                (function verify_id() {
                    if (!annotation.id) {
                        window.setTimeout(verify_id, 5);
                    } else {
                        createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, annotation);
                    }
                })();
            });

            this.annotator.subscribe("annotationUpdated", function(annotation) {
                modifyHighlightColor(annotation);
            });

            this.annotator.subscribe("annotationEditorHidden", function(editor) {
                if (activeRect) {
                    $(activeRect).remove();
                    activeRect = null;
                }
            });

            this.annotator.subscribe("annotationDeleted", function(annotation) {
                let highlight = highlights['d' + annotation.id];
                if (highlight) {
                    $(highlight.div).remove();
                    delete highlights['d' + annotation.id];
                }
            });
        },
    }
}