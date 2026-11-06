/* ============================================================
   public/js/orb.js — the LazyTradie AI Orb renderer (window.LTOrb).

   A living dot-mesh sphere: ~1.5–2.5k points on latitude rings, displaced by 3D
   simplex noise in the vertex shader, over an OPAQUE shaded core (so it reads on
   black, navy AND white), with a gold rim light, outer glow (dark themes) or a soft
   coloured drop shadow + crisp darker rim (light theme), and radiating rings.

   No dependencies. WebGL 1 with a Canvas 2D fallback; handles context loss.
   Personality follows the Melbourne time of day (same buckets as
   services/voice/greetings.js) and morphs over ~3 s; theme changes crossfade ~400 ms.

     var orb = LTOrb.create(hostEl, { size: 64, theme: 'auto', time: 'auto' });
     orb.setState('idle' | 'hover' | 'pressed' | 'listening' | 'thinking' | 'speaking');
     orb.setHover(bool); orb.press(); orb.flash('success' | 'error'); orb.ring();
     orb.setLevel(0..1) or orb.setLevelSource(fn → 0..1)   // mic / playback RMS
     orb.setMagnetic(bool); orb.setMagnetStrength(0..2)    // dots part around the cursor
     orb.setTheme('black' | 'navy' | 'light' | 'auto'); orb.setTime(bucket | 'auto');
     orb.pause(reason) / orb.resume(reason); orb.destroy(); orb.info()
     manual mode (recording): LTOrb.create(el, { manual: true }) → orb.step(dt); orb.render()

   Performance: devicePixelRatio capped at 2; 30 fps while idle, 60 when active;
   the loop stops when the tab is hidden, the orb is off-screen, or pause() is held.
   prefers-reduced-motion → one static frame + a CSS opacity breathe only.
   Premium touches: magnetic cursor (dots part around the pointer / a touch and spring
   back, slight parallax tilt), a shockwave on tap, 4 gold sparkles on elliptical orbits,
   a slow light sweep round the rim (~6 s), an aurora halo that breathes (dark) / a
   shadow pulse (light). The cursor is read once per frame from a passive document
   listener; the 60 fps rate only applies while it is in range. Reduced motion: none.
   ============================================================ */
