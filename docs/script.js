import * as THREE from './three.module.js';
import { OrbitControls } from "./OrbitControls.js";

const defaultCube = 'lifecubeproject';
let url = new URL(document.location);
let cube = url.searchParams.get('c') || defaultCube;
let camera, renderer;
const scene = new THREE.Scene();
let mesh;
const loadManager = new THREE.LoadingManager();
const loader = new THREE.TextureLoader(loadManager);

init();
animate();

function loadCube(name) {
  cube = name;

  loader.setPath('textures-' + cube + '/');
  let materials = [];
  for (let i = 0; i < 6; i++) {
    materials.push(new THREE.MeshBasicMaterial({
      map: loader.load(cube + '-' + i + '.jpg')}));
    materials[i].map.minFilter = THREE.LinearMipmapLinearFilter;
    materials[i].side = THREE.DoubleSide;
  }
  loadManager.onLoad = () => {
    const geometry = new THREE.BoxGeometry(200, 200, 200);
    mesh = new THREE.Mesh(geometry, materials);
    scene.add(mesh);
  }
  loadManager.onError = () => {
    if (cube != defaultCube) {
      window.alert("Cube " + cube + " not found, using default " + defaultCube);
      loadCube(defaultCube);
    }
  }
}

function init() {
  // Ensure hashtags are in alphabetical order
  const ordered = cube.split(',').sort().join();
  if (ordered != cube) {
    url.searchParams.set('c', ordered);
    window.location.href = url.toString();
  }
  loadCube(cube);

  camera = new THREE.PerspectiveCamera(
    70, window.innerWidth / window.innerHeight, 1, 1000 );
  camera.position.z = 400;

  // Source: https://svs.gsfc.nasa.gov/4851
  // Processed with https://viewer.openhdr.org/ and
  // https://matheowis.github.io/HDRI-to-CubeMap/
  scene.background = (new THREE.CubeTextureLoader()).load([
    'starfield_cubemap_512/px.png',
    'starfield_cubemap_512/nx.png',
    'starfield_cubemap_512/py.png',
    'starfield_cubemap_512/ny.png',
    'starfield_cubemap_512/pz.png',
    'starfield_cubemap_512/nz.png'
  ]);

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
