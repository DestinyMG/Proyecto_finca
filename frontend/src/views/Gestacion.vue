<template>
    <BaseAdmin>
        <div>

            <h2>Gestión de Gestación</h2>

            <!-- BUSCAR ANIMAL -->
            <div class="busqueda-animal">
                <label>Código del Animal</label>
                <div class="input-boton">
                    <input v-model="codigoAnimal" placeholder="Ej: A001" />
                    <button @click="buscarAnimal">Buscar</button>
                </div>
            </div>


            <!-- ANIMAL ENCONTRADO -->
            <div v-if="animalSeleccionado">
                <h3>Animal encontrado</h3>
                <p><strong>Código:</strong> {{ animalSeleccionado.codigoAnimal }}</p>
                <p><strong>Tipo:</strong> {{ animalSeleccionado.tipo }}</p>
                <p><strong>Sexo:</strong> {{ animalSeleccionado.sexo }}</p>
            </div>

            <!-- FORMULARIO DE GESTACIÓN -->
            <div v-if="animalSeleccionado">
                <form @submit.prevent="guardarGestacion">

                    <!-- Estado -->
                    <div>
                        <label>Estado</label>
                        <select v-model="formData.estado">
                            <option value="Gestación">Gestación</option>
                            <option value="Vacía">Vacía</option>
                        </select>
                    </div>

                    <!-- Fecha de palpación -->
                    <div>
                        <label>Fecha de Palpación</label>
                        <input type="date" v-model="formData.fecha_palpacion" required />
                    </div>

                    <!-- Tiempo de gestación SOLO SI ESTÁ EN GESTACIÓN -->
                    <div v-if="formData.estado === 'Gestación'">
                        <label>Tiempo de Gestación (días)</label>
                        <input type="number" v-model="formData.tiempo_gestacion" min="1" />
                    </div>

                    <!-- Próxima palpación -->
                    <div>
                        <label>Próxima Palpación</label>
                        <input type="date" v-model="formData.proxima_palpacion" />
                    </div>

                    <!-- Observaciones -->
                    <div>
                        <label>Observaciones</label>
                        <textarea v-model="formData.observaciones"></textarea>
                    </div>

                    <button type="submit">Guardar Registro</button>
                </form>
            </div>

            <!-- HISTORIAL DE GESTACIÓN -->
            <div v-if="historial.length">
                <h3>Historial de Gestación del Animal</h3>
                <div v-for="registro in historial" :key="registro.id" class="historial-item">
                    <p><strong>Estado:</strong> {{ registro.estado }}</p>
                    <p><strong>Fecha de Palpación:</strong> {{ registro.fecha_palpacion }}</p>
                    <p v-if="registro.tiempo_gestacion"><strong>Tiempo de Gestación:</strong> {{
                        registro.tiempo_gestacion }} días</p>
                    <p v-if="registro.proxima_palpacion"><strong>Próxima Palpación:</strong> {{
                        registro.proxima_palpacion }}</p>
                    <p v-if="registro.observaciones"><strong>Observaciones:</strong> {{ registro.observaciones }}</p>
                    <button @click="eliminarRegistro(registro.id)">Eliminar</button>
                    <hr />
                </div>
            </div>

        </div>
    </BaseAdmin>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import BaseAdmin from '../components/BaseAdmin.vue';

// ENDPOINTS
const API_ANIMALES = 'https://proyecto-finca-yxcf.onrender.com/animales/';
const API_GESTACION = 'https://proyecto-finca-yxcf.onrender.com/api4/gestacion/';

const codigoAnimal = ref('');
const animalSeleccionado = ref(null);
const historial = ref([]);

// FORM DATA COMPLETO (incluye estado)
const formData = ref({
    animal: null,
    estado: "Gestación",
    fecha_palpacion: new Date().toISOString().slice(0, 10),
    tiempo_gestacion: '',
    proxima_palpacion: '',
    observaciones: ''
});

