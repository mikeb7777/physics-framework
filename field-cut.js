/* Sim A: the information-density field in 3D, with a section cut you can move
   (2 Oct 2026). Michael: the old mesh looked like a sheet; show the field in 3D and let a
   slider take a section cut along any line, since a sheet is only one cut. The rubber
   sheet is the classic case of a picture that teaches the wrong thing (IC2-TOOL-002).

   Field: three wells drift on slow orbits. Around each, density falls off with distance
   (the pull inward) and carries outgoing ripples, so the field changes through time.
   Left: the field as a glowing 3D cloud (drag to turn it) and the cut plane. Right: the
   cut itself as a live heatmap in viridis. An illustration of the framework's equations,
   not measured data. Requires three.js (already on the page). */
(function () {
  var WELLS = [
    { r: 0.62, w: 0.35, ph: 0.0, tilt: 0.5, m: 1.0 },
    { r: 0.48, w: -0.27, ph: 2.1, tilt: -0.8, m: 0.8 },
    { r: 0.30, w: 0.52, ph: 4.0, tilt: 1.2, m: 0.65 }
  ];
  function wellPos(k, t) {
    var W = WELLS[k], a = W.ph + W.w * t;
    var x = W.r * Math.cos(a), z = W.r * Math.sin(a);
    return [x, z * Math.sin(W.tilt) * 0.6, z * Math.cos(W.tilt)];
  }
  /* density at point p and time t, in 0..1 */
  function field(px, py, pz, t, P) {
    var v = 0;
    for (var k = 0; k < 3; k++) {
      var dx = px - P[k][0], dy = py - P[k][1], dz = pz - P[k][2];
      var d = Math.sqrt(dx * dx + dy * dy + dz * dz);
      var m = WELLS[k].m;
      v += m * 0.055 / (d * d + 0.012);                                    // the pull: dense near the well
      v += m * 0.34 * Math.sin(16 * d - 3.2 * t) * Math.exp(-1.7 * d);     // ripples moving outward in time
    }
    return Math.max(0, Math.min(1, 1 - Math.exp(-Math.max(0, 0.12 + v * 0.5) * 1.6)));
  }
  function viridis(t) {
    t = Math.max(0, Math.min(1, t));
    var s = [[68,1,84],[72,40,120],[62,74,137],[49,104,142],[38,130,142],[31,158,137],[53,183,121],[109,205,89],[180,222,44],[253,231,37]];
    var x = t * (s.length - 1), i = Math.floor(x), f = x - i;
    if (i >= s.length - 1) return s[s.length - 1];
    var a = s[i], b = s[i + 1];
    return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
  }

  function start() {
    var wrap = document.getElementById('w-field'), canvas = document.getElementById('c-field'), heat = document.getElementById('c-cut');
    if (!wrap || !canvas || !heat || !window.THREE) return;
    var THREE = window.THREE;
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x020408, 1);
    var camera = new THREE.PerspectiveCamera(42, 1, 0.05, 50);
    var dist = 4.6;
    var scene = new THREE.Scene();
    function size() {
      var r = wrap.getBoundingClientRect(), w = Math.max(200, Math.floor(r.width)), h = Math.max(200, Math.floor(r.height));
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
      dist = camera.aspect < 1 ? 4.6 / Math.pow(camera.aspect, 0.85) : 4.6; if (typeof cam === 'function' && camera.position.lengthSq()) cam();   // pull back on narrow screens
    }
    size(); window.addEventListener('resize', size);

    /* the cloud: a 3D grid of points whose brightness is the density */
    var N = 30, pts = [], pos = new Float32Array(N * N * N * 3), col = new Float32Array(N * N * N * 3), i3 = 0;
    for (var a = 0; a < N; a++) for (var b = 0; b < N; b++) for (var c = 0; c < N; c++) {
      var J = 0.6 / (N - 1), x = -1 + 2 * a / (N - 1) + (Math.random() - 0.5) * J, y = -1 + 2 * b / (N - 1) + (Math.random() - 0.5) * J, z = -1 + 2 * c / (N - 1) + (Math.random() - 0.5) * J;   // jitter breaks moire
      pos[i3] = x; pos[i3 + 1] = y; pos[i3 + 2] = z; pts.push([x, y, z]); i3 += 3;
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    var cloud = new THREE.Points(geo, new THREE.PointsMaterial({ size: 0.06, vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
    scene.add(cloud);
    var box = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(2, 2, 2)), new THREE.LineBasicMaterial({ color: 0x3a4a5c }));
    scene.add(box);
    var wellMeshes = WELLS.map(function () { var s = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffd700 })); scene.add(s); return s; });

    /* the cut plane */
    var plane = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 2.6), new THREE.MeshBasicMaterial({ color: 0xf1e303, transparent: true, opacity: 0.14, side: THREE.DoubleSide, depthWrite: false }));
    var rim = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(2.6, 2.6)), new THREE.LineBasicMaterial({ color: 0xf1e303 }));
    plane.add(rim); scene.add(plane);

    /* orbit by dragging */
    var theta = 0.7, phi = 1.15, drag = false, ox = 0, oy = 0, idleSpin = true;
    function cam() { camera.position.set(dist * Math.sin(phi) * Math.sin(theta), dist * Math.cos(phi), dist * Math.sin(phi) * Math.cos(theta)); camera.lookAt(0, 0, 0); }
    size(); cam();
    function down(x, y) { drag = true; ox = x; oy = y; idleSpin = false; }
    function move(x, y) { if (!drag) return; theta -= (x - ox) * 0.008; phi = Math.max(0.15, Math.min(Math.PI - 0.15, phi + (y - oy) * 0.008)); ox = x; oy = y; cam(); }
    wrap.addEventListener('mousedown', function (e) { down(e.clientX, e.clientY); });
    window.addEventListener('mouseup', function () { drag = false; });
    wrap.addEventListener('mousemove', function (e) { move(e.clientX, e.clientY); });
    wrap.addEventListener('touchstart', function (e) { down(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });
    window.addEventListener('touchend', function () { drag = false; });
    wrap.addEventListener('touchmove', function (e) { move(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });

    /* sliders: direction of the cut (around the vertical), tilt, and position along its normal */
    var sAng = document.getElementById('cut-angle'), sTilt = document.getElementById('cut-tilt'), sOff = document.getElementById('cut-offset');
    var lab = document.getElementById('cut-readout'), play = document.getElementById('cut-play');
    var running = true;
    if (play) play.addEventListener('click', function () { running = !running; play.textContent = running ? 'Pause' : 'Play'; play.setAttribute('aria-pressed', String(!running)); });
    function basis() {
      var th = (+sAng.value) * Math.PI / 180, tl = (+sTilt.value) * Math.PI / 180, off = +sOff.value / 100;
      var n = new THREE.Vector3(Math.cos(tl) * Math.cos(th), Math.sin(tl), Math.cos(tl) * Math.sin(th)).normalize();
      var helper = Math.abs(n.y) > 0.9 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0);
      var u = new THREE.Vector3().crossVectors(helper, n).normalize(), v = new THREE.Vector3().crossVectors(n, u).normalize();
      return { n: n, u: u, v: v, c: n.clone().multiplyScalar(off) };
    }
    var hctx = heat.getContext('2d'), HN = 120, img = hctx.createImageData(HN, HN);
    var off = document.createElement('canvas'); off.width = off.height = HN; var octx = off.getContext('2d');

    var t = 0, last = performance.now(), visible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(wrap);
    function frame(now) {
      requestAnimationFrame(frame);
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (!visible) return;
      if (running) t += dt;
      if (idleSpin && !drag) { theta += dt * 0.12; cam(); }
      var P = [wellPos(0, t), wellPos(1, t), wellPos(2, t)];
      for (var k = 0; k < 3; k++) wellMeshes[k].position.set(P[k][0], P[k][1], P[k][2]);
      /* cloud colors */
      for (var j = 0, q = 0; j < pts.length; j++, q += 3) {
        var d = field(pts[j][0], pts[j][1], pts[j][2], t, P), g = 0.05 + 0.95 * Math.pow(d, 1.5), c = viridis(d);
        col[q] = c[0] / 255 * g; col[q + 1] = c[1] / 255 * g; col[q + 2] = c[2] / 255 * g;
      }
      geo.attributes.color.needsUpdate = true;
      /* the cut */
      var B = basis();
      plane.position.copy(B.c); plane.lookAt(B.c.clone().add(B.n));
      for (var yy = 0; yy < HN; yy++) for (var xx = 0; xx < HN; xx++) {
        var s1 = -1.3 + 2.6 * xx / (HN - 1), s2 = 1.3 - 2.6 * yy / (HN - 1);
        var px = B.c.x + B.u.x * s1 + B.v.x * s2, py = B.c.y + B.u.y * s1 + B.v.y * s2, pz = B.c.z + B.u.z * s1 + B.v.z * s2;
        var o = (yy * HN + xx) * 4;
        if (Math.abs(px) > 1 || Math.abs(py) > 1 || Math.abs(pz) > 1) { img.data[o] = 2; img.data[o + 1] = 4; img.data[o + 2] = 8; img.data[o + 3] = 255; continue; }
        var cc = viridis(field(px, py, pz, t, P));
        img.data[o] = cc[0]; img.data[o + 1] = cc[1]; img.data[o + 2] = cc[2]; img.data[o + 3] = 255;
      }
      octx.putImageData(img, 0, 0);
      hctx.imageSmoothingEnabled = true; hctx.drawImage(off, 0, 0, heat.width, heat.height);
      if (lab) lab.textContent = 'Cut: direction ' + sAng.value + '°, tilt ' + sTilt.value + '°, position ' + (sOff.value / 100).toFixed(2);
      renderer.render(scene, camera);
    }
    requestAnimationFrame(frame);
  }

  window._simInit = window._simInit || {};
  window._simInit.peg3d = function () { if (window._simInit.peg3d._done) return; window._simInit.peg3d._done = true; start(); };
})();
