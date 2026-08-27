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
  var mobileMenu = document.getElementById('mobile-menu');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  if (mobileMenu && toggle) {
    Array.prototype.slice.call(mobileMenu.querySelectorAll('nav a')).forEach(function (link) {
      link.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
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
    var end = document.querySelector('#ablauf');
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

  // Ablauf — looping step highlight.
  // One step active at a time, ~3 s per step, cycling 01 -> 02 -> 03 -> 04 -> 01 ...
  // Starts when the section enters the viewport; pauses/respects reduced motion.
  var rail = document.querySelector('.process-rail');
  var procSection = rail && rail.closest('section');
  var pDots = rail ? Array.prototype.slice.call(rail.querySelectorAll('i')) : [];
  var pSteps = Array.prototype.slice.call(document.querySelectorAll('.process-step'));
  var procInterval = null;
  var currentStep = 0;
  var STEP_DURATION = 3000;

  function updateActiveStep() {
    pSteps.forEach(function (step, i) {
      step.classList.toggle('active', i === currentStep);
    });
    pDots.forEach(function (dot, i) {
      dot.classList.toggle('active', i === currentStep);
    });
    currentStep = (currentStep + 1) % pSteps.length;
  }

  function startProcessLoop() {
    if (procInterval || !pSteps.length) return;
    procSection.classList.add('seq');
    updateActiveStep();
    procInterval = setInterval(updateActiveStep, STEP_DURATION);
  }

  function stopProcessLoop() {
    if (procInterval) {
      clearInterval(procInterval);
      procInterval = null;
    }
  }

  function isProcessInView() {
    if (!procSection) return false;
    var r = procSection.getBoundingClientRect();
    return r.top < window.innerHeight && r.bottom > 0;
  }

  if (procSection && !isStatic && !reduced) {
    if (isProcessInView()) startProcessLoop();
    window.addEventListener('scroll', function () {
      if (isProcessInView()) {
        startProcessLoop();
      } else {
        stopProcessLoop();
      }
    }, { passive: true });
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

  // Contact form — Formspree AJAX submission (no redirect)
  var contactForm = document.querySelector('.contact-form[data-formspree]');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var parent = contactForm.parentElement;
      var successState = parent.querySelector('.form-state--success');
      var errorState = parent.querySelector('.form-state--error');
      var submitBtn = contactForm.querySelector('button[type="submit"]');
      var originalBtnHTML = submitBtn ? submitBtn.innerHTML : '';

      if (errorState) {
        errorState.hidden = true;
        errorState.classList.remove('is-visible');
      }
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Wird gesendet…';
      }

      var formData = new FormData(contactForm);
      fetch(contactForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      })
      .then(function (response) {
        if (response.ok) {
          contactForm.style.display = 'none';
          if (successState) {
            successState.hidden = false;
            successState.classList.add('is-visible');
            successState.focus();
          }
        } else {
          throw new Error('Formspree responded with ' + response.status);
        }
      })
      .catch(function () {
        if (errorState) {
          errorState.hidden = false;
          errorState.classList.add('is-visible');
          errorState.focus();
        }
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnHTML;
        }
      });
    });
  }

  // File-upload UX: show selected filenames, sizes and removable list
  document.querySelectorAll('.dropzone input[type="file"]').forEach(function (input) {
    var dropzone = input.closest('.dropzone');
    if (!dropzone) return;
    var list = dropzone.querySelector('.dropzone__files');
    if (!list) {
      list = document.createElement('span');
      list.className = 'dropzone__files';
      list.setAttribute('aria-live', 'polite');
      dropzone.appendChild(list);
    }

    function formatSize(bytes) {
      if (bytes === 0) return '0 KB';
      if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' KB';
      return (Math.round(bytes / (1024 * 1024) * 10) / 10) + ' MB';
    }

    function renderFiles() {
      var files = input.files;
      list.innerHTML = '';
      if (!files || files.length === 0) return;

      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var item = document.createElement('span');
        item.className = 'dropzone__file';

        var nameSpan = document.createElement('span');
        nameSpan.className = 'dropzone__file-name';
        nameSpan.textContent = file.name;

        var metaSpan = document.createElement('span');
        metaSpan.className = 'dropzone__file-meta';
        metaSpan.textContent = formatSize(file.size);

        var remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'dropzone__file-remove';
        remove.setAttribute('aria-label', 'Datei entfernen');
        remove.innerHTML = '<span aria-hidden="true">×</span>';
        (function (idx) {
          remove.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            var dt = new DataTransfer();
            var current = input.files;
            for (var j = 0; j < current.length; j++) {
              if (j !== idx) dt.items.add(current[j]);
            }
            input.files = dt.files;
            renderFiles();
          });
        })(i);

        item.appendChild(nameSpan);
        item.appendChild(metaSpan);
        item.appendChild(remove);
        list.appendChild(item);
      }
    }

    input.addEventListener('change', renderFiles);
  });
})();
