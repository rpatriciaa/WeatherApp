var CookieLawBar = CookieLawBar || {

    getCookie: function(c) {
        return (c=(document.cookie.match('(^|; )'+ c +'=([^;]*)')||0)[2]) && decodeURIComponent(c);
    },

    setCookie: function(name, value, days) {
        var cookie = name + '=' + encodeURIComponent(value);
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            cookie += ';expires=' + date.toGMTString();
        }
        cookie += ';path=/';
        document.cookie = cookie;
    },

    slideUp: function(el, pos) {
        var _this = this;
        setTimeout(function() {
            el.style.display = 'block';
            el.style[pos] = '-' + el.offsetHeight + 'px';
            el.style.display = 'none';
            setTimeout(function() {
                el.style.display = 'block';
                _this.addcl(el, 'cookie-law-bar-transition-' + pos);
                setTimeout(function() {
                    el.style[pos] = '0px';
                    if (pos == 'top') {
                        _this.addcl(document.body, 'cookie-law-bar-body-slide');
                    }
                }, 30);
            }, 30);
        }, 500);
    },

    slideDown: function(el, pos) {
        el.style[pos] = '-' + el.offsetHeight + 'px';
        setTimeout(function() {
            el.style.display = 'none';
        }, 500);
    },

    addcl: function(el, cl) {
        if (el && el.className.indexOf(cl) < 0) {
            el.className += ' ' + cl;
            el.className = el.className.trim();
        }
    },

    remcl: function(el, cl) {
        el && (el.className = el.className.replace(cl, ' '));
    }
};

function clb_accept() {
    var bar = document.querySelector('#cookie-law-bar');
    CookieLawBar.setCookie('cookie-law-bar', 'accept', 365);
    if (bar.style.bottom == '0px') {
        CookieLawBar.slideDown(bar, 'bottom');
    } else {
        CookieLawBar.slideDown(bar, 'top');
        CookieLawBar.remcl(document.body, 'cookie-law-bar-body-slide');
        setTimeout(function() {
            CookieLawBar.remcl(document.body, 'cookie-law-bar-body');
        }, 530);
    }
}

jQuery(document).ready(function($) {
    var bar = document.querySelector('#cookie-law-bar');
    if (CookieLawBar.getCookie('cookie-law-bar') != 'accept') {
        if (bar.style.bottom == '0px') {
            CookieLawBar.slideUp(bar, 'bottom');
        } else {
            CookieLawBar.slideUp(bar, 'top');
            CookieLawBar.addcl(document.body, 'cookie-law-bar-body');
        }
    }
});