(function (root, factory) {
  var api = factory(root);
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.LTOrb = api;
}(typeof self !== 'undefined' ? self : this, function (root) {
  'use strict';

  // ── Melbourne time of day — the same buckets as services/voice/greetings.js ──
  var HOUR_FMT = null;
  try { HOUR_FMT = new Intl.DateTimeFormat('en-AU', { timeZone: 'Australia/Melbourne', hour: 'numeric', hourCycle: 'h23' }); } catch (_e) { /* old engine */ }
  function melbourneHour(date) {
    date = date || new Date();
    if (HOUR_FMT && HOUR_FMT.formatToParts) {
      var parts = HOUR_FMT.formatToParts(date);
      for (var i = 0; i < parts.length; i++) {
        if (parts[i].type === 'hour') { var h = Number(parts[i].value); return h === 24 ? 0 : h; }
      }
    }
    return (date.getUTCHours() + 10) % 24; // no time-zone support: assume AEST
  }
  function bucketForHour(h) {
    if (h >= 5 && h < 12) return 'morning';
    if (h >= 12 && h < 17) return 'afternoon';
    if (h >= 17 && h < 21) return 'evening';
    if (h >= 21) return 'night';
    return 'late_night';
  }
  function bucketFor(date) { return bucketForHour(melbourneHour(date)); }
  var BUCKETS = ['morning', 'afternoon', 'evening', 'night', 'late_night'];

  // ── personalities: palette + shape per bucket ──────────────────────────────
  // c1 top / c2 middle / c3 bottom of the dot shell; k1 lit / k2 shadow side of the core.
  var PERSONALITY = {
    morning:    { c1: '#FFD36E', c2: '#FF9F7A', c3: '#FF6B6B', k1: '#FFB65C', k2: '#D9475E',
      amp: 0.07, freq: 2.4, speed: 0.40, rip: 0.018, ripSpeed: 2.2, spin: 0.20, breathRate: 4.0, breathAmp: 0.030, spark: 0.40 },
    afternoon:  { c1: '#8CF4FF', c2: '#22C7D6', c3: '#0E9F9A', k1: '#2CC9E8', k2: '#0A5E7E',
      amp: 0.11, freq: 2.0, speed: 0.55, rip: 0.016, ripSpeed: 2.6, spin: 0.30, breathRate: 3.6, breathAmp: 0.030, spark: 0.40 },
    evening:    { c1: '#FFA24A', c2: '#F2508C', c3: '#B5179E', k1: '#FF7A45', k2: '#8C1670',
      amp: 0.16, freq: 1.35, speed: 0.28, rip: 0.012, ripSpeed: 1.4, spin: 0.16, breathRate: 4.5, breathAmp: 0.030, spark: 0.45 },
    night:      { c1: '#4FB2FF', c2: '#8B5CF6', c3: '#4338CA', k1: '#6A5CFF', k2: '#2A157F',
      amp: 0.08, freq: 1.6, speed: 0.18, rip: 0.009, ripSpeed: 1.0, spin: 0.09, breathRate: 5.0, breathAmp: 0.025, spark: 0.35 },
    late_night: { c1: '#7C8CE8', c2: '#5A3FB5', c3: '#17205C', k1: '#283A93', k2: '#070B26',
      amp: 0.05, freq: 1.4, speed: 0.10, rip: 0.006, ripSpeed: 0.7, spin: 0.05, breathRate: 6.5, breathAmp: 0.045, spark: 1.00 },
  };
  var GOLD = hex('#F5A623');
  var SHAPE_KEYS = ['amp', 'freq', 'speed', 'rip', 'ripSpeed', 'spin', 'breathRate', 'breathAmp', 'spark'];
  var COLOR_KEYS = ['c1', 'c2', 'c3', 'k1', 'k2'];

  // How each state shapes the orb (multipliers / additions on top of the personality).
  var STATES = {
    idle:      { bright: 1.00, speedMul: 1.00, ampMul: 1.00, scale: 1.00, swirl: 0, think: 0, inflow: 0, glow: 1.00, orbit: 1.0 },
    hover:     { bright: 1.10, speedMul: 1.35, ampMul: 1.05, scale: 1.15, swirl: 0, think: 0, inflow: 0, glow: 1.15, orbit: 1.3 },
    pressed:   { bright: 1.06, speedMul: 1.20, ampMul: 1.00, scale: 0.92, swirl: 0, think: 0, inflow: 0, glow: 1.10, orbit: 1.2 },
    listening: { bright: 1.08, speedMul: 1.25, ampMul: 1.10, scale: 1.05, swirl: 0, think: 0, inflow: 1, glow: 1.25, orbit: 1.5 },
    thinking:  { bright: 1.04, speedMul: 1.60, ampMul: 0.90, scale: 0.97, swirl: 1, think: 1, inflow: 0, glow: 1.10, orbit: 2.8 },
    speaking:  { bright: 1.08, speedMul: 1.20, ampMul: 1.05, scale: 1.04, swirl: 0, think: 0, inflow: 0, glow: 1.30, orbit: 2.3 },
  };

  function hex(h) {
    var n = parseInt(String(h).replace('#', ''), 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(cur, target, dt, tau) { return cur + (target - cur) * (1 - Math.exp(-dt / Math.max(tau, 1e-4))); }
  function easeArr(cur, target, dt, tau) { for (var i = 0; i < 3; i++) cur[i] = ease(cur[i], target[i], dt, tau); return cur; }

  // ── geometry: latitude rings of dots (the reference's dot-grid sphere) ──────
  function buildPoints(rings, sparkles, inflow, orbiters) {
    var pos = [], meta = [], i, j, s = 1;
    function rnd() { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; } // deterministic
    for (i = 0; i < rings; i++) {
      var lat = -Math.PI / 2 + (i + 0.5) / rings * Math.PI;
      var y = Math.sin(lat), rr = Math.cos(lat);
      var n = Math.max(6, Math.round(rr * rings * 2));
      var off = (i % 2) * 0.5;
      for (j = 0; j < n; j++) {
        var lon = (j + off) / n * Math.PI * 2;
        pos.push(rr * Math.cos(lon), y, rr * Math.sin(lon)); meta.push(rnd(), 0);
      }
    }
    function randomDir() {
      var u = rnd() * 2 - 1, th = rnd() * Math.PI * 2, r = Math.sqrt(1 - u * u);
      return [r * Math.cos(th), u, r * Math.sin(th)];
    }
    for (i = 0; i < inflow; i++) { var d = randomDir(); pos.push(d[0], d[1], d[2]); meta.push(rnd(), 1); }
    for (i = 0; i < sparkles; i++) { var e = randomDir(); pos.push(e[0], e[1], e[2]); meta.push(rnd(), 2); }
    for (i = 0; i < (orbiters || 0); i++) { pos.push(0, 0, 0); meta.push((i + 0.15 + rnd() * 0.5) / orbiters, 3); } // gold orbiting sparkles
    return { pos: new Float32Array(pos), meta: new Float32Array(meta), count: pos.length / 3 };
  }

  // ── shaders ────────────────────────────────────────────────────────────────
  // 3D simplex noise: Ashima Arts / Stefan Gustavson (MIT).
  var NOISE = [
    'vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}',
    'vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}',
    'vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}',
    'vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}',
    'float snoise(vec3 v){',
    ' const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0);',
    ' vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);',
    ' vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);',
    ' vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy;',
    ' i=mod289(i);',
    ' vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));',
    ' float n_=0.142857142857; vec3 ns=n_*D.wyz-D.xzx;',
    ' vec4 j=p-49.0*floor(p*ns.z*ns.z); vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_);',
    ' vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y);',
    ' vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);',
    ' vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0));',
    ' vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;',
    ' vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);',
    ' vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));',
    ' p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;',
    ' vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m;',
    ' return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));',
    '}',
  ].join('\n');

  var POINTS_VS = [
    'precision highp float;',
    'attribute vec3 aPos; attribute vec2 aMeta;',
    'uniform float uNoiseT, uRipT, uSpinA, uSwirlT, uTime;',
    'uniform float uAmp, uFreq, uRip, uLevel, uSwirl, uInflow, uSpark, uTilt;',
    'uniform float uR, uPointPx, uThink, uErr, uSweep, uBright, uLight;',
    'uniform vec2 uOffset, uCursor, uPar, uShock;',
    'uniform float uMag, uOrbT, uOrbit, uRimA, uRimK;',
    'uniform vec3 uC1, uC2, uC3, uGold;',
    'varying vec3 vCol; varying float vA;',
    NOISE,
    'mat3 rotY(float a){float c=cos(a),s=sin(a);return mat3(c,0.0,-s, 0.0,1.0,0.0, s,0.0,c);}',
    'mat3 rotX(float a){float c=cos(a),s=sin(a);return mat3(1.0,0.0,0.0, 0.0,c,s, 0.0,-s,c);}',
    'mat3 rotZ(float a){float c=cos(a),s=sin(a);return mat3(c,s,0.0, -s,c,0.0, 0.0,0.0,1.0);}',
    'void main(){',
    ' float seed=aMeta.x; float kind=aMeta.y;',
    ' vec3 p=aPos;',
    ' p=rotY(uSwirl*(p.y*2.2+uSwirlT))*p;',                          // thinking: twist into a vortex
    ' float n=snoise(p*uFreq+vec3(0.0,uNoiseT,uNoiseT*0.6));',
    ' float rp=snoise(p*(uFreq*1.8+0.8)+vec3(uRipT));',
    ' float r=1.0+n*uAmp+rp*(uRip+uLevel*0.11);',
    ' r*=1.0-0.10*uSwirl;',
    ' vec3 q; float a=1.0; float sz=1.0;',
    ' if(kind<0.5){ q=p*r; }',
    ' else if(kind<1.5){ float ph=fract(uTime*0.62+seed); q=aPos*(1.0+0.6*(1.0-ph)*(1.0-ph));',   // listening: particles flow IN
    '   a=uInflow*smoothstep(0.0,0.2,ph)*smoothstep(1.0,0.8,ph); sz=1.15; }',
    ' else if(kind<2.5){ q=p*(r+0.03); a=uSpark*pow(0.5+0.5*sin(uTime*(1.6+seed*2.4)+seed*40.0),6.0); sz=1.9; }',
    ' else { float ph=uOrbT*(0.55+seed*0.5)+seed*6.2831; float A=1.2+seed*0.18;',            // gold sparkles on tilted ellipses
    '   q=rotZ(seed*2.6-1.3)*rotX(0.42+seed*0.55)*vec3(cos(ph)*A,0.0,sin(ph)*A*0.9);',
    '   a=uOrbit*(0.75+0.25*sin(uTime*3.0+seed*20.0)); sz=2.2; }',
    ' if(kind<2.5) q=rotX(uTilt+uPar.y)*rotY(uSpinA+uPar.x)*q; else q=rotX(uTilt*0.5+uPar.y)*rotY(uPar.x)*q;',
    ' if(uShock.y>0.0&&kind<0.5){ float l0=max(length(q),0.001); float ang=acos(clamp(q.z/l0,-1.0,1.0));',   // tap: a shockwave runs from the face to the edge
    '   q*=1.0+uShock.y*0.13*exp(-pow((ang-uShock.x*3.4)/0.24,2.0))*max(0.0,1.0-uShock.x/0.85); }',
    ' q*=mix(1.0,0.975,uLight);',                                   // light: hug the crisp rim
    ' float persp=3.2/(3.2-q.z);',
    ' vec2 xy=q.xy*persp*uR;',
    ' if(uMag>0.001&&(kind<0.5||kind>2.5)){ vec2 dv=xy-uCursor; float dd=length(dv); float sg=0.62*uR;',     // magnetic: dots part around the cursor
    '   xy+=dv/max(dd,0.0001)*uMag*exp(-dd*dd/(sg*sg))*0.42*uR; }',
    ' xy+=uOffset;',
    ' gl_Position=vec4(xy,0.0,1.0);',
    ' float front=clamp(q.z*0.5+0.5,0.0,1.0);',
    ' float lat=clamp(q.y*0.5+0.5,0.0,1.0);',
    ' vec3 c=mix(uC3,uC2,smoothstep(0.0,0.55,lat)); c=mix(c,uC1,smoothstep(0.45,1.0,lat));',
    ' c*=0.82+0.36*(n*0.5+0.5);',
    ' float len=max(length(q),0.001); float rim=1.0-abs(q.z)/len;',
    ' float side=clamp(dot(normalize(q.xy+vec2(0.0001)),normalize(vec2(0.55,0.85))),0.0,1.0);',
    ' c=mix(c,uGold,pow(rim,2.0)*(0.22+0.72*side));',                 // gold rim light, upper right
    ' float rA=atan(q.y,q.x); float dA=abs(mod(rA-uRimA+3.14159,6.28318)-3.14159);',
    ' c=mix(c,vec3(1.0,0.95,0.82),uRimK*pow(rim,3.0)*exp(-dA*dA/0.18)*0.8);',   // the slow light sweep round the rim
    ' c=mix(c,vec3(0.58,0.38,1.0),uThink*0.5);',
    ' c=mix(c,vec3(1.0,0.32,0.28),uErr*0.75);',
    ' float band=exp(-pow(dot(q.xy,vec2(0.7071))-uSweep,2.0)/0.03);',
    ' c=mix(c,vec3(1.0,0.88,0.55),band*0.85);',
    ' c*=uBright;',
    ' if(kind>0.5&&kind<1.5) c=mix(uGold,uC1,0.35);',
    ' if(kind>1.5&&kind<2.5) c=mix(uGold,vec3(1.0,0.93,0.7),0.35);',
    ' if(kind>2.5) c=mix(uGold,vec3(1.0,0.96,0.86),0.3);',
    ' float edgeK=smoothstep(0.80,0.98,length(q.xy));',              // over the core vs at the silhouette
    ' c=mix(c,mix(c*1.06,c*0.6,edgeK),uLight);',                     // light theme: never white; darker than the page at the edge
    ' float depthA=mix(mix(0.30,0.16,uLight),1.0,front);',
    ' if(kind<0.5) a*=depthA;',
    ' float back=smoothstep(-0.03,0.10,q.z/len);',                  // back hemisphere hidden behind the solid core
    ' if(kind>2.5) back=max(back,smoothstep(0.9,1.0,length(q.xy)));', // orbiters stay visible outside the silhouette
    ' a*=back;',
    ' vCol=c; vA=a;',
    ' gl_PointSize=uPointPx*mix(0.55,1.15,front)*sz;',
    '}',
  ].join('\n');

  var POINTS_FS = [
    'precision mediump float;',
    'varying vec3 vCol; varying float vA;',
    'void main(){',
    ' float d=length(gl_PointCoord-0.5);',
    ' float a=smoothstep(0.5,0.26,d)*vA;',
    ' if(a<0.004) discard;',
    ' gl_FragColor=vec4(vCol*a,a);',
    '}',
  ].join('\n');

  var QUAD_VS = 'attribute vec2 aXY; varying vec2 vUv; void main(){ vUv=aXY; gl_Position=vec4(aXY,0.0,1.0); }';

  var QUAD_FS = [
    '#ifdef GL_FRAGMENT_PRECISION_HIGH',
    'precision highp float;',
    '#else',
    'precision mediump float;',
    '#endif',
    'varying vec2 vUv;',
    'uniform float uR, uPx, uCoreT, uLight, uGlow, uThink, uErr, uSweep, uLevel, uBright, uPulse, uTime;',
    'uniform float uMag, uAurora, uAurT, uRimA, uRimK, uShadowK;',
    'uniform vec2 uOffset, uCursor, uPar;',
    'uniform vec3 uC1, uC2, uC3, uK1, uK2, uGold;',
    'uniform vec4 uRingAge, uRingAmp;',
    NOISE,
    'vec4 over(vec4 dst, vec3 c, float a){ return vec4(c*a+dst.rgb*(1.0-a), a+dst.a*(1.0-a)); }',
    'float ring(float d, float age, float amp){',
    ' if(age<0.0||age>1.1) return 0.0;',
    ' float rr=0.95+age*0.78; float w=0.03+age*0.025;',
    ' return exp(-pow((d-rr)/w,2.0))*amp*(1.0-age/1.1);',
    '}',
    'void main(){',
    ' vec2 q=(vUv-uOffset)/uR; float d=length(q); float px=uPx/uR;',
    ' vec4 o=vec4(0.0);',
    // light theme: soft coloured drop shadow
    ' float sd=length((q-vec2(0.0,-0.16))*vec2(1.0,1.18))/(0.94+0.08*uShadowK);',          // + a clean pulse with the idle breath
    ' o=over(o, uK2*0.55, uLight*(0.24+0.10*uShadowK)*(1.0-smoothstep(0.5,1.35,sd)));',
    // dark themes: outer glow to ~1.6x
    ' float g=(1.0-uLight)*uGlow*(0.5+0.5*uLevel)*exp(-max(d-0.93,0.0)*2.8)*(1.0-smoothstep(1.08,1.62,d));',
    ' o=over(o, mix(uC2,uGold,0.12), clamp(g*0.62,0.0,1.0));',
    // dark themes: a soft aurora halo that breathes with the idle cycle
    ' float aur=(1.0-uLight)*uAurora*smoothstep(0.86,1.0,d)*(1.0-smoothstep(1.0,1.6,d));',
    ' if(aur>0.002){ float an=snoise(vec3(q*1.25,uAurT)); float rib=smoothstep(-0.2,0.7,an);',
    '  o=over(o, mix(mix(uC3,uC1,rib),uGold,0.12), clamp(aur*rib*0.42,0.0,1.0)); }',
    // rings (press, voice peaks) + the listening pulse
    ' vec3 rc=mix(mix(uC2,uGold,0.25),uK2*0.8,uLight);',
    ' float rb=ring(d,uRingAge.x,uRingAmp.x)+ring(d,uRingAge.y,uRingAmp.y)+ring(d,uRingAge.z,uRingAmp.z)+ring(d,uRingAge.w,uRingAmp.w);',
    ' rb+=exp(-pow((d-(1.07+uPulse*0.12))/0.03,2.0))*uPulse*0.8;',
    ' o=over(o, rc, clamp(rb,0.0,1.0)*0.85);',
    // the solid core
    ' float R=0.93;',
    ' float cov=1.0-smoothstep(R-px*1.2,R+px*0.4,d);',
    ' if(cov>0.0){',
    '  vec2 cq=q/R; float cz=sqrt(max(0.0,1.0-dot(cq,cq)));',
    '  vec3 nrm=vec3(cq,cz); vec3 L=normalize(vec3(-0.45-uPar.x*0.9,0.6+uPar.y*0.9,0.66));',     // parallax: the light follows the tilt
    '  float diff=clamp(dot(nrm,L),0.0,1.0);',
    '  float n1=snoise(vec3(cq*1.7,uCoreT))*0.5+0.5;',
    '  float n2=snoise(vec3(cq*3.2+7.0,uCoreT*1.5))*0.5+0.5;',
    '  vec3 base=mix(uK2,uK1,clamp(0.15+0.85*diff,0.0,1.0));',
    '  base=mix(base,uC2,n1*0.30);',
    '  base+=(n2-0.5)*0.07;',
    '  base=mix(base,vec3(0.40,0.24,0.86),uThink*0.45);',
    '  base*=1.0+uThink*0.20*sin(uTime*5.5)*(1.0-length(cq));',        // thinking: inner core pulses
    '  base=mix(base,vec3(0.82,0.16,0.15),uErr*0.55);',
    '  float fres=pow(1.0-cz,2.6);',
    '  float side=clamp(dot(normalize(cq+vec2(0.0001)),normalize(vec2(0.55,0.85))),0.0,1.0);',
    '  base=mix(base,uGold,fres*(0.24+0.7*side));',                      // gold rim light
    '  float ca=atan(cq.y,cq.x); float dA=abs(mod(ca-uRimA+3.14159,6.28318)-3.14159);',
    '  base=mix(base,vec3(1.0,0.94,0.78),uRimK*fres*exp(-dA*dA/0.16)*0.75);',              // light sweep round the rim
    '  vec2 cu=uCursor/uR-q; base+=uMag*exp(-dot(cu,cu)/0.10)*0.07;',                         // a faint glint where the cursor glides
    '  base+=pow(clamp(dot(reflect(-L,nrm),vec3(0.0,0.0,1.0)),0.0,1.0),18.0)*0.18;', // soft specular
    '  float band=exp(-pow(dot(q,vec2(0.7071))-uSweep,2.0)/0.02);',
    '  base=mix(base,vec3(1.0,0.88,0.55),band*0.75);',                   // success shimmer sweep
    '  base*=uBright;',
    '  base=mix(base,base*0.9,uLight);',
    '  float rimLine=uLight*(1.0-smoothstep(px*0.5,px*1.4,abs(d-(R-px*0.9))));', // light: crisp darker 1px rim
    '  base=mix(base,uK2*0.45,rimLine);',
    '  o=over(o, clamp(base,0.0,1.0), cov);',
    ' }',
    ' gl_FragColor=o;',
    '}',
  ].join('\n');

  // ── WebGL renderer ─────────────────────────────────────────────────────────
  function GLRenderer(canvas, preserve, geo) {
    var gl = canvas.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false, depth: false, stencil: false,
      preserveDrawingBuffer: !!preserve, powerPreference: 'low-power' });
    if (!gl) throw new Error('no webgl');
    function sh(type, src) {
      var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS) && !gl.isContextLost()) throw new Error('shader: ' + gl.getShaderInfoLog(s));
      return s;
    }
    function prog(vs, fs) {
      var p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p);
      if (!gl.getProgramParameter(p, gl.LINK_STATUS) && !gl.isContextLost()) throw new Error('link: ' + gl.getProgramInfoLog(p));
      var u = {}, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS);
      for (var i = 0; i < n; i++) { var info = gl.getActiveUniform(p, i); u[info.name] = gl.getUniformLocation(p, info.name); }
      return { p: p, u: u };
    }
    var pts = prog(POINTS_VS, POINTS_FS), quad = prog(QUAD_VS, QUAD_FS);
    var bPos = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bPos); gl.bufferData(gl.ARRAY_BUFFER, geo.pos, gl.STATIC_DRAW);
    var bMeta = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bMeta); gl.bufferData(gl.ARRAY_BUFFER, geo.meta, gl.STATIC_DRAW);
    var bQuad = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bQuad); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var aPos = gl.getAttribLocation(pts.p, 'aPos'), aMeta = gl.getAttribLocation(pts.p, 'aMeta'), aXY = gl.getAttribLocation(quad.p, 'aXY');
    gl.disable(gl.DEPTH_TEST); gl.enable(gl.BLEND);

    function set(prg, name, v) {
      var loc = prg.u[name]; if (loc == null) return;
      if (typeof v === 'number') gl.uniform1f(loc, v);
      else if (v.length === 2) gl.uniform2f(loc, v[0], v[1]);
      else if (v.length === 3) gl.uniform3f(loc, v[0], v[1], v[2]);
      else gl.uniform4f(loc, v[0], v[1], v[2], v[3]);
    }
    return {
      kind: 'webgl',
      gl: gl,
      draw: function (U) {
        gl.viewport(0, 0, canvas.width, canvas.height);
        gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
        // core + glow + rings + shadow (normal, premultiplied)
        gl.useProgram(quad.p);
        gl.bindBuffer(gl.ARRAY_BUFFER, bQuad); gl.enableVertexAttribArray(aXY); gl.vertexAttribPointer(aXY, 2, gl.FLOAT, false, 0, 0);
        for (var k in U.quad) set(quad, k, U.quad[k]);
        gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        gl.disableVertexAttribArray(aXY);
        // dot shell: additive on dark themes, normal blending on light (additive vanishes on white)
        gl.useProgram(pts.p);
        gl.bindBuffer(gl.ARRAY_BUFFER, bPos); gl.enableVertexAttribArray(aPos); gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, bMeta); gl.enableVertexAttribArray(aMeta); gl.vertexAttribPointer(aMeta, 2, gl.FLOAT, false, 0, 0);
        for (var m in U.pts) set(pts, m, U.pts[m]);
        if (U.additive) gl.blendFunc(gl.ONE, gl.ONE); else gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
        gl.drawArrays(gl.POINTS, 0, geo.count);
        gl.disableVertexAttribArray(aPos); gl.disableVertexAttribArray(aMeta);
      },
      lose: function () { var ext = gl.getExtension('WEBGL_lose_context'); if (ext) ext.loseContext(); return !!ext; },
      destroy: function () { try { var ext = gl.getExtension('WEBGL_lose_context'); if (ext) ext.loseContext(); } catch (_e) {} },
    };
  }

  // ── Canvas 2D fallback (no WebGL / context not coming back) ────────────────
  function Canvas2DRenderer(canvas, geo) {
    var g = canvas.getContext('2d');
    if (!g) throw new Error('no 2d');
    // a lighter point set for the CPU
    var step = Math.max(1, Math.round(geo.count / 380)), P = [];
    for (var i = 0; i < geo.count; i += step) if (geo.meta[i * 2 + 1] === 0) P.push([geo.pos[i * 3], geo.pos[i * 3 + 1], geo.pos[i * 3 + 2]]);
    function rgb(c, a) { return 'rgba(' + Math.round(c[0] * 255) + ',' + Math.round(c[1] * 255) + ',' + Math.round(c[2] * 255) + ',' + a + ')'; }
    function mix3(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
    return {
      kind: '2d',
      draw: function (U) {
        var W = canvas.width, H = canvas.height, s = Math.min(W, H) / 2;
        var q = U.quad, p = U.pts, light = q.uLight;
        var cx = W / 2 + q.uOffset[0] * s, cy = H / 2 - q.uOffset[1] * s, R = q.uR * s;
        g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H);
        if (light > 0.01) { // drop shadow
          var sg = g.createRadialGradient(cx, cy + R * 0.16, R * 0.5, cx, cy + R * 0.16, R * 1.35);
          sg.addColorStop(0, rgb(mix3(q.uK2, [0, 0, 0], 0.45), 0.30 * light)); sg.addColorStop(1, rgb(q.uK2, 0));
          g.fillStyle = sg; g.fillRect(0, 0, W, H);
        }
        if (light < 0.99) { // glow
          var gg = g.createRadialGradient(cx, cy, R * 0.8, cx, cy, R * 1.6);
          gg.addColorStop(0, rgb(q.uC2, 0.55 * (1 - light) * Math.min(1.5, q.uGlow))); gg.addColorStop(1, rgb(q.uC2, 0));
          g.fillStyle = gg; g.fillRect(0, 0, W, H);
        }
        var rc = mix3(q.uC2, q.uGold, 0.25);
        [0, 1, 2, 3].forEach(function (k) {
          var age = q.uRingAge[k], amp = q.uRingAmp[k];
          if (age < 0 || age > 1.1) return;
          g.strokeStyle = rgb(rc, amp * (1 - age / 1.1) * 0.8); g.lineWidth = Math.max(1, R * 0.05);
          g.beginPath(); g.arc(cx, cy, R * (0.95 + age * 0.78), 0, Math.PI * 2); g.stroke();
        });
        // core
        var cg = g.createRadialGradient(cx - R * 0.3, cy - R * 0.35, R * 0.1, cx, cy, R * 0.93);
        var k1 = mix3(q.uK1, [0.42, 0.25, 0.86], q.uThink * 0.45), k2 = mix3(q.uK2, [0.42, 0.25, 0.86], q.uThink * 0.3);
        k1 = mix3(k1, [0.82, 0.16, 0.15], q.uErr * 0.55);
        cg.addColorStop(0, rgb(k1.map(function (v) { return Math.min(1, v * q.uBright * (1 - 0.16 * light)); }), 1));
        cg.addColorStop(0.75, rgb(mix3(k1, k2, 0.7), 1)); cg.addColorStop(1, rgb(mix3(k2, q.uGold, 0.35), 1));
        g.fillStyle = cg; g.beginPath(); g.arc(cx, cy, R * 0.93, 0, Math.PI * 2); g.fill();
        if (light > 0.5) { g.strokeStyle = rgb(mix3(q.uK2, [0, 0, 0], 0.55), 1); g.lineWidth = 1; g.stroke(); }
        // dots
        var cs = Math.cos(p.uSpinA + p.uPar[0]), sn = Math.sin(p.uSpinA + p.uPar[0]), ct = Math.cos(p.uTilt + p.uPar[1]), st = Math.sin(p.uTilt + p.uPar[1]);
        var ps = Math.max(1, p.uPointPx * 0.8);
        var curX = cx + p.uCursor[0] * s, curY = cy - p.uCursor[1] * s, sg = 0.62 * R, push = p.uMag * 0.42 * R;
        function repel(xy) { if (push <= 0.01) return xy; var dx = xy[0] - curX, dy = xy[1] - curY, dd = Math.sqrt(dx * dx + dy * dy) || 0.0001, k = Math.exp(-dd * dd / (sg * sg)); return [xy[0] + dx / dd * push * k, xy[1] + dy / dd * push * k]; }
        for (var j = 0; j < P.length; j++) {
          var v = P[j];
          var n = Math.sin(v[0] * 3.1 + p.uNoiseT * 2.0) * Math.cos(v[1] * 2.7 + p.uNoiseT * 1.3) * Math.sin(v[2] * 2.3 + p.uNoiseT);
          var r = 1 + n * p.uAmp * 1.6 + Math.sin(v[1] * 9 + p.uRipT * 3) * (p.uRip + p.uLevel * 0.16) * 0.6;
          var x = v[0] * r, y = v[1] * r, z = v[2] * r;
          var x2 = x * cs + z * sn, z2 = -x * sn + z * cs;            // spin
          var y2 = y * ct - z2 * st, z3 = y * st + z2 * ct;           // tilt
          var front = Math.max(0, Math.min(1, z3 * 0.5 + 0.5));
          if (z3 < -0.05) continue;
          var persp = 3.2 / (3.2 - z3);
          var lat = Math.max(0, Math.min(1, y2 * 0.5 + 0.5));
          var c = lat < 0.5 ? mix3(q.uC3, p.uC2, lat * 2) : mix3(p.uC2, p.uC1, (lat - 0.5) * 2);
          c = mix3(c, [0, 0, 0], 0.34 * light);
          g.fillStyle = rgb(c, (0.3 + 0.7 * front) * (light > 0.5 ? 0.95 : 1));
          var pt = repel([cx + x2 * persp * R, cy - y2 * persp * R]), sz = ps * (0.55 + 0.6 * front);
          g.fillRect(pt[0] - sz / 2, pt[1] - sz / 2, sz, sz);
        }
        if (p.uOrbit > 0) { // the gold orbiting sparkles
          for (var oi = 0; oi < 4; oi++) {
            var sd = (oi + 0.4) / 4, ph = p.uOrbT * (0.55 + sd * 0.5) + sd * 6.2831, A = 1.2 + sd * 0.18;
            var ox = Math.cos(ph) * A, oz = Math.sin(ph) * A * 0.9, tl = 0.42 + sd * 0.55, oy = -oz * Math.sin(tl), oz2 = oz * Math.cos(tl);
            if (oz2 < 0 && ox * ox + oy * oy < 0.85) continue; // behind the core
            var op = repel([cx + ox * R, cy - oy * R]);
            g.fillStyle = rgb(mix3(q.uGold, [1, 0.96, 0.86], 0.3), p.uOrbit); g.beginPath(); g.arc(op[0], op[1], Math.max(1, ps * 0.9), 0, Math.PI * 2); g.fill();
          }
        }
      },
      destroy: function () {},
    };
  }

  // ── the orb ────────────────────────────────────────────────────────────────
  function themeLight(t) { return t === 'light' ? 1 : 0; }
  function autoTheme() {
    try { return (root.document.documentElement.getAttribute('data-mode') === 'light') ? 'light' : 'black'; } catch (_e) { return 'black'; }
  }
  function prefersReduced() {
    try { return !!(root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (_e) { return false; }
  }

  function Orb(host, opts) {
    var o = this.o = {};
    var d = { size: 64, canvasScale: 2.4, theme: 'auto', time: 'auto', reducedMotion: null, manual: false, preserve: false,
      renderer: 'auto', fps: 60, idleFps: 30, dprMax: 2, magnetic: true, magnet: 1 };
    for (var k in d) o[k] = (opts && opts[k] !== undefined) ? opts[k] : d[k];
    this.host = host;
    this.time = 0; this.state = 'idle'; this.hoverOn = false; this.pauses = {}; this.running = false; this.destroyed = false;
    this.level = 0; this.levelRaw = 0; this.levelMean = 0; this.levelFn = null; this.lastPeak = -1;
    this.rings = [-9, -9, -9, -9]; this.ringAmp = [0, 0, 0, 0]; this.ringNext = 0;
    this.sweepAt = -9; this.errAt = -9; this.pressAt = -9;
    this.ph = { noise: 0, rip: 0, spin: 0.6, swirl: 0, core: 0, breath: 0, orbit: 0, aur: 0 };
    this.mag = { x: 0, y: 0, s: 0, vx: 0, vy: 0, vs: 0, near: false }; this.shockAt = -9; this._ptr = null; this._hostRect = null; this._rectAt = -9;
    this.stats = { frames: 0, fps: 0, ms: 0, since: 0, acc: 0 };
    this.themeName = o.theme === 'auto' ? autoTheme() : o.theme;
    this.bucketMode = o.time; this.bucket = o.time === 'auto' ? bucketFor() : o.time;
    var per = PERSONALITY[this.bucket] || PERSONALITY.afternoon;
    this.cur = {}; this.tgt = {};
    for (var i = 0; i < SHAPE_KEYS.length; i++) { this.cur[SHAPE_KEYS[i]] = per[SHAPE_KEYS[i]]; }
    for (var c = 0; c < COLOR_KEYS.length; c++) this.cur[COLOR_KEYS[c]] = hex(per[COLOR_KEYS[c]]);
    var st = STATES.idle; for (var sk in st) this.cur[sk] = st[sk];
    this.cur.light = themeLight(this.themeName);
    this.reduced = o.reducedMotion == null ? prefersReduced() : !!o.reducedMotion;
    this.geo = buildPoints(o.size >= 160 ? 46 : 34, 26, 64, 4);
    this._mountCanvas();
    this._frame = this._frame.bind(this);
    this._wire();
    if (this.reduced) { host.classList.add('lt-orb-reduced'); this.step(0); this.render(); }
    else if (!o.manual) this._start();
  }

  Orb.prototype._mountCanvas = function () {
    var o = this.o, cv = root.document.createElement('canvas');
    cv.className = 'lt-orb-canvas'; cv.setAttribute('aria-hidden', 'true');
    if (this.canvas && this.canvas.parentNode) this.canvas.parentNode.replaceChild(cv, this.canvas); else this.host.appendChild(cv);
    this.canvas = cv;
    this._size();
    var self = this;
    cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); self._lost(); });
    cv.addEventListener('webglcontextrestored', function () { self._restored(); });
    this.r = null;
    if (o.renderer !== '2d') { try { this.r = GLRenderer(cv, o.preserve, this.geo); } catch (e) { this.r = null; this.glError = String(e && e.message || e).slice(0, 300); } }
    if (!this.r) {
      if (o.renderer !== '2d') { var c2 = root.document.createElement('canvas'); c2.className = cv.className; c2.setAttribute('aria-hidden', 'true'); cv.parentNode.replaceChild(c2, cv); this.canvas = cv = c2; this._size(); }
      this.r = Canvas2DRenderer(cv, this.geo);
    }
  };

  Orb.prototype._size = function () {
    var o = this.o, css = o.size * o.canvasScale, dpr = Math.min(o.dprMax, root.devicePixelRatio || 1);
    this.canvas.style.width = css + 'px'; this.canvas.style.height = css + 'px';
    this.canvas.width = Math.round(css * dpr); this.canvas.height = Math.round(css * dpr);
    this.dpr = dpr;
  };

  Orb.prototype._wire = function () {
    var self = this, doc = root.document;
    this._onVis = function () { if (doc.hidden) self.pause('hidden'); else self.resume('hidden'); };
    doc.addEventListener('visibilitychange', this._onVis);
    if (root.IntersectionObserver) {
      this._io = new root.IntersectionObserver(function (es) { var vis = es[es.length - 1].isIntersecting; if (vis) self.resume('offscreen'); else self.pause('offscreen'); });
      this._io.observe(this.host);
    }
    if (this.o.theme === 'auto' && root.MutationObserver) {
      this._mo = new root.MutationObserver(function () { self._setThemeName(autoTheme()); });
      this._mo.observe(doc.documentElement, { attributes: true, attributeFilter: ['data-mode'] });
    }
    if (this.o.reducedMotion == null && root.matchMedia) {
      try {
        this._mq = root.matchMedia('(prefers-reduced-motion: reduce)');
        this._onMq = function () { self.setReducedMotion(self._mq.matches); };
        if (this._mq.addEventListener) this._mq.addEventListener('change', this._onMq); else this._mq.addListener(this._onMq);
      } catch (_e) {}
    }
    this._timeTimer = root.setInterval(function () { if (self.bucketMode === 'auto') self._setBucket(bucketFor()); }, 60000);
    // magnetic cursor: remember where the pointer is (passive, no work here); the frame reads it
    this._onPtr = function (e) {
      if (e.type === 'pointerup' && e.pointerType !== 'mouse') { self._ptr = null; return; } // a finger lifted: nothing hovers
      self._ptr = { x: e.clientX, y: e.clientY };
    };
    this._onPtrOut = function (e) { if (!e.relatedTarget) self._ptr = null; };
    this._onScroll = function () { self._ptrDirty = true; };
    doc.addEventListener('pointermove', this._onPtr, { passive: true });
    doc.addEventListener('pointerdown', this._onPtr, { passive: true });
    doc.addEventListener('pointerup', this._onPtr, { passive: true });
    doc.addEventListener('pointerout', this._onPtrOut, { passive: true });
    root.addEventListener('scroll', this._onScroll, { passive: true, capture: true });
    root.addEventListener('resize', this._onScroll, { passive: true });
  };

  Orb.prototype._lost = function () {
    var self = this; this.contextLost = true; this._stop();
    clearTimeout(this._lostTimer);
    // the context usually comes back; if not, swap in a fresh canvas (2D or a new WebGL)
    this._lostTimer = setTimeout(function () { if (self.contextLost && !self.destroyed) { self.contextLost = false; self._mountCanvas(); self._kick(); } }, 2500);
  };
  Orb.prototype._restored = function () {
    clearTimeout(this._lostTimer); this.contextLost = false;
    try { this.r = GLRenderer(this.canvas, this.o.preserve, this.geo); } catch (_e) { this._mountCanvas(); }
    this._kick();
  };
  Orb.prototype._kick = function () { if (this.reduced) { this.render(); } else if (!this.o.manual) this._start(); };

  Orb.prototype._paused = function () { for (var k in this.pauses) if (this.pauses[k]) return true; return false; };
  Orb.prototype._start = function () {
    if (this.running || this.destroyed || this.reduced || this.o.manual || this.contextLost || this._paused()) return;
    this.running = true; this.lastT = 0; this.lastDraw = 0;
    this.raf = root.requestAnimationFrame(this._frame);
  };
  Orb.prototype._stop = function () { this.running = false; if (this.raf) root.cancelAnimationFrame(this.raf); this.raf = 0; };
  Orb.prototype._busy = function () {
    return this.state !== 'idle' || this.hoverOn || this.level > 0.02 || (this.time - this.sweepAt) < 1.2 || (this.time - this.errAt) < 1 ||
      Math.abs(this.cur.light - themeLight(this.themeName)) > 0.01 || this._morphing ||
      this.mag.near || this.mag.s > 0.01 || (this.time - this.shockAt) < 0.9;
  };
  Orb.prototype._frame = function (now) {
    if (!this.running) return;
    this.raf = root.requestAnimationFrame(this._frame);
    var idleFps = this.r && this.r.kind === '2d' ? Math.min(15, this.o.idleFps) : this.o.idleFps; // the CPU fallback idles slower
    var minDt = 1000 / (this._busy() ? this.o.fps : idleFps);
    if (this.lastDraw && now - this.lastDraw < minDt - 2) return;
    var dt = this.lastT ? Math.min(0.1, (now - this.lastT) / 1000) : 1 / 60;
    this.lastT = now; this.lastDraw = now;
    var t0 = root.performance ? root.performance.now() : 0;
    this.step(dt); this.render();
    var st = this.stats, t1 = root.performance ? root.performance.now() : 0;
    st.frames++; st.acc += t1 - t0;
    if (!st.since) st.since = now;
    if (now - st.since >= 1000) { st.fps = Math.round(st.frames * 1000 / (now - st.since)); st.ms = +(st.acc / st.frames).toFixed(2); st.frames = 0; st.acc = 0; st.since = now; }
  };

  /** Advance the simulation by dt seconds (manual mode drives this itself). */
  Orb.prototype.step = function (dt) {
    var c = this.cur, t = this.tgt, per = PERSONALITY[this.bucket] || PERSONALITY.afternoon, s = STATES[this.state] || STATES.idle;
    this.time += dt;
    // audio level: fast attack, slower release
    var raw = this.levelFn ? clamp(+this.levelFn() || 0, 0, 1) : this.levelRaw;
    this.level = ease(this.level, raw, dt, raw > this.level ? 0.04 : 0.16);
    this.levelMean = ease(this.levelMean, this.level, dt, 0.45);
    if ((this.state === 'speaking' || this.state === 'listening') && this.level > this.levelMean * 1.35 + 0.08 && this.time - this.lastPeak > 0.2) {
      this.lastPeak = this.time; this.ring(Math.min(1, 0.35 + this.level));
    }
    // targets: personality × state
    var hoverAdd = this.hoverOn && this.state === 'idle' ? STATES.hover : null;
    var S = hoverAdd || s;
    var morphTau = 0.75; // ~3 s to settle a time-of-day change
    var morphing = false;
    for (var i = 0; i < SHAPE_KEYS.length; i++) {
      var k = SHAPE_KEYS[i]; t[k] = per[k];
      var before = c[k]; c[k] = ease(c[k], t[k], dt, morphTau); if (Math.abs(c[k] - t[k]) > 1e-3 * Math.max(1, Math.abs(t[k]))) morphing = true; void before;
    }
    for (var j = 0; j < COLOR_KEYS.length; j++) {
      var ck = COLOR_KEYS[j], tc = hex(per[ck]); easeArr(c[ck], tc, dt, morphTau);
      if (Math.abs(c[ck][0] - tc[0]) + Math.abs(c[ck][1] - tc[1]) + Math.abs(c[ck][2] - tc[2]) > 0.01) morphing = true;
    }
    this._morphing = morphing;
    var stateTau = this.state === 'pressed' ? 0.05 : 0.28;
    for (var sk in S) c[sk] = ease(c[sk], S[sk], dt, sk === 'scale' ? stateTau : 0.3);
    c.light = ease(c.light, themeLight(this.themeName), dt, 0.13); // ~400 ms crossfade
    // phases (integrated, so speed changes never jump)
    var lv = this.level;
    this.ph.noise = (this.ph.noise + dt * c.speed * c.speedMul) % 1000;
    this.ph.rip = (this.ph.rip + dt * c.ripSpeed * c.speedMul * (1 + lv * 1.5)) % 1000;
    this.ph.spin = (this.ph.spin + dt * c.spin * (1 + c.swirl * 0.6)) % (Math.PI * 2000);
    this.ph.swirl = (this.ph.swirl + dt * 1.6) % 1000;
    this.ph.core = (this.ph.core + dt * 0.22 * (1 + c.think * 1.5)) % 200;
    this.ph.breath = (this.ph.breath + dt * Math.PI * 2 / c.breathRate) % (Math.PI * 2);
    this.ph.orbit = (this.ph.orbit + dt * 0.9 * c.orbit) % 10000;
    this.ph.aur = (this.ph.aur + dt * 0.11 * c.speedMul) % 1000;
    this._magnet(dt);
  };

  /** Magnetic cursor: where the pointer is (canvas clip units), springing in / back out. */
  function spring(m, k, target, dt, stiff, zeta) {
    var v = m['v' + k], x = m[k], c = 2 * Math.sqrt(stiff) * zeta, n = Math.max(1, Math.ceil(dt / 0.008)), h = dt / n;
    for (var i = 0; i < n; i++) { v += (stiff * (target - x) - c * v) * h; x += v * h; }
    m[k] = x; m['v' + k] = v;
  }
  /**
   * The pointer in the orb canvas's clip units (centre 0,0; canvas edge ±1) and whether it
   * is near enough to pull: within 2.6 orb radii of the centre, i.e. ~1.5 radii of the rim.
   */
  function magnetTarget(ptr, rect, size, canvasScale, scale) {
    var half = size * canvasScale / 2, R = scale / canvasScale;
    var dx = (ptr.x - (rect.left + rect.width / 2)) / half, dy = -(ptr.y - (rect.top + rect.height / 2)) / half;
    return { x: dx, y: dy, near: dx * dx + dy * dy < R * R * 2.6 * 2.6 };
  }
  Orb.prototype._magnet = function (dt) {
    var m = this.mag, o = this.o, want = 0, tx = m.x, ty = m.y;
    m.near = false;
    if (o.magnetic && !this.reduced && this._ptr && dt > 0) {
      if (this._ptrDirty || !this._hostRect || this.time - this._rectAt > 1) { // the orb moved (scroll / resize / layout) — measure at most once a second otherwise
        this._hostRect = this.host.getBoundingClientRect(); this._ptrDirty = false; this._rectAt = this.time;
      }
      var mt = magnetTarget(this._ptr, this._hostRect, o.size, o.canvasScale, this.cur.scale);
      if (mt.near) {
        m.near = true; want = Math.min(2, o.magnet); tx = mt.x; ty = mt.y;
        if (m.s < 0.02) { m.x = mt.x; m.y = mt.y; m.vx = m.vy = 0; } // arriving: start where the cursor is
      }
    }
    spring(m, 'x', tx, dt, 170, 0.9); spring(m, 'y', ty, dt, 170, 0.9);
    spring(m, 's', want, dt, 70, 0.5);                 // a little overshoot as the dots spring back
    if (Math.abs(m.s) < 0.0005 && !m.near) { m.s = 0; m.vs = 0; }
  };

  Orb.prototype._uniforms = function () {
    var c = this.cur, o = this.o, time = this.time;
    var breath = 1 + c.breathAmp * Math.sin(this.ph.breath);
    var bounce = this.state === 'speaking' ? this.level * 0.07 : this.state === 'listening' ? this.level * 0.04 : 0;
    var R = (1 / o.canvasScale) * c.scale * breath * (1 + bounce);
    var errAge = time - this.errAt, err = errAge >= 0 && errAge < 0.9 ? Math.min(1, (0.9 - errAge) / 0.5) : 0;
    var shake = errAge >= 0 && errAge < 0.55 ? Math.sin(errAge * 62) * 0.014 * (1 - errAge / 0.55) : 0;
    var swAge = time - this.sweepAt, sweep = swAge >= 0 && swAge < 1.0 ? -1.4 + swAge * 2.8 : -9;
    var ringAge = [], ringAmp = [];
    for (var i = 0; i < 4; i++) { ringAge.push(time - this.rings[i]); ringAmp.push(this.ringAmp[i]); }
    var canvasPx = this.canvas.width, pointPx = (canvasPx / o.canvasScale) / (o.size >= 160 ? 46 : 34) * 0.9;
    var light = c.light, offset = [shake, 0];
    var bright = c.bright * (1 + (this.state === 'speaking' ? this.level * 0.12 : 0));
    var still = this.reduced, m = this.mag;
    var mag = still ? 0 : Math.max(0, m.s), cursor = [m.x, m.y];
    var par = still ? [0, 0] : [clamp(m.x * Math.max(0, m.s), -1, 1) * 0.22, clamp(m.y * Math.max(0, m.s), -1, 1) * -0.22];
    var shAge = time - this.shockAt, shock = [Math.max(0, shAge), !still && shAge >= 0 && shAge < 0.85 ? 1 : 0];
    var rimA = ((time % 6) / 6) * Math.PI * 2 + Math.PI / 2, breath01 = 0.5 + 0.5 * Math.sin(this.ph.breath);
    return {
      additive: light < 0.5,
      quad: {
        uR: R, uPx: 2 / canvasPx, uCoreT: this.ph.core, uLight: light, uGlow: c.glow, uThink: c.think, uErr: err,
        uSweep: sweep, uLevel: this.level, uBright: bright, uPulse: this.state === 'listening' ? this.level : 0, uTime: time % 1000,
        uOffset: offset, uC1: c.c1, uC2: c.c2, uC3: c.c3, uK1: c.k1, uK2: c.k2, uGold: GOLD, uRingAge: ringAge, uRingAmp: ringAmp,
        uMag: mag, uCursor: cursor, uPar: par, uAurora: 0.5 + 0.5 * breath01, uAurT: this.ph.aur, uRimA: rimA, uRimK: 0.55, uShadowK: breath01,
      },
      pts: {
        uNoiseT: this.ph.noise, uRipT: this.ph.rip, uSpinA: this.ph.spin, uSwirlT: this.ph.swirl, uTime: time % 1000,
        uAmp: c.amp * c.ampMul, uFreq: c.freq, uRip: c.rip, uLevel: this.level, uSwirl: c.swirl, uInflow: c.inflow, uSpark: c.spark,
        uTilt: 0.38, uR: R, uPointPx: pointPx, uThink: c.think, uErr: err, uSweep: sweep, uBright: bright, uLight: light,
        uOffset: offset, uC1: c.c1, uC2: c.c2, uC3: c.c3, uGold: GOLD,
        uMag: mag, uCursor: cursor, uPar: par, uShock: shock, uOrbT: this.ph.orbit, uOrbit: still ? 0 : 0.9, uRimA: rimA, uRimK: 0.55,
      },
    };
  };

  Orb.prototype.render = function () {
    if (this.destroyed || this.contextLost || !this.r) return;
    try { this.r.draw(this._uniforms()); } catch (_e) { /* a lost context mid-frame — the lost handler recovers */ }
  };

  // ── public API ─────────────────────────────────────────────────────────────
  Orb.prototype.setState = function (s) {
    if (!STATES[s] || s === this.state) return this;
    var was = this.state; this.state = s;
    if (s === 'pressed') { this.pressAt = this.time; this.shockAt = this.time; this.ring(0.9); }
    if (s !== 'listening' && s !== 'speaking' && !this.levelFn) this.levelRaw = 0;
    void was; this._kickRender(); return this;
  };
  Orb.prototype.setHover = function (on) { this.hoverOn = !!on; this._kickRender(); return this; };
  Orb.prototype.press = function () { this.ring(0.9); this.pressAt = this.time; this.shockAt = this.time; return this; };
  Orb.prototype.setMagnetic = function (on) { this.o.magnetic = !!on; return this; };
  Orb.prototype.setMagnetStrength = function (v) { this.o.magnet = clamp(+v || 0, 0, 2); return this; };
  Orb.prototype.ring = function (amp) {
    var i = this.ringNext; this.ringNext = (this.ringNext + 1) % 4;
    this.rings[i] = this.time; this.ringAmp[i] = amp == null ? 0.8 : amp; return this;
  };
  Orb.prototype.flash = function (kind) {
    if (kind === 'success') this.sweepAt = this.time;
    if (kind === 'error') this.errAt = this.time;
    this._kickRender(); return this;
  };
  Orb.prototype.setLevel = function (v) { this.levelRaw = clamp(+v || 0, 0, 1); return this; };
  Orb.prototype.setLevelSource = function (fn) { this.levelFn = typeof fn === 'function' ? fn : null; return this; };
  Orb.prototype._setThemeName = function (t) { if (t !== this.themeName) { this.themeName = t; this._kickRender(); } };
  Orb.prototype.setTheme = function (t) { this.o.theme = t; this._setThemeName(t === 'auto' ? autoTheme() : t); return this; };
  Orb.prototype._setBucket = function (b) { if (PERSONALITY[b] && b !== this.bucket) { this.bucket = b; this._kickRender(); } };
  Orb.prototype.setTime = function (b) { this.bucketMode = b; this._setBucket(b === 'auto' ? bucketFor() : b); return this; };
  Orb.prototype.setReducedMotion = function (on) {
    this.reduced = !!on; this.host.classList.toggle('lt-orb-reduced', this.reduced);
    if (this.reduced) { this._stop(); this.step(0); this.render(); } else this._start();
    return this;
  };
  // A static (reduced-motion) orb still re-renders on theme / time / state changes.
  Orb.prototype._kickRender = function () {
    if (!this.reduced) return;
    var c = this.cur, per = PERSONALITY[this.bucket];
    for (var i = 0; i < SHAPE_KEYS.length; i++) c[SHAPE_KEYS[i]] = per[SHAPE_KEYS[i]];
    for (var j = 0; j < COLOR_KEYS.length; j++) c[COLOR_KEYS[j]] = hex(per[COLOR_KEYS[j]]);
    c.light = themeLight(this.themeName);
    this.render();
  };
  Orb.prototype.pause = function (reason) { this.pauses[reason || 'manual'] = true; this._stop(); return this; };
  Orb.prototype.resume = function (reason) { delete this.pauses[reason || 'manual']; this._start(); return this; };
  Orb.prototype.setSize = function (px) { this.o.size = px; this._size(); this.render(); return this; };
  Orb.prototype.loseContext = function () { return this.r && this.r.lose ? this.r.lose() : false; };
  Orb.prototype.info = function () {
    return { renderer: this.reduced ? 'static-' + (this.r ? this.r.kind : 'none') : (this.r ? this.r.kind : 'none'), fps: this.stats.fps,
      frameMs: this.stats.ms, running: this.running, paused: Object.keys(this.pauses), state: this.state, bucket: this.bucket,
      theme: this.themeName, points: this.geo.count, level: +this.level.toFixed(3), magnet: +this.mag.s.toFixed(3), near: this.mag.near, glError: this.glError || null };
  };
  Orb.prototype.destroy = function () {
    this.destroyed = true; this._stop(); clearTimeout(this._lostTimer); clearInterval(this._timeTimer);
    root.document.removeEventListener('visibilitychange', this._onVis);
    ['pointermove', 'pointerdown', 'pointerup'].forEach(function (t) { root.document.removeEventListener(t, this._onPtr); }, this);
    root.document.removeEventListener('pointerout', this._onPtrOut); root.removeEventListener('scroll', this._onScroll, true); root.removeEventListener('resize', this._onScroll);
    if (this._io) this._io.disconnect(); if (this._mo) this._mo.disconnect();
    if (this._mq && this._onMq) { try { if (this._mq.removeEventListener) this._mq.removeEventListener('change', this._onMq); else this._mq.removeListener(this._onMq); } catch (_e) {} }
    if (this.r) this.r.destroy();
    if (this.canvas && this.canvas.parentNode) this.canvas.parentNode.removeChild(this.canvas);
    this.host.classList.remove('lt-orb-reduced');
  };

  return {
    create: function (host, opts) { return new Orb(host, opts); },
    bucketFor: bucketFor, bucketForHour: bucketForHour, melbourneHour: melbourneHour,
    BUCKETS: BUCKETS, PERSONALITY: PERSONALITY, STATES: STATES,
    magnetTarget: magnetTarget, spring: spring, SHADERS: { POINTS_VS: POINTS_VS, POINTS_FS: POINTS_FS, QUAD_VS: QUAD_VS, QUAD_FS: QUAD_FS },
  };
}));
