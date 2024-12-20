<template>
  <div ref="threeCanvas" style="width: 100vh; height: 100vh;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import data from './example_response.json'

const threeCanvas = ref<HTMLDivElement | null>(null);

onMounted(() => {
  // === Создание сцены и основных компонентов ===
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    50,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  const renderer = new THREE.WebGLRenderer();

  // Установка размеров рендера
  renderer.setSize(window.innerWidth, window.innerHeight);
  if (threeCanvas.value) {
    threeCanvas.value.appendChild(renderer.domElement);
  }

  camera.position.set(150, 150, 150);
  camera.lookAt(0, 0, 0);

  // === Контроллеры OrbitControls ===
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; // Плавность движения
  controls.dampingFactor = 0.1;

  // === Оси X, Y, Z ===
  const axesHelper = new THREE.AxesHelper(10);
  scene.add(axesHelper);

  // === Свет ===
  const ambientLight = new THREE.AmbientLight(0xffffff, 1);
  scene.add(ambientLight);

  // Добавление объектов в сцену
  addObjects(scene);

  // === Анимация ===
  const animate = () => {
    controls.update(); // Обновление управления
    renderer.render(scene, camera);
    requestAnimationFrame(animate); // Цикл анимации
  };
  animate();

  // === Обновление размеров окна ===
  const handleResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  };
  window.addEventListener('resize', handleResize);

  // === Очистка при уничтожении ===
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
    controls.dispose();
    renderer.dispose();
  });
});

// Функция добавления объектов в сцену
const addObjects = (scene: THREE.Scene) => {

  // const orangeColors = [
  //   [83, 7, 42], [97, 30, 43], [134, 127, 22], [80, 27, 21], [149, 88, 21],
  //   [112, 7, 36], [137, 47, 9], [136, 81, 30], [134, 45, 4], [147, 40, 57],
  //   [176, 70, 30], [137, 112, 4], [133, 36, 26], [143, 57, 52], [110, 45, 54],
  //   [73, 70, 53], [143, 131, 53], [94, 28, 42], [177, 37, 59], [172, 74, 6],
  //   [88, 140, 39], [98, 7, 19], [39, 50, 46], [142, 43, 4], [157, 45, 6],
  //   [145, 63, 0], [122, 146, 15]
  // ];

  // const blueColors = [
  //   [75, 67, 56], [122, 149, 14], [90, 37, 13], [176, 64, 36], [78, 74, 13],
  //   [141, 106, 7], [76, 65, 57], [84, 1, 37], [107, 39, 59], [74, 74, 15],
  //   [95, 5, 17], [119, 144, 16], [83, 2, 47], [143, 58, 50], [140, 77, 27],
  //   [83, 24, 19], [131, 41, 0], [102, 3, 20], [138, 50, 8], [144, 37, 55],
  //   [176, 40, 59], [89, 143, 39], [112, 1, 41], [134, 78, 34], [137, 125, 21],
  //   [130, 123, 24], [111, 1, 31], [73, 67, 57], [95, 31, 41], [69, 126, 32],
  //   [157, 44, 3], [133, 78, 27], [149, 59, 0], [76, 74, 16], [137, 43, 14],
  //   [96, 25, 48], [94, 27, 45], [75, 41, 8], [68, 117, 34], [140, 112, 4],
  //   [146, 130, 52], [85, 22, 19], [145, 61, 3], [74, 66, 49], [69, 128, 35]
  // ];

  // const greenColors = [
  //   [101, 98, 26]
  // ];

  // const redColors = [
  //   [163, 85, 7], [162, 85, 7], [161, 85, 7], [160, 85, 7], [160, 85, 8]
  // ];

  const orangeColors = [];
  const blueColors = [];
  const greenColors = [];
  const redColors = [];

  data.food.forEach(item => {
    orangeColors.push(item.c);
  });
  ['golden', 'suspicious'].forEach(foodType => {
    if (data.specialFood[foodType]) {
      data.specialFood[foodType].forEach(item => {
        orangeColors.push(item);
      });
    }
  });

  // Заполняем blueColors из fences
  data.fences.forEach(fence => {
    blueColors.push(fence);
  });

  // Заполняем greenColors из snakes (направления)
  data.snakes.forEach(snake => {
    greenColors.push(snake.geometry[0]);
  });

  // Заполняем redColors из enemies (геометрии)
  data.enemies.forEach(enemy => {
    redColors.push(enemy.geometry[0]);
  });

  // Создание геометрии квадрата
  const squareSize = 1; // Размер квадрата
  const geometry = new THREE.BoxGeometry(squareSize, squareSize, squareSize);

  const orangeMaterial = new THREE.MeshBasicMaterial({ color: 0xffa500 });
  const greenMaterial = new THREE.MeshBasicMaterial({ color: 0x00FF00 });
  const blueMaterial = new THREE.MeshBasicMaterial({ color: 0x0000FF });
  const redMaterial = new THREE.MeshBasicMaterial({ color: 0xFF0000 });

  orangeColors.forEach(element => {
    const cube = new THREE.Mesh(geometry, orangeMaterial);
    cube.position.set(element[0], element[1], element[2]);
    scene.add(cube);
  });

  greenColors.forEach(element => {
    const cube = new THREE.Mesh(geometry, greenMaterial);
    cube.position.set(element[0], element[1], element[2]);
    scene.add(cube);
  });

  blueColors.forEach(element => {
    const cube = new THREE.Mesh(geometry, blueMaterial);
    cube.position.set(element[0], element[1], element[2]);
    scene.add(cube);
  });

  redColors.forEach(element => {
    const cube = new THREE.Mesh(geometry, redMaterial);
    cube.position.set(element[0], element[1], element[2]);
    scene.add(cube);
  });

  // // Создание материала для квадрата (красный цвет)
  // const material = new THREE.MeshBasicMaterial({ color: 0xff1000 });

  // // Создание меша (геометрия + материал)
  // const redCube = new THREE.Mesh(geometry, material);
  // const redCube1 = new THREE.Mesh(geometry, material);

  // // Установка позиции квадрата
  // redCube.position.set(0, 0, 0);
  // redCube1.position.set(1, 0, 0);

  // // Добавление квадрата в сцену
  // scene.add(redCube);
  // scene.add(redCube1);
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

#app,
div[ref="threeCanvas"] {
  width: 100%;
  height: 100%;
}
</style>