// Limpiar tiempo_gestacion si se selecciona "Vacía"
watch(() => formData.value.estado, (nuevo) => {
    if (nuevo === "Vacía") {
        formData.value.tiempo_gestacion = null;
    }
});

// Buscar animal por código y cargar historial
const buscarAnimal = async () => {
    try {
        const res = await axios.get(`${API_ANIMALES}?codigoAnimal=${codigoAnimal.value}`);

        if (!res.data.length) {
            alert("Animal no encontrado.");
            animalSeleccionado.value = null;
            formData.value.animal = null;
            historial.value = [];
            return;
        }

        const animal = res.data[0];

        // Solo hembras
        if (animal.sexo !== 'Hembra') {
            alert("Solo se permiten hembras para el módulo de gestación.");
            animalSeleccionado.value = null;
            formData.value.animal = null;
            historial.value = [];
            return;
        }

        animalSeleccionado.value = animal;
        formData.value.animal = animal.id;

        // ✅ Cargar historial de gestación
        const his = await axios.get(`${API_GESTACION}?animal=${animal.id}`);
        historial.value = his.data;

    } catch (error) {
        console.error(error);
        alert("Error al buscar animal");
    }
};

// Guardar registro de gestación y actualizar historial
const guardarGestacion = async () => {
    try {
        await axios.post(API_GESTACION, formData.value);

        alert("Registro de gestación guardado correctamente.");

        // Reset form
        formData.value = {
            animal: animalSeleccionado.value.id,
            estado: "Gestación",
            fecha_palpacion: new Date().toISOString().slice(0, 10),
            tiempo_gestacion: '',
            proxima_palpacion: '',
            observaciones: ''
        };

        // Recargar historial
        const his = await axios.get(`${API_GESTACION}?animal=${animalSeleccionado.value.id}`);
        historial.value = his.data;

    } catch (error) {
        console.error(error);
        alert("Error al guardar gestación");
    }
};

