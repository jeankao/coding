var markdown = $(".markdown-body");
//smooth all hash trigger scrolling
function smoothHashScroll() {
  var hashElements = $("a[href^='#']").toArray();
  for (var i = 0; i < hashElements.length; i++) {
    var element = hashElements[i];
    var $element = $(element);
    var hash = element.hash;
    if (hash) {
      $element.on('click', function (e) {
        // store hash
        var hash = this.hash;
        hash = decodeURIComponent(hash);

        if ($(hash).length <= 0) return;
        // prevent default anchor click behavior
        e.preventDefault();
        //window.location.hash = hash;                      
        // animate
        $('body, html').animate({
          scrollTop: ($(hash).offset().top) - $('#topnav').height(),
        }, 500, "linear", function () {
          // when done, add hash to url
          // (default click behaviour)
        });
      });
    }
  }
}

smoothHashScroll();
var toc = $('.ui-toc');
var tocAffix = $('.ui-affix-toc');
var tocDropdown = $('.ui-toc-dropdown');
//toc
tocDropdown.click(function (e) {
  e.stopPropagation();
});

var enoughForAffixToc = true;

var docTitles = [];
var activeTitle = null;
var offsetFix = $('#topnav').height();
var titleCount = 0;

function generateScrollspy() {
  $('#doc h1, #doc h2, #doc h3').each(function () {
    var $this = $(this);
    var position = $this.position();
    docTitles.push({
      obj: $this,
      pos: position
    });
    titleCount++;
  });
  if (enoughForAffixToc) {
    toc.hide();
    tocAffix.show();
  } else {
    tocAffix.hide();
    toc.show();
  }
}

function windowResize() {
  //toc right
  var paddingRight = parseFloat(markdown.css('padding-right'));
  var right = ($(window).width() - (markdown.offset().left + markdown.outerWidth() - paddingRight));
  toc.css('right', right + 'px');
  //affix toc left
  var newbool;
  var rightMargin = (markdown.parent().outerWidth() - markdown.outerWidth());
  //for ipad or wider device
  if (rightMargin >= 133) {
    newbool = true;
    var affixLeftMargin = (tocAffix.outerWidth() - tocAffix.width()) / 2;
    var left = markdown.offset().left + markdown.outerWidth() - affixLeftMargin;
    tocAffix.css('left', left + 'px');
  } else {
    newbool = false;
  }
  if (newbool != enoughForAffixToc) {
    enoughForAffixToc = newbool;
    generateScrollspy();
  }
}
$(window).resize(function () {
  windowResize();
});
$(document).ready(function () {
  windowResize();
  generateScrollspy();
  $(window).scroll(function () {
    var scroll_top = $(this).scrollTop();
    for (i = 0; i < titleCount; i++) {
      var titem = docTitles[i];
      if (i < titleCount - 1) {
        if (scroll_top >= titem.pos.top - offsetFix &&
          ((i < titleCount - 1 && scroll_top < docTitles[i + 1].pos.top - offsetFix) || i == titleCount - 1)) {
          if (activeTitle !== titem.obj) {
            activeTitle = titem.obj;
            $('.toc>.nav li').removeClass('active');
            $('.toc>.nav a[href="#' + activeTitle.context.id + '"]').parent().addClass('active');
          }
        }
      }
    }
  });
});

//remove hash
function removeHash() {
  window.location.hash = '';
}

var backtotop = $('.back-to-top');
var gotobottom = $('.go-to-bottom');

backtotop.click(function (e) {
  e.preventDefault();
  e.stopPropagation();
  if (scrollToTop)
    scrollToTop();
  removeHash();
});
gotobottom.click(function (e) {
  e.preventDefault();
  e.stopPropagation();
  if (scrollToBottom)
    scrollToBottom();
  removeHash();
});

var toggle = $('.expand-toggle');
var tocExpand = true;

checkExpandToggle();
toggle.click(function (e) {
  e.preventDefault();
  e.stopPropagation();
  tocExpand = !tocExpand;
  checkExpandToggle();
})

function checkExpandToggle() {
  var toc = $('.ui-toc-dropdown .toc');
  var toggle = $('.expand-toggle');
  if (!tocExpand) {
    toc.removeClass('expand');
    toggle.text('Expand all');
  } else {
    toc.addClass('expand');
    toggle.text('Collapse all');
  }
}

function scrollToTop() {
  $('body, html').stop(true, true).animate({
    scrollTop: 0
  }, 100, "linear");
}

function scrollToBottom() {
  $('body, html').stop(true, true).animate({
    scrollTop: $(document.body)[0].scrollHeight
  }, 100, "linear");
}