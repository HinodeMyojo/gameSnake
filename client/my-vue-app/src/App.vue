<template>
  <div style="display: flex; gap: 10px;">
    <p>Длина первой змеи = {{ snake_1_lenght }}</p>
    <p>Длина второй змеи = {{ snake_2_lenght }}</p>
    <p>Длина третьей змеи = {{ snake_3_lenght }}</p>
  </div>
  <div ref="threeCanvas" style="width: 100vh; height: 100vh;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
// import data from './example_response.json'
import axios from 'axios';

const threeCanvas = ref<HTMLDivElement | null>(null);

var snake_1_lenght = ref(0);
var snake_2_lenght = ref(0);
var snake_3_lenght = ref(0);


const token = '452cc499-268d-4d8f-9948-fcaa0aba839d';
const serverUrl = 'https://games-test.datsteam.dev/play/snake3d';
const api = '/player/move';
const dataRequest = {
  snakes: [

  ]
}
const url = `${serverUrl}${api}`;

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


  // setInterval(() => {
  //   // Очищаем сцену перед добавлением новых объектов, кроме света и вспомогательных элементов
  //   scene.children = scene.children.filter(
  //     obj => obj.type === 'AmbientLight' || obj.type === 'AxesHelper'
  //   );
  //   addObjects(scene);
  // }, 1000);
  setInterval(() => addObjects(scene), 1000);

  // === Очистка при уничтожении ===
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
    controls.dispose();
    renderer.dispose();
  });
});

const Request = async () => {
  const response = await axios.post(url, dataRequest, {
    headers: {
      'X-Auth-Token': `${token}`,
      'Content-Type': 'application/json',
    }
  });
  console.log(response);
  return response;

}

// Функция добавления объектов в сцену
const objectMap: Record<string, THREE.Mesh> = {}; // Карта объектов для управления добавлением/удалением

const addObjects = async (scene: THREE.Scene) => {
  const orangeColors = [];
  const blueColors = [];
  const greenColors = [];
  const redColors = [];

  const data = (await Request()).data;

  // === Сбор данных ===
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

  data.fences.forEach(fence => {
    blueColors.push(fence);
  });

  let counter = 0;
  data.snakes.forEach(snake => {
    snake.geometry.forEach(item => {
      greenColors.push(item);
    });
    counter += 1;
    if (counter === 1) {
      snake_1_lenght.value = snake.geometry.length;
    } else if (counter === 2) {
      snake_2_lenght.value = snake.geometry.length;
    } else if (counter === 3) {
      snake_3_lenght.value = snake.geometry.length;
    }
  });

  data.enemies.forEach(enemy => {
    enemy.geometry.forEach(item => {
      redColors.push(item);
    });
  });

  // === Материалы для объектов ===
  const orangeMaterial = new THREE.MeshBasicMaterial({ color: 0xffa500 });
  const greenMaterial = new THREE.MeshBasicMaterial({ color: 0x00FF00 });
  const blueMaterial = new THREE.MeshBasicMaterial({ color: 0x0000FF });
  const redMaterial = new THREE.MeshBasicMaterial({ color: 0xFF0000 });

  const createOrUpdateCube = (key: string, position: number[], material: THREE.Material) => {
    if (objectMap[key]) {
      // Если объект существует, обновляем его позицию
      objectMap[key].position.set(position[0], position[1], position[2]);
    } else {
      // Если объекта нет, создаём новый
      const geometry = new THREE.BoxGeometry(1, 1, 1);
      const cube = new THREE.Mesh(geometry, material);
      cube.position.set(position[0], position[1], position[2]);
      scene.add(cube);
      objectMap[key] = cube;
    }
  };

  // === Создание или обновление объектов ===
  orangeColors.forEach((pos, index) => createOrUpdateCube(`orange-${index}`, pos, orangeMaterial));
  greenColors.forEach((pos, index) => createOrUpdateCube(`green-${index}`, pos, greenMaterial));
  blueColors.forEach((pos, index) => createOrUpdateCube(`blue-${index}`, pos, blueMaterial));
  redColors.forEach((pos, index) => createOrUpdateCube(`red-${index}`, pos, redMaterial));

  // === Удаление старых объектов ===
  const allKeys = [
    ...orangeColors.map((_, index) => `orange-${index}`),
    ...greenColors.map((_, index) => `green-${index}`),
    ...blueColors.map((_, index) => `blue-${index}`),
    ...redColors.map((_, index) => `red-${index}`),
  ];
  for (const key in objectMap) {
    if (!allKeys.includes(key)) {
      // Удаляем объект из сцены и освобождаем память
      scene.remove(objectMap[key]);
      objectMap[key].geometry.dispose();
      objectMap[key].material.dispose();
      delete objectMap[key];
    }
  }
};

// === Обновление сцены каждую секунду ===





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
