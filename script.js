import * as THREE from './three.module.js';
import { OrbitControls } from "./OrbitControls.js";

const hashtag = 'lifecubeproject';
let camera, scene, renderer;
let mesh;

init();
animate();

function init() {

  camera = new THREE.PerspectiveCamera(
    70, window.innerWidth / window.innerHeight, 1, 1000 );
  camera.position.z = 400;

  scene = new THREE.Scene();

  const loadManager = new THREE.LoadingManager();
  const loader = new THREE.TextureLoader(loadManager);
  loader.setPath('textures-' + hashtag + '/');
  let materials = [];
  for (let i = 0; i < 6; i++) {
    materials.push(new THREE.MeshBasicMaterial({
      map: loader.load(hashtag + '-' + i + '.jpg')}));
    materials[i].map.minFilter = THREE.LinearMipmapLinearFilter;
    materials[i].side = THREE.DoubleSide;
  }
  loadManager.onLoad = () => {
    const geometry = new THREE.BoxGeometry(200, 200, 200);
    mesh = new THREE.Mesh(geometry, materials);
    scene.add(mesh);
  }

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  let controls = new OrbitControls(camera, renderer.domElement);
  controls.maxDistance = 900;
  controls.update();
  window.controls = controls;
  window.camera = camera;

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