// Eliminar registro de gestación
const eliminarRegistro = async (id) => {
    if (!confirm("¿Desea eliminar este registro?")) return;

    try {
        await axios.delete(`${API_GESTACION}${id}/`);
        alert("Registro eliminado.");

        // Actualizar historial
        historial.value = historial.value.filter(r => r.id !== id);

    } catch (error) {
        console.error(error);
        alert("Error al eliminar el registro");
    }
};
</script>
<style scoped>
/* Contenedor principal */
div {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Título principal */
h2 {
    color: #2d5016;
    text-align: center;
    margin-bottom: 30px;
    font-size: 2.2rem;
    font-weight: 600;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    border-bottom: 3px solid #4a7c3f;
    padding-bottom: 10px;
}

/* Sección de búsqueda */
div:has(> label[for]) {
    background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 30px;
    border: 2px solid #4a7c3f;
    box-shadow: 0 4px 15px rgba(74, 124, 63, 0.1);
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2d5016;
    font-size: 1.1rem;
}

input[type="text"],
input[type="date"],
input[type="number"],
select,
textarea {
    width: 100%;
    max-width: 400px;
    padding: 12px 15px;
    border: 2px solid #7cb068;
    border-radius: 8px;
    font-size: 1rem;
    background-color: #ffffff;
    transition: all 0.3s ease;
    margin-bottom: 15px;
}

input:focus,
select:focus,
textarea:focus {
    outline: none;
    border-color: #2d5016;
    box-shadow: 0 0 0 3px rgba(45, 80, 22, 0.1);
    background-color: #f8fff8;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

/* Botones */
button {
    background: linear-gradient(135deg, #4a7c3f 0%, #2d5016 100%);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 10px;
    box-shadow: 0 2px 8px rgba(45, 80, 22, 0.3);
}

button:hover {
    background: linear-gradient(135deg, #5a8c4f 0%, #3d6026 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(45, 80, 22, 0.4);
}

button:active {
    transform: translateY(0);
}

/* Información del animal encontrado */
div:has(> h3) {
    background: linear-gradient(135deg, #e8f4e8 0%, #d4e8d4 100%);
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    border-left: 5px solid #4a7c3f;
}

h3 {
    color: #2d5016;
    margin-bottom: 15px;
    font-size: 1.5rem;
    border-bottom: 2px solid #7cb068;
    padding-bottom: 8px;
}

/* Formulario de gestación */
form {
    background: linear-gradient(135deg, #f0f8f0 0%, #e0f0e0 100%);
    padding: 30px;
    border-radius: 12px;
    margin: 25px 0;
    border: 2px dashed #7cb068;
}

form>div {
    margin-bottom: 20px;
    background: transparent;
    padding: 0;
    border: none;
    box-shadow: none;
}

/* Historial de gestación */
.historial-item {
    background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
    padding: 20px;
    margin: 15px 0;
    border-radius: 10px;
    border-left: 4px solid #4a7c3f;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.historial-item:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.historial-item p {
    margin: 8px 0;
    color: #333;
    line-height: 1.5;
}

.historial-item strong {
    color: #2d5016;
    font-weight: 600;
}

/* Botón eliminar en historial */
.historial-item button {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
    margin-top: 15px;
    padding: 8px 16px;
    font-size: 0.9rem;
}

.historial-item button:hover {
    background: linear-gradient(135deg, #e04b59 0%, #d92538 100%);
}

/* Línea divisoria */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #7cb068 50%, transparent 100%);
    margin: 20px 0;
}

/* Estados específicos */
select option[value="Gestación"] {
    background-color: #d4edda;
    color: #155724;
}

select option[value="Vacía"] {
    background-color: #f8d7da;
    color: #721c24;
}

/* Responsive */
@media (max-width: 768px) {
    div {
        padding: 15px;
    }

    h2 {
        font-size: 1.8rem;
    }

    form {
        padding: 20px;
    }

    input[type="text"],
    input[type="date"],
    input[type="number"],
    select,
    textarea {
        max-width: 100%;
    }

    .historial-item {
        padding: 15px;
    }
}

/* Animaciones suaves */
.historial-item,
form,
div:has(> h3) {
    animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Efectos de focus mejorados */
input:focus::placeholder,
textarea:focus::placeholder {
    color: transparent;
}

/* Estilo para campos requeridos */
input:required,
select:required {
    border-left: 4px solid #4a7c3f;
}

/* Mensajes de alerta implícitos */
.alert-message {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 12px;
    border-radius: 6px;
    margin: 10px 0;
    font-weight: 500;
}

/* Mejoras visuales para el formulario */
form>div:last-of-type {
    margin-bottom: 0;
    padding-top: 15px;
    border-top: 1px solid #7cb068;
}

/* Estilo para el botón de búsqueda específico */
div:has(> button)>button {
    margin-top: 0;
    margin-left: 10px;
}

/* Contenedor de búsqueda flex */
div:has(> label[for]) {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

div:has(> label[for])>div {
    display: flex;
    gap: 10px;
    align-items: center;
    width: 100%;
    flex-wrap: wrap;
}

.busqueda-animal {
    background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 30px;
    border: 2px solid #4a7c3f;
    box-shadow: 0 4px 15px rgba(74, 124, 63, 0.1);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.busqueda-animal label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2d5016;
    font-size: 1.1rem;
}

.input-boton {
    display: flex;
    gap: 10px;
    width: 100%;
    flex-wrap: wrap;
}

.input-boton input {
    flex: 1;
    min-width: 200px;
    padding: 12px 15px;
    border: 2px solid #7cb068;
    border-radius: 8px;
    font-size: 1rem;
    background-color: #ffffff;
}

.input-boton button {
    padding: 12px 25px;
    border-radius: 8px;
    font-weight: 600;
}
</style>