<template>
    <BaseAdmin>
        <template #default>
            <div class="detalle-animal-container">
                <h2>Detalle del Animal</h2>

                <!-- Cargando animal -->
                <div v-if="!animal" class="loading">
                    Cargando información del animal...
                </div>

                <!-- Datos del animal -->
                <div v-else class="animal-card">
                    <h3>{{ animal.codigoAnimal }} - {{ animal.tipo }} ({{ animal.sexo }})</h3>

                    <div class="animal-info">
                        <div v-for="(valor, clave) in camposFiltrados" :key="clave" class="info-item">
                            <strong>{{ formatLabel(clave) }}:</strong>
                            <span>
                                <template v-if="clave === 'embarazada'">{{ valor ? 'Sí' : 'No' }}</template>
                                <template v-else>{{ valor }}</template>
                            </span>
                        </div>
                    </div>
                </div>

                <!-- ✅ Historial de gestación (solo hembras) -->
                <div v-if="animal?.sexo === 'Hembra' && gestacion.length" class="gestacion-container">
                    <h3>Historial de Gestación</h3>

                    <div v-for="g in gestacion" :key="g.id" class="gestacion-item">
                        <p><strong>Estado:</strong> {{ g.estado }}</p>
                        <p><strong>Fecha Palpación:</strong> {{ g.fecha_palpacion }}</p>
                        <p v-if="g.tiempo_gestacion"><strong>Días Gestación:</strong> {{ g.tiempo_gestacion }}</p>
                        <p v-if="g.proxima_palpacion"><strong>Próxima Palpación:</strong> {{ g.proxima_palpacion }}</p>
                        <p v-if="g.observaciones"><strong>Observaciones:</strong> {{ g.observaciones }}</p>

                        <hr />
                    </div>
                </div>

                <!-- Historial sanitario -->
                <div v-if="historial.length" class="historial-container">
                    <h3>Historial Sanitario</h3>

                    <div v-for="registro in historial" :key="registro.id" class="historial-item">
                        <p><strong>Fecha:</strong> {{ registro.fecha_registro }}</p>
                        <p><strong>Estado:</strong> {{ registro.estado }}</p>
                        <p v-if="registro.enfermedad_nombre"><strong>Enfermedad:</strong> {{ registro.enfermedad_nombre
                        }}</p>
                        <p v-if="registro.tratamiento"><strong>Tratamiento:</strong> {{ registro.tratamiento }}</p>
                        <p v-if="registro.observaciones"><strong>Observaciones:</strong> {{ registro.observaciones }}
                        </p>
                        <p v-if="registro.proxima_revision"><strong>Próxima Revisión:</strong> {{
                            registro.proxima_revision }}</p>

                        <div v-if="registro.vacunas_detalle.length">
                            <strong>Vacunas:</strong>
                            <ul>
                                <li v-for="vacuna in registro.vacunas_detalle" :key="vacuna.id">
                                    {{ vacuna.nombre }} - {{ vacuna.descripcion }}
                                </li>
                            </ul>
                        </div>

                        <div v-if="registro.medicamentos_detalle.length">
                            <strong>Medicamentos:</strong>
                            <ul>
                                <li v-for="med in registro.medicamentos_detalle" :key="med.id">
                                    {{ med.nombre }} - {{ med.dosis || '-' }} - {{ med.descripcion }}
                                </li>
                            </ul>
                        </div>

                        <hr />
                    </div>
                </div>

                <!-- ✅ Historial de producción de leche (solo hembras) -->
                <div v-if="animal?.sexo === 'Hembra' && produccion.length" class="produccion-container">
                    <h3>Historial de Producción de Leche</h3>
                    <div v-for="p in produccion" :key="p.id" class="produccion-item">
                        <p><strong>Fecha:</strong> {{ p.fecha }}</p>
                        <p><strong>Litros:</strong> {{ p.litros }}</p>
                        <hr />
                    </div>
                </div>
            </div>
        </template>
    </BaseAdmin>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import BaseAdmin from '../components/BaseAdmin.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const animalId = Number(route.params.id);

// -----------------------------------------------------
// DATOS DEL ANIMAL
// -----------------------------------------------------
const animal = ref(null);
const API_ANIMALES = 'https://proyecto-finca-yxcf.onrender.com/api1/animales/';
const camposHembra = ['embarazada', 'produccionLeche', 'partos', 'fecha_palpacion', 'fecha_parto', 'codigo_madre'];

const cargarAnimal = async () => {
    try {
        const res = await axios.get(`${API_ANIMALES}${animalId}/`);
        animal.value = res.data;
    } catch (err) {
        console.error(err);
        alert('No se pudo cargar el animal');
    }
};

const camposFiltrados = computed(() => {
    if (!animal.value) return {};
    return Object.fromEntries(
        Object.entries(animal.value)
            .filter(([_, value]) => value !== null)
            .filter(([key]) => !(animal.value.sexo !== 'Hembra' && camposHembra.includes(key)))
    );
});

const formatLabel = (key) => key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

// -----------------------------------------------------
// HISTORIAL SANITARIO
// -----------------------------------------------------
const historial = ref([]);
const API_REGISTROS = 'https://proyecto-finca-yxcf.onrender.com/api2/registros/';

