Annotator.Plugin.Image = function (element) {
  if ($('img', element).length === 0)
    return;

  return {
    pluginInit: function() {
      if (!Annotator.supported())
        return;
      let annotator = this.annotator;
      //-----------------------------------------------------------------------
      // Annotorious integration
      anno.addHandler('onAnnotationCreated', function(annotation, info) {
        if ($(annotator.element[0]).find(info.element).length === 0)
          return;
        var xanno = Object.assign({}, annotation);
        xanno.context = (new URL(annotation.context)).pathname;
        xanno.src = (new URL(annotation.src)).pathname;
        annotator.publish('annotationCreated', xanno);
        console.log("Create: ", xanno, ta, tb);
        console.log(annotator);
      });
      anno.addHandler('onAnnotationUpdated', function(annotation, info) {
        if ($(annotator.element[0]).find(info.element).length === 0)
          return;
        var obj = annotator.plugins.Store.options.annotationData;
        var annoitem = Object.assign(obj, annotation);
        annoitem.src = (new URL(annotation.src)).pathname;
        //annotator.publish('annotationUpdated', annoitem);
        console.log(annoitem);
        var url = (annotator.plugins.Store.options.prefix + annotator.plugins.Store.options.urls.update);
        url = url.replace(/:id/, annoitem.id);
        console.log(url);
        $.ajax({
          'url': url,
          'method': 'PUT',
          'data': annoitem,
        });
        console.log("Update: ", annoitem);
        return 
      });
      anno.addHandler('onAnnotationRemoved', function(annotation) {
        if ($(annotator.element[0]).find(info.element).length === 0)
          return;
        annotator.publish('annotationDeleted', Object.assign({}, annotation));
        console.log("Remove: ", annotation);
      });
      this.annotator.subscribe("annotationUpdated", function(annotation) {
        console.log("annotationUpdated", annotation);
      });
      this.annotator.subscribe("annotationsLoaded", function(annotations) {
        console.log('Loading....');
        for(let annoitem of annotations) {
          var xanno = Object.assign({}, annoitem);
          console.log('    ', xanno);
          anno.addAnnotation(xanno);
        }
        console.log('==========================================================================');
      });
      this.annotator.subscribe('mouseDown', function(e) {
        console.log('mouseDown', e);
      });
      this.annotator.subscribe('mouseUp', function(e) {
        console.log('mouseUp', e);
      });
    },
  }
}
