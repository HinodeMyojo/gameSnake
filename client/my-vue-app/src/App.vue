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
import data from './example_response.json'

const threeCanvas = ref<HTMLDivElement | null>(null);

var snake_1_lenght = ref(0);
var snake_2_lenght = ref(0);
var snake_3_lenght = ref(0);

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
  var counter = 0;
  data.snakes.forEach(snake => {
    snake.geometry.forEach(item => {
      greenColors.push(item); // Добавляем элемент в greenColors
    });
    counter += 1;
    if (counter == 1) {
      snake_1_lenght.value = snake.geometry.length;
    } else if (counter == 2) {
      snake_2_lenght.value = snake.geometry.length;
    } else if (counter == 3) {
      snake_3_lenght.value = snake.geometry.length;
    }

  });

  // Заполняем redColors из enemies (геометрии)
  data.enemies.forEach(enemy => {
    enemy.geometry.forEach(item => {
      redColors.push(item); // Добавляем все элементы из geometry в redColors
    });
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


  // // Создание материала я квадрата (красный цвет)
  // const material = new TEE.MeshBasicMaterial({ color: 0xff1000 });

  // // Создание меша (геомрия + материал)
  // const redCube = new THE.Mesh(geometry, material);
  // const redCube1 = new TEE.Mesh(geometry, material);

  // // Установка позиции кдрата
  // redCube.position.set(00, 0);
  // redCube1.position.set( 0, 0);

  // // Добавление квадрата сцену
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