const cargarHistorial = async () => {
    try {
        const res = await axios.get(API_REGISTROS);
        historial.value = res.data.filter(r => r.animal === animalId);
    } catch (err) {
        console.error(err);
        alert('No se pudo cargar el historial sanitario');
    }
};

// -----------------------------------------------------
// HISTORIAL DE GESTACIÓN (solo hembras)
// -----------------------------------------------------
const gestacion = ref([]);
const API_GESTACION = 'https://proyecto-finca-yxcf.onrender.com/api4/gestacion/';

const cargarGestacion = async () => {
    try {
        const res = await axios.get(API_GESTACION);
        gestacion.value = res.data.filter(g => g.animal === animalId);
    } catch (err) {
        console.error(err);
        alert('No se pudo cargar la información de gestación');
    }
};

// -----------------------------------------------------
// HISTORIAL DE PRODUCCIÓN DE LECHE (solo hembras)
// -----------------------------------------------------
const produccion = ref([]);
const API_PRODUCCION = 'https://proyecto-finca-yxcf.onrender.com/api3/produccion/';

const cargarProduccion = async () => {
    if (!animal.value || animal.value.sexo !== 'Hembra') return;
    try {
        const res = await axios.get(`${API_PRODUCCION}?animal=${animalId}`);
        produccion.value = res.data.map(p => ({
            id: p.id,
            fecha: p.fecha,
            litros: p.litros
        }));
    } catch (err) {
        console.error(err);
        alert('No se pudo cargar la producción de leche');
    }
};

// -----------------------------------------------------
// Ejecutar todas las cargas
// -----------------------------------------------------
onMounted(() => {
    cargarAnimal();
    cargarHistorial();
    cargarGestacion();
});

// 🔹 Cuando el animal se cargue, llamar producción si es hembra
watch(animal, (newVal) => {
    if (newVal && newVal.sexo === 'Hembra') {
        cargarProduccion();
    }
});
</script>





<style scoped>
.detalle-animal-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
    text-align: center;
    color: #2d5016;
    margin-bottom: 25px;
}

.animal-card {
    background: linear-gradient(135deg, #f0f8f0 0%, #e0f0e0 100%);
    padding: 25px;
    border-radius: 12px;
    border: 2px solid #7cb068;
    margin-bottom: 20px;
}

.animal-card h3 {
    color: #2d5016;
    margin-bottom: 15px;
}

.animal-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.info-item strong {
    color: #2d5016;
    margin-right: 5px;
}

.loading {
    text-align: center;
    font-size: 1.2rem;
    color: #555;
}

.historial-container {
    margin-top: 30px;
}

.historial-item {
    background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    border-left: 4px solid #4a7c3f;
}

.historial-item strong {
    color: #2d5016;
}

.historial-item hr {
    margin-top: 10px;
    margin-bottom: 10px;
    border: none;
    border-top: 1px dashed #7cb068;
}

/* ---------- SECCIÓN GENERAL ---------- */

.gestacion-container,
.historial-container {
    margin-top: 30px;
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #7cb068;
    background: linear-gradient(135deg, #f0f8f0 0%, #e0f0e0 100%);
}

.gestacion-container h3,
.historial-container h3 {
    margin-bottom: 15px;
    color: #2d5016;
    font-size: 1.4rem;
}

/* ---------- ITEMS DEL HISTORIAL ---------- */

.gestacion-item,
.historial-item {
    padding: 15px;
    margin-bottom: 15px;
    background: #ffffff;
    border-radius: 10px;
    border-left: 5px solid #7cb068;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.07);
}

/* Espacio entre párrafos */
.gestacion-item p,
.historial-item p {
    margin: 5px 0;
}

/* Negritas verdes */
.gestacion-item strong,
.historial-item strong {
    color: #2d5016;
}

/* Línea divisoria suave */
.gestacion-item hr,
.historial-item hr {
    margin-top: 12px;
    border: 0;
    border-top: 1px solid #c7d8c3;
}

/* ---------- LISTAS (Vacunas / Medicamentos) ---------- */

.historial-item ul {
    margin: 8px 0 5px 18px;
    padding: 0;
}

.historial-item li {
    margin-bottom: 4px;
}

/* ---------- COLORES POR ESTADO (Opcional, pero muy bonito 😎) ---------- */

/* Cuando está en Gestación */
.gestacion-item[data-estado="Gestación"] {
    border-left-color: #4caf50;
}

/* Cuando está Vacía */
.gestacion-item[data-estado="Vacía"] {
    border-left-color: #ff7043;
}

/* Sanitario — estado crítico */
.historial-item[data-estado="Enfermo"] {
    border-left-color: #e53935;
}

/* Sanitario — estado normal */
.historial-item[data-estado="Sano"] {
    border-left-color: #43a047;
}

/* Contenedor de producción de leche */
.produccion-container {
    background: linear-gradient(135deg, #fefbf0 0%, #f9f5e6 100%);
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #d9c88a;
    margin-top: 25px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Título */
.produccion-container h3 {
    color: #a37f00;
    margin-bottom: 15px;
    text-align: center;
}

/* Cada registro */
.produccion-item {
    background-color: #fff8e1;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid #e5d3a2;
}

/* Fechas y litros */
.produccion-item p {
    margin: 5px 0;
    color: #5a4a00;
}

/* Línea separadora */
.produccion-item hr {
    border: 0.5px solid #e5d3a2;
    margin-top: 10px;
}
</style>
