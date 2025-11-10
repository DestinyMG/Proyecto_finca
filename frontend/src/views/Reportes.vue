<template>
    <BaseAdmin>
        <div class="produccion-leche-container">
            <h2>Estadísticas de Producción de Leche</h2>

            <!-- Estadísticas Generales -->
            <div class="estadisticas-generales">
                <h3>Producción General del Hato</h3>

                <div>
                    <label>Filtrar por año:</label>
                    <input type="number" v-model.number="filtroAnio" @change="cargarEstadisticasGenerales" />
                </div>

                <div v-if="estadisticasGenerales">
                    <p><strong>Total anual:</strong> {{ estadisticasGenerales.total_anual }} litros</p>

                    <!-- Gráfico general -->
                    <div class="grafico-pie-container">
                        <Pie v-if="chartGeneralDataSafe" :data="chartGeneralDataSafe" :options="chartOptions" />
                    </div>
                </div>
            </div>

            <hr />

            <!-- Estadísticas por Animal -->
            <div class="estadisticas-animal">
                <h3>Producción por Animal</h3>

                <div class="animal-search">
                    <input v-model="codigoAnimal" placeholder="Código del Animal" />
                    <button type="button" @click="buscarAnimal">Buscar Animal</button>
                </div>

                <div v-if="animalSeleccionado">
                    <p><strong>Animal:</strong> {{ animalSeleccionado.codigoAnimal }} ({{ animalSeleccionado.tipo }})
                    </p>
                    <p><strong>Sexo:</strong> {{ animalSeleccionado.sexo }}</p>

                    <div v-if="estadisticasAnimal">
                        <p><strong>Total anual:</strong> {{ estadisticasAnimal.total_anual }} litros</p>

                        <!-- Gráfico animal -->
                        <div class="grafico-pie-container">
                            <Pie v-if="chartAnimalDataSafe" :data="chartAnimalDataSafe" :options="chartOptions" />
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </BaseAdmin>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import BaseAdmin from "../components/BaseAdmin.vue";

import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from "chart.js";
import { Pie } from "vue-chartjs";

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const API_PRODUCCION = "https://proyecto-finca-yxcf.onrender.com/api3/produccion/";
const API_ANIMALES = "https://proyecto-finca-yxcf.onrender.com/api1/animales/";

// Variables generales
const filtroAnio = ref(new Date().getFullYear());
const estadisticasGenerales = ref(null);
const chartGeneralData = ref({
    labels: [],
    datasets: [{ label: "Litros", data: [], backgroundColor: [] }]
});

const codigoAnimal = ref("");
const animalSeleccionado = ref(null);
const estadisticasAnimal = ref(null);
const chartAnimalData = ref({
    labels: [],
    datasets: [{ label: "Litros", data: [], backgroundColor: [] }]
});

// Opciones comunes de Chart.js
const chartOptions = {
    responsive: true,
    plugins: { legend: { position: "bottom" } }
};

// ====================
// Props de gráficos seguros
// ====================
const chartGeneralDataSafe = computed(() => {
    if (!chartGeneralData.value.labels?.length) return null;

    return {
        labels: chartGeneralData.value.labels,
        datasets: [
            {
                label: "Litros",
                data: chartGeneralData.value.datasets[0].data,
                backgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF",
                    "#FF9F40",
                    "#C9CBCF",
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF"
                ]
            }
        ]
    };
});

const chartAnimalDataSafe = computed(() => {
    if (!chartAnimalData.value.labels?.length) return null;

    return {
        labels: chartAnimalData.value.labels,
        datasets: [
            {
                label: "Litros",
                data: chartAnimalData.value.datasets[0].data,
                backgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF",
                    "#FF9F40",
                    "#C9CBCF",
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF"
                ]
            }
        ]
    };
});

