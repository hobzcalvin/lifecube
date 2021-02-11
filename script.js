import * as THREE from './three.module.js';
import { OrbitControls } from "./OrbitControls.js";

let camera, scene, renderer;
let mesh;

init();
animate();

function init() {

  camera = new THREE.PerspectiveCamera(
    70, window.innerWidth / window.innerHeight, 1, 1000 );
  camera.position.z = 400;

  scene = new THREE.Scene();

  const texture = new THREE.TextureLoader().load('pexels.jpg');

  const geometry = new THREE.BoxGeometry(200, 200, 200);
  const material = new THREE.MeshBasicMaterial({ map: texture });

  mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  let controls = new OrbitControls(camera, renderer.domElement);
  controls.update();

  window.addEventListener('resize', onWindowResize);
  renderer.render(scene, camera);
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render( scene, camera );
}
