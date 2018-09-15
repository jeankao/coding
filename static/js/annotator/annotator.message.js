Annotator.Plugin.Message = function(element, types) {
  /*
  if ($('img', element).length > 0)
    return;
  */
  function formatDateTime(d) {
    function _(n) {
      if (n < 10)
        return '0' + n;
      return '' + n;
    }
    return '' + d.getFullYear() + '/' + _(d.getMonth() + 1) + '/' + _(d.getDate()) + ' ' + _(d.getHours()) + ':' + _(d.getMinutes()) + ':' + _(d.getSeconds());
  }
  function modifyAnnotationClass(annotation) {
    if (annotation.highlights)
      $(annotation.highlights[0]).attr('class', 'annotator-hl atype-' + annotation.atype);
  }
  return {
    field: null,
    typefield: null,
    input: null,
    pluginInit: function() {
      if (!Annotator.supported())
        return;
      this.annotator.subscribe("annotationsLoaded", function(annotations) {
        for (let i in annotations) {
          let annoitem = annotations[i];
          modifyAnnotationClass(annoitem);
        }
      });
      this.annotator.subscribe("annotationCreated", modifyAnnotationClass);
      this.annotator.subscribe("annotationUpdated", modifyAnnotationClass);
      var type_count = 0;
      for (let xi in types) {
        type_count++;
      }
      if (type_count > 0) {
        this.annotator.editor.addField({
          type: 'select',
          load: function(field, annotation) {
            typeid = annotation['atype'] || 0;
            tagHTML = "<select id='annotation-type' class='form-control'>";
            for (var key in types) {
              tagHTML += "<option value='" + key.substr(1) + "' style='background-color: " + types[key].color + "'>" + types[key].kind + "</option>";
            }
            tagHTML += "</select>";
            $(field).html(tagHTML);
            if (typeid) {
              $('select', field).css('background-color', types['t'+typeid].color);
              $('select', field).change(function(e) {
                $(e.target).css('background-color', types['t'+$(e.target).val()].color);
              });
              $('#annotation-type').val(typeid);
            }
          },
          submit: function(field, annotation) {
            annotation.atype = $(field).find(':selected').val();
          },
        });
        this.annotator.viewer.addField({
          load: function(field, annotation) {
            typeid = annotation['atype'] || 0;
            field = $(field);
            if ((type = types['t' + typeid]) || 0)
              return field.addClass('annotator-hl atype-' + typeid).html(type.kind);
            return field.html('類別尚未指定');
          },
        });
      }
      this.annotator.viewer.addField({
        load: function(field, annotation) {
          field.innerHTML = field.innerHTML = formatDateTime(new Date(annotation.created)) + " | " + annotation.supervisor;
        }
      });
    },
  };
}