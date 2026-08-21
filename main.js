// PRIME STRUCTURES — proof pages
// Motion: assembly/consequence. One easing, reveals fire once,
// load-path draws with scroll, reduced-motion respected.

(function () {
  if (location.search.indexOf('static') !== -1) { document.documentElement.classList.add('static'); }

  var header = document.querySelector('.site-header');
  var isStatic = document.documentElement.classList.contains('static');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Reveals — position sweep (robust against fast scroll jumps), fires once
  var revealables = Array.prototype.slice.call(
    document.querySelectorAll('.reveal, .wipe, .reveal-rule')
  );

  var gauge = document.querySelector('.gauge span');

  // Load path — structural datum: line spans standfirst → kontakt,
  // draws with scroll, yellow nodes light when the line reaches them.
  var loadpath = document.querySelector('.loadpath');
  var lpLine = loadpath && loadpath.querySelector('.lp-line');
  var lpNodes = loadpath ? Array.prototype.slice.call(loadpath.querySelectorAll('.lp-node')) : [];
  var lpTop = 0, lpHeight = 0;

  function layoutLoadpath() {
    if (!loadpath) return;
    var end = document.querySelector('#kontakt');
    if (!end) return;
    var endR = end.getBoundingClientRect();
    var mainR = loadpath.parentElement.getBoundingClientRect();
    lpTop = 0;
    lpHeight = (endR.top - mainR.top + endR.height * 0.55) - lpTop;
    loadpath.style.top = lpTop + 'px';
    loadpath.style.height = lpHeight + 'px';
    lpNodes.forEach(function (node) {
      var anchor = document.querySelector(node.getAttribute('data-anchor'));
      if (!anchor) return;
      var aR = anchor.getBoundingClientRect();
      var y = (aR.top - mainR.top) + aR.height * 0.5 - lpTop;
      node.style.top = Math.max(0, Math.min(y, lpHeight - 8)) + 'px';
    });
  }

  // Ablauf — the plan sheet draws itself once, when the section comes
  // into view. Deliberately time-based rather than scroll-scrubbed:
  // scroll position at load (restored scroll, anchor jumps) used to put
  // the sequence at 100% before it had ever been seen.
  // No-ops on every page without a process rail.
  var rail = document.querySelector('.process-rail');
  var procSection = rail && rail.closest('section');
  var pDots = rail ? Array.prototype.slice.call(rail.querySelectorAll('i')) : [];
  var pSteps = Array.prototype.slice.call(document.querySelectorAll('.process-step'));
  var procRun = false;
  var PROC_DRAW = 2400;   // ms for the line to travel 01 -> 04

  function armProcess() {
    if (!procSection || procRun) return;
    var r = procSection.getBoundingClientRect();
    if (r.top > window.innerHeight * 0.72 || r.bottom < 0) return;
    procRun = true;
    // Feed the real point offsets into the stage clock so the line
    // stops exactly on each point. Delays live in CSS; only the
    // geometry is measured here.
    var w = rail.offsetWidth;
    if (w > 0) {
      for (var i = 1; i < pDots.length; i++) {
        rail.style.setProperty('--f' + i, (pDots[i].offsetLeft / w).toFixed(4));
      }
    }
    procSection.classList.add('seq--run');
  }

  if (procSection) {
    procSection.classList.add('seq');
    // Reduced motion / QA: the finished drawing, with nothing moving.
    if (isStatic || reduced) procSection.classList.add('seq--done');
  }

  var ticking = false;

  function sweep() {
    ticking = false;
    header.classList.toggle('scrolled', window.scrollY > 8);

    var vh = window.innerHeight;

    revealables = revealables.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh - 40 || r.bottom < vh) {
        el.classList.add('in');
        return false;
      }
      return true;
    });

    if (loadpath && lpLine && lpHeight > 0 && !isStatic && !reduced) {
      var mainTop = loadpath.parentElement.getBoundingClientRect().top + window.scrollY;
      var drawnTo = window.scrollY + vh * 0.72 - (mainTop + lpTop);
      var p = Math.max(0, Math.min(drawnTo / lpHeight, 1));
      lpLine.style.transform = 'scaleY(' + p + ')';
      lpNodes.forEach(function (node) {
        if (parseFloat(node.style.top || '0') <= drawnTo) node.classList.add('lit');
      });
    }
    if (loadpath && (isStatic || reduced)) {
      lpNodes.forEach(function (n) { n.classList.add('lit'); });
    }

    if (procSection && !isStatic && !reduced) armProcess();

    if (gauge) {
      var h = document.documentElement.scrollHeight - vh;
      gauge.style.height = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    }
  }

  // Sync sweep: cheap enough per-frame, and immune to rAF/timer
  // throttling in hidden or backgrounded tabs.
  function onScroll() { sweep(); }

  function relayout() { layoutLoadpath(); onScroll(); }

  // Project index filter (yellow underline = active state)
  var fbtns = document.querySelectorAll('.fbtn');
  if (fbtns.length) {
    fbtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-f');
        fbtns.forEach(function (b) { b.classList.toggle('active', b === btn); });
        document.querySelectorAll('.pi-entry').forEach(function (e) {
          e.classList.toggle('hidden', f !== 'alle' && e.getAttribute('data-cat') !== f);
        });
        var t2 = document.querySelector('.pi-tier2');
        if (t2) {
          t2.style.display = (f === 'alle' || f === t2.getAttribute('data-cat-block')) ? '' : 'none';
        }
        relayout();
      });
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', relayout, { passive: true });
  window.addEventListener('load', relayout);
  layoutLoadpath();
  sweep();
})();
