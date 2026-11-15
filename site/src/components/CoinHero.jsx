import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

// Background: an aurora of the brand colors (navy-900, blue-500, green-500),
// driven by fbm noise and nudged by the pointer.
const bgVertex = /* glsl */ `
  varying vec2 vUv;
  void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
`;
const bgFragment = /* glsl */ `
  precision highp float;
  varying vec2 vUv;
  uniform float uTime;
  uniform vec2 uMouse;
  uniform vec2 uRes;
  vec3 navy = vec3(0.0, 0.027, 0.282);
  vec3 blue = vec3(0.078, 0.392, 1.0);
  vec3 green = vec3(0.047, 0.6, 0.443);
  vec3 lime = vec3(0.376, 0.878, 0.255);
  float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float noise(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
  }
  float fbm(vec2 p) { float v = 0.0, a = 0.5; for (int i = 0; i < 5; i++) { v += a * noise(p); p *= 2.02; a *= 0.5; } return v; }
  void main() {
    vec2 uv = vUv;
    vec2 p = uv * vec2(uRes.x / uRes.y, 1.0) * 2.2;
    float t = uTime * 0.06;
    vec2 q = vec2(fbm(p + t), fbm(p + vec2(5.2, 1.3) - t));
    vec2 r = vec2(fbm(p + 3.0 * q + vec2(1.7, 9.2) + uMouse * 0.6 + t * 1.5), fbm(p + 3.0 * q + vec2(8.3, 2.8)));
    float f = fbm(p + 2.5 * r);
    vec3 col = navy;
    col = mix(col, blue, smoothstep(0.35, 0.85, f) * 0.55);
    col = mix(col, green, smoothstep(0.45, 0.95, r.y) * 0.6);
    col = mix(col, lime, smoothstep(0.82, 1.05, f * r.x * 1.6) * 0.25);
    float vig = smoothstep(1.25, 0.25, length(uv - vec2(0.5, 0.45)));
    col *= mix(0.55, 1.0, vig);
    col += (hash(uv * uRes + uTime) - 0.5) * 0.025; // film grain
    gl_FragColor = vec4(col, 1.0);
  }
`;

function coinFaceTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const grad = g.createRadialGradient(100, 90, 20, 128, 128, 128);
  grad.addColorStop(0, '#fff3a6');
  grad.addColorStop(0.55, '#f6c21c');
  grad.addColorStop(1, '#d48a00');
  g.fillStyle = grad; g.fillRect(0, 0, 256, 256);
  g.lineWidth = 14; g.strokeStyle = '#e09a00';
  g.beginPath(); g.arc(128, 128, 104, 0, Math.PI * 2); g.stroke();
  g.font = '800 150px "Plus Jakarta Sans", system-ui, sans-serif';
  g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillStyle = '#ea7e00'; g.fillText('c', 134, 140);
  g.fillStyle = '#fff503'; g.fillText('c', 128, 134);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

export default function CoinHero() {
  const ref = useRef(null);

  useEffect(() => {
    const host = ref.current;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    } catch (e) {
      host.classList.add('no-webgl');
      return undefined;
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.autoClear = false;
    host.appendChild(renderer.domElement);

    // Background pass
    const bgScene = new THREE.Scene();
    const bgCam = new THREE.Camera();
    const uniforms = { uTime: { value: 0 }, uMouse: { value: new THREE.Vector2() }, uRes: { value: new THREE.Vector2(1, 1) } };
    bgScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ vertexShader: bgVertex, fragmentShader: bgFragment, uniforms, depthWrite: false })));

    // Coins
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
    camera.position.set(0, 0, 16);
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    const key = new THREE.DirectionalLight(0xfff1c4, 2.2); key.position.set(4, 6, 8); scene.add(key);
    scene.add(new THREE.AmbientLight(0x6b8cff, 0.4));

    const face = coinFaceTexture();
    const edgeMat = new THREE.MeshStandardMaterial({ color: 0xe8a50c, metalness: 1, roughness: 0.28 });
    const faceMat = new THREE.MeshStandardMaterial({ map: face, metalness: 0.85, roughness: 0.3 });
    const geo = new THREE.CylinderGeometry(1, 1, 0.16, 64);
    const COUNT = window.innerWidth < 700 ? 14 : 26;
    // Keep most coins on the right so they don't cross the headline on wide screens.
    const spawnX = () => (window.innerWidth < 700 || Math.random() < 0.15 ? (Math.random() - 0.5) * 22 : 1.5 + Math.random() * 9.5);
    const coins = [];
    for (let i = 0; i < COUNT; i++) {
      const m = new THREE.Mesh(geo, [edgeMat, faceMat, faceMat]);
      const s = 0.45 + Math.random() * 0.75;
      m.scale.setScalar(s);
      m.userData = {
        x: spawnX(), y: (Math.random() - 0.5) * 14, z: -Math.random() * 10 + 1,
        speed: 0.25 + Math.random() * 0.5, spin: new THREE.Vector3(Math.random() * 1.2, Math.random() * 1.6, Math.random() * 0.6),
        phase: Math.random() * Math.PI * 2
      };
      m.rotation.set(Math.random() * 6, Math.random() * 6, Math.random() * 6);
      scene.add(m); coins.push(m);
    }

    const mouse = new THREE.Vector2(), target = new THREE.Vector2();
    const onMove = (e) => {
      const r = host.getBoundingClientRect();
      target.set(((e.clientX - r.left) / r.width) * 2 - 1, -(((e.clientY - r.top) / r.height) * 2 - 1));
    };
    window.addEventListener('pointermove', onMove, { passive: true });

    const resize = () => {
      const w = host.clientWidth, h = host.clientHeight;
      renderer.setSize(w, h, false);
      camera.aspect = w / h; camera.updateProjectionMatrix();
      uniforms.uRes.value.set(w, h);
    };
    const ro = new ResizeObserver(resize); ro.observe(host); resize();

    let visible = true, raf = 0, last = performance.now(), t = 0;
    const io = new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible && !raf) loop(performance.now()); }, { threshold: 0 });
    io.observe(host);

    function frame(dt) {
      t += dt;
      mouse.lerp(target, 0.05);
      uniforms.uTime.value = t; uniforms.uMouse.value.copy(mouse);
      for (const c of coins) {
        const u = c.userData;
        u.y -= u.speed * dt;
        if (u.y < -8) { u.y = 8; u.x = spawnX(); }
        c.position.set(u.x + Math.sin(t * 0.6 + u.phase) * 0.6 + mouse.x * (2 - u.z * 0.2), u.y + mouse.y * 0.8, u.z);
        c.rotation.x += u.spin.x * dt; c.rotation.y += u.spin.y * dt; c.rotation.z += u.spin.z * dt;
      }
      camera.position.x = mouse.x * 0.8; camera.position.y = mouse.y * 0.5; camera.lookAt(0, 0, 0);
      renderer.clear();
      renderer.render(bgScene, bgCam);
      renderer.clearDepth();
      renderer.render(scene, camera);
    }
    function loop(now) {
      const dt = Math.min(0.05, (now - last) / 1000); last = now;
      frame(dt);
      raf = visible && !reduce ? requestAnimationFrame(loop) : 0;
    }
    frame(0.016);
    if (!reduce) raf = requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(raf); io.disconnect(); ro.disconnect();
      window.removeEventListener('pointermove', onMove);
      geo.dispose(); edgeMat.dispose(); faceMat.dispose(); face.dispose(); pmrem.dispose(); renderer.dispose();
      host.removeChild(renderer.domElement);
    };
  }, []);

  return <div className="hero-canvas" ref={ref} aria-hidden="true" />;
}
