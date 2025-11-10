<template>
    <BaseAdmin>
        <div class="produccion-leche-container">
            <h2>Estadísticas de Producción de Leche</h2>

            <!-- Estadísticas Generales -->
            <div class="estadisticas-generales">
                <h3>Producción General del Hato</h3>

                <div class="anio-filter">
                    <label>Filtrar por año:</label>
                    <input type="number" v-model.number="filtroAnio" />

                    <button @click="cargarEstadisticasGenerales">
                        Buscar Año
                    </button>
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

// Animal
const codigoAnimal = ref("");
const animalSeleccionado = ref(null);
const estadisticasAnimal = ref(null);
const chartAnimalData = ref({
    labels: [],
    datasets: [{ label: "Litros", data: [], backgroundColor: [] }]
});

// Opciones Chart.js
const chartOptions = {
    responsive: true,
    plugins: { legend: { position: "bottom" } }
};

// ====================
// PROP GRÁFICO GENERAL
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
                    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                    "#9966FF", "#FF9F40", "#C9CBCF", "#FF6384",
                    "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"
                ]
            }
        ]
    };
});

// ====================
// PROP GRÁFICO ANIMAL
// ====================
const chartAnimalDataSafe = computed(() => {
    if (!chartAnimalData.value.labels?.length) return null;

    return {
        labels: chartAnimalData.value.labels,
        datasets: [
            {
                label: "Litros",
                data: chartAnimalData.value.datasets[0].data,
                backgroundColor: [
                    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                    "#9966FF", "#FF9F40", "#C9CBCF", "#FF6384",
                    "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"
                ]
            }
        ]
    };
});

// ====================
// CARGAR ESTADÍSTICAS GENERALES SEGÚN AÑO
// ====================
const cargarEstadisticasGenerales = async () => {
    try {
        const res = await axios.get(
            `${API_PRODUCCION}estadisticas_generales/?año=${filtroAnio.value}`
        );

        estadisticasGenerales.value = res.data;

        chartGeneralData.value.labels = res.data?.produccion_mensual?.map(m => `Mes ${m.mes}`) || [];
        chartGeneralData.value.datasets[0].data = res.data?.produccion_mensual?.map(m => m.litros || 0) || [];

    } catch (err) {
        console.error("Error cargando estadísticas generales:", err);
        alert("No se pudo cargar la información.");
    }
};

// ====================
// BUSCAR ANIMAL
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

        const resEst = await axios.get(
            `${API_PRODUCCION}estadisticas_animal/?animal_id=${animalSeleccionado.value.id}&año=${filtroAnio.value}`
        );

        estadisticasAnimal.value = resEst.data;

        chartAnimalData.value.labels = resEst.data?.produccion_mensual?.map(m => `Mes ${m.mes}`) || [];
        chartAnimalData.value.datasets[0].data = resEst.data?.produccion_mensual?.map(m => m.litros || 0) || [];

    } catch (err) {
        console.error("Error buscando animal:", err);
        alert("Error al buscar animal o traer estadísticas");
    }
};

// ====================
// Al cargar la página → carga el año actual
// ====================
onMounted(() => {
    cargarEstadisticasGenerales();
});
</script>


<style scoped>
/* ---------- CONTENEDOR GENERAL ---------- */

.produccion-leche-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.produccion-leche-container h2 {
    text-align: center;
    color: #2d5016;
    margin-bottom: 25px;
}


/* ---------- TARJETAS (Mis mismos estilos de antes) ---------- */

.form-card,
.historial-card {
    background: linear-gradient(135deg, #f0f8f0 0%, #e0f0e0 100%);
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #7cb068;
    margin-bottom: 25px;
}

.form-card h3,
.historial-card h3 {
    color: #2d5016;
    margin-bottom: 15px;
}


/* ---------- BUSCADOR DE ANIMAL ---------- */

.animal-search {
    display: flex;
    gap: 10px;
}

.animal-search input {
    flex: 1;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #9bbb8b;
}

.animal-search button {
    padding: 8px 15px;
    background-color: #7cb068;
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.2s ease;
}

.animal-search button:hover {
    background-color: #6b9a59;
}


/* ---------- INFO DEL ANIMAL ---------- */

.animal-info {
    margin-top: 10px;
    padding: 12px;
    background: #ffffff;
    border-left: 5px solid #7cb068;
    border-radius: 8px;
    line-height: 1.4;
}

.animal-info p strong {
    color: #2d5016;
}


/* ---------- FORMULARIO ---------- */

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    font-weight: bold;
    color: #2d5016;
}

.form-group input {
    width: 100%;
    padding: 8px 12px;
    margin-top: 5px;
    border-radius: 8px;
    border: 1px solid #9bbb8b;
}

.form-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.form-actions button {
    padding: 10px 18px;
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    transition: 0.2s;
}

.form-actions button[type="submit"] {
    background-color: #4caf50;
}

.form-actions button[type="submit"]:hover {
    background-color: #449a47;
}

.form-actions button[type="button"] {
    background-color: #e57373;
}

.form-actions button[type="button"]:hover {
    background-color: #d16464;
}


/* ---------- HISTORIAL DE PRODUCCIÓN ---------- */

.historial-card h4 {
    color: #2d5016;
    margin-bottom: 8px;
}

.registro-item {
    padding: 15px;
    background: #ffffff;
    border-radius: 10px;
    border-left: 5px solid #7cb068;
    margin-bottom: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.07);
}

.registro-item p strong {
    color: #2d5016;
}

/* Línea divisoria */
.registro-item hr {
    margin-top: 12px;
    border: 0;
    border-top: 1px solid #c7d8c3;
}

/* Botones del registro */
.registro-actions {
    margin-top: 10px;
    display: flex;
    gap: 10px;
}

.registro-actions button {
    padding: 7px 14px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
    color: #fff;
}

.registro-actions button:first-child {
    background-color: #4c8bbd;
}

.registro-actions button:first-child:hover {
    background-color: #3e7aa7;
}

.registro-actions button:last-child {
    background-color: #e05b5b;
}

.registro-actions button:last-child:hover {
    background-color: #c84f4f;
}
</style>