$(function () {
  const CS_VAR = 'btn-warning', 
        CS_ARR = 'btn-danger', 
        CS_CONST = 'btn-success',
        CS_OP = 'btn-info';

  const BCLASS = {
    'var': CS_VAR, 
    'arr': CS_ARR, 
    'str-const': CS_CONST, 
    'num-const': CS_CONST,
    'op': CS_OP,
  };

  const TYPELIST = {
    'vars': 'var', 
    'strs': 'str-const',
    'nums': 'num-const',
  };

  function getType(token) {
    if (token.includes('['))
      return 'arr';
    if (token.includes("'"))
      return 'str-const';
    if (token.match(/^\d+$/))
      return 'num-const';
    if (token.match(/[\(\)+\-*\/^]/))
      return 'op';
    return 'var';
  }

  function newBlock(type, item, target) {
    var element = $('<li class="btn btn-sm expr-item '+type+' '+BCLASS[type]+'">' + item + '</li>');
    element.appendTo($(target));
    return element;
  }

  function newExprBlock(setEventHandler = false) {
    var expr = $('<div class="expr"><ul class="expr-lhs expr-item-list"></ul> <ul class="d-inline-block pl-0"><li class="btn btn-dark btn-sm">=</li></ul> <ul class="expr-rhs expr-item-list"></ul></div>');

    if (setEventHandler) {
      $('.expr-lhs', expr).sortable({
        receive: function (event, ui) {
          $(this).empty().append($(ui.item).clone());
        },
      }).disableSelection();
  
      $('.sortable', expr).sortable({
        connectWith: '.expr-trash',
      }).disableSelection();  
    }
    expr.appendTo('#expr-list');
    return expr;
  }

  function newArrBlock(name, size) {
    var wrapper = $('<ul class="expr-item-list" data-name="'+name+'" data-size="'+size+'"></ul>');
    for (var i = 0; i < size; i++) {
      newBlock('arr', i, wrapper);
    }
    wrapper.appendTo($('<li class="arr-wrapper"><span class="btn btn-sm btn-danger">'+name+'</span></li>').appendTo($('#arr-list')));
    return wrapper;
  }

  function initExprElements() {
    // init vars, strs, nums
    for (key in TYPELIST) {
      var items = exprjson[key];
      for (id in items) {
        item = items[id];
        newBlock(TYPELIST[key], item, '#'+TYPELIST[key]+'-list');
      }  
    }
    // init arrs
    for (id in exprjson['arrs']) {
      var arr = exprjson['arrs'][id];
      newArrBlock(arr.name, arr.size);
    }
    // init expression
    for (id in exprjson['exprs']) {
      var expr = exprjson['exprs'][id];
      var tokens = expr.match(/('[^']+'|[\w\d]+(\[\d+\])?|[\(\)+\-*\/])/g);
      expr = newExprBlock();
      newBlock(getType(tokens[0]), tokens[0], $('.expr-lhs', expr));
      for (var i = 1; i < tokens.length; i++) {
        token = tokens[i];
        newBlock(getType(token), token, $('.expr-rhs', expr));
      }
    }
  }

  initExprElements();

  $('#new-element').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var title = button.text();
    var modal = $(this);

    $('#elementName').attr('pattern', button.data('pattern'));
    $('#elementName').val('');
    if (button.data('type') === 'num-const') {
      $('#elementName').attr('type', 'number');
    } else {
      $('#elementName').attr('type', '');
    }
    if (button.data('type') === 'arr') {
      $('#form-group-elementNumber').css('display', 'block');
    } else {
      $('#form-group-elementNumber').css('display', 'none');
    }

    modal.data('type', button.data('type'));
    modal.data('class', button.data('class'));
    modal.find('.modal-title').text(title);
    $('#elementName').val('').focus();
  });

  function createNewElement() {
    var input = $('#elementName').val().trim();
    if (input !== "") {
      var type = $('#new-element').data('type');
      var bclass = $('#new-element').data('class');
      var list_id = '#' + type + '-list';
      var connectTo = ".expr-rhs, .expr-trash";
      if (type === "var" || type == "arr") {
        connectTo += ", .expr-lhs";
      }
      if (type === "arr" && $('#elementNumber').val().trim()) {
        var capacity = parseInt($('#elementNumber').val().trim());
        var wrapper = newArrBlock(input, capacity);
        $('.expr-item', wrapper).draggable({
          connectToSortable: connectTo,
          revert: "invalid",
          helper: function() {
            var name = $(this).parent().data('name');
            if ($(this).hasClass('expr-item arr'))
              return $(this).clone().prepend(name+'[').append(']');
            return $(this).clone();
          },
        });
      } else {
        if (type==="str-const")
          input = "'" + input + "'";
        
        newBlock(type, input, list_id).draggable({
          connectToSortable: connectTo,
          helper: "clone",
          revert: "invalid",
        });
        $('#elementName').val('').focus();
      }
    }
  }

  $('#new-element-ok').click(createNewElement);

  $('#elementName').on('keypress', function (event) {
    if (event.which === 13) {
      event.preventDefault();
      createNewElement();
      $('#elementName').val('').focus();
    }
  });

  $('#new-exp').click(function() {
    newExprBlock(true);
  });

  $('.card-header .expr-item').draggable({
    connectToSortable: '.expr-rhs',
    helper: "clone",
    revert: "invalid",
  });

  $('.card-header .expr-item.str-const, .card-header .expr-item.num-const').draggable({
    connectToSortable: '.expr-rhs, .expr-trash',
    helper: "clone",
    revert: "invalid",
  });

  $('.card-header .expr-item.var, .card-header .expr-item.arr').draggable({
    connectToSortable: '.expr-rhs, .expr-lhs, .expr-trash',
    revert: "invalid",
    helper: function() {
      var name = $(this).parent().data('name');
      if ($(this).hasClass('expr-item arr'))
        return $(this).clone().prepend(name+'[').append(']');
      return $(this).clone();
    },
  });

  $('.expr-lhs').sortable({
    receive: function (event, ui) {
      $(this).empty().append($(ui.helper).clone());
    },
  }).disableSelection();

  $('.expr-rhs').sortable({
    receive: function(event, ui) {
      var item = $(ui.helper);
      if (item.hasClass('expr-item arr')) {
        var name = item.parent().data('name');
        //console.log(ui);
        item.prepend(name);
        //$(this).empty().append(item.clone().prepend(name));
      }
    },
  }).disableSelection();

  $('.expr-trash').sortable({
    receive: function (event, ui) {
      console.log(ui);      
      $(ui.item).detach();
      $(ui.helper).detach();
    }
  });

  $('.expr-lhs, .expr-rhs, .expr-list').sortable({
    connectWith: '.expr-trash',
  }).disableSelection();

  $('.expr-arr-list').sortable({
    connectWith: '.expr-trash',
  }).disableSelection();
  //-------------------------------------------------------------------------
  // 送出答案
  $('#expr-submit').click(function() {
    var data = {
      vars: [], 
      arrs: [],
      strs: [],
      nums: [],
      exprs: [],
    };

    for (var key in TYPELIST) {
      $('.expr-item', '#'+TYPELIST[key]+'-list').each(function(index, obj) {
        data[key].push($(obj).text());
      });  
    }

    $('.expr-item-list', '#arr-list').each(function(index, obj) {
      var size = $('.expr-item', $(obj)).length;
      data['arrs'].push({name: $(obj).data('name'), size: size});
    });

    $('.expr', '#expr-list').each(function(index, obj) {
      var tokens = [];
      $('li', $(obj)).each(function(index, item) {
        tokens.push($(item).text());
      });
      data['exprs'].push(tokens.join(' '));
    });    
    $('#jsonstr').val(JSON.stringify(data));
    $('#expr-form').submit();
  });
});