// ====================
// Cargar estadísticas generales
// ====================
const cargarEstadisticasGenerales = async () => {
    try {
        const res = await axios.get(
            `${API_PRODUCCION}estadisticas_generales/?año=${filtroAnio.value}`
        );

        estadisticasGenerales.value = res.data;

        chartGeneralData.value.labels =
            res.data?.produccion_mensual?.map(m => `Mes ${m.mes}`) || [];

        chartGeneralData.value.datasets[0].data =
            res.data?.produccion_mensual?.map(m => m.litros || 0) || [];

    } catch (err) {
        console.error("Error cargando estadísticas generales:", err);
    }
};


// ====================
// Buscar Animal
// ====================
const buscarAnimal = async () => {
    if (!codigoAnimal.value.trim()) return alert("Ingrese un código de animal");

    try {
        const resAnimal = await axios.get(`${API_ANIMALES}?codigoAnimal=${codigoAnimal.value.trim()}`);
        if (!resAnimal.data.length) {
            alert("Animal no encontrado");
            animalSeleccionado.value = null;
            estadisticasAnimal.value = null;
            chartAnimalData.value.labels = [];
            chartAnimalData.value.datasets[0].data = [];
            return;
        }

        animalSeleccionado.value = resAnimal.data[0];

        const resEst = await axios.get(`${API_PRODUCCION}estadisticas_animal/?animal_id=${animalSeleccionado.value.id}`);
        estadisticasAnimal.value = resEst.data;

        chartAnimalData.value.labels = resEst.data?.produccion_mensual?.map(m => `Mes ${m.mes}`) || [];
        chartAnimalData.value.datasets[0].data = resEst.data?.produccion_mensual?.map(m => m.litros || 0) || [];
    } catch (err) {
        console.error("Error buscando animal:", err);
        alert("Error al buscar animal o traer estadísticas");
    }
};

// ====================
// Inicialización
// ====================
onMounted(() => {
    cargarEstadisticasGenerales();
});
</script>



<style scoped>
/* Contenedor principal */
.produccion-leche-container {
    padding: 30px;
    max-width: 1200px;
    margin: 0 auto;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
}

/* Títulos */
h2 {
    font-size: 2rem;
    margin-bottom: 20px;
    text-align: center;
    color: #2c3e50;
}

h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    color: #34495e;
}

/* Secciones */
.estadisticas-generales,
.estadisticas-animal {
    background: #f9f9f9;
    padding: 20px 25px;
    margin-bottom: 30px;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
}

/* Separador */
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 40px 0;
}

/* Inputs y botones */
input[type="number"],
input[type="text"] {
    padding: 8px 12px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-left: 10px;
    width: 120px;
    transition: all 0.2s ease;
}

input[type="number"]:focus,
input[type="text"]:focus {
    outline: none;
    border-color: #36a2eb;
    box-shadow: 0 0 5px rgba(54, 162, 235, 0.3);
}

/* Botones */
button {
    padding: 8px 15px;
    font-size: 1rem;
    background-color: #36a2eb;
    border: none;
    border-radius: 5px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-left: 5px;
}

button:hover {
    background-color: #2b85c7;
}

/* Búsqueda de animal */
.animal-search {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

/* Párrafos de estadísticas */
.estadisticas-generales p,
.estadisticas-animal p {
    font-size: 1rem;
    margin: 8px 0;
}

/* Gráficos */
canvas {
    max-width: 100%;
    margin-top: 20px;
}

/* Responsive */
@media (max-width: 768px) {
    .animal-search {
        flex-direction: column;
        align-items: flex-start;
    }

    input[type="number"],
    input[type="text"] {
        width: 100%;
        margin-left: 0;
        margin-bottom: 10px;
    }

    button {
        width: 100%;
        margin-left: 0;
    }
}

.produccion-leche-container {
    padding: 20px;
}

h2,
h3,
h4 {
    margin-bottom: 10px;
}

.estadisticas-generales,
.estadisticas-animal {
    margin-bottom: 40px;
}

.animal-search {
    margin-bottom: 10px;
}

input {
    margin: 0 5px 10px 0;
}

.grafico-pie-container {
    width: 500px;
    height: 500px;
    margin: 20px auto;
}
</style>
