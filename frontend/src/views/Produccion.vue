<template>
    <BaseAdmin>
        <div class="produccion-leche-container">
            <h2>Registro de Producción de Leche</h2>

            <!-- BUSCADOR DE ANIMAL -->
            <div class="form-card">
                <div class="form-group">
                    <label>Código del Animal</label>
                    <div class="animal-search">
                        <input v-model="codigoAnimal" placeholder="Ej: A001" />
                        <button type="button" @click="buscarAnimal">Buscar</button>
                    </div>

                    <div v-if="animalSeleccionado" class="animal-info">
                        <p><strong>Tipo:</strong> {{ animalSeleccionado.tipo }}</p>
                        <p><strong>Sexo:</strong> {{ animalSeleccionado.sexo }}</p>
                    </div>
                </div>
            </div>

            <!-- FORMULARIO DE REGISTRO -->
            <div v-if="animalSeleccionado" class="form-card">
                <form @submit.prevent="guardarRegistro">
                    <div class="form-group">
                        <label>Fecha</label>
                        <input type="date" v-model="formData.fecha" required />
                    </div>

                    <div class="form-group">
                        <label>Litros de Leche</label>
                        <input type="number" v-model="formData.litros" step="0.1" required />
                    </div>

                    <div class="form-actions">
                        <button type="submit">{{ editing ? 'Actualizar Registro' : 'Guardar Registro' }}</button>
                        <button v-if="editing" type="button" @click="cancelarEdicion">Cancelar</button>
                    </div>
                </form>
            </div>

            <!-- HISTORIAL DE PRODUCCIÓN -->
            <div v-if="historial.length" class="historial-card">
                <h3>Historial de Producción de Leche</h3>
                <div v-for="r in historial" :key="r.id" class="registro-item">
                    <h4>📅 {{ r.fecha }}</h4>
                    <p><strong>Litros:</strong> {{ r.litros }}</p>
                    <div class="registro-actions">
                        <button @click="editarRegistro(r)">Editar</button>
                        <button @click="eliminarRegistro(r.id)">Eliminar</button>
                    </div>
                    <hr />
                </div>
            </div>
        </div>
    </BaseAdmin>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import BaseAdmin from '../components/BaseAdmin.vue';

// ENDPOINTS
const API_ANIMALES = 'http://localhost:8000/api1/animales/';
const API_PRODUCCION = 'http://localhost:8000/api3/produccion/';

// VARIABLES
const codigoAnimal = ref('');
const animalSeleccionado = ref(null);
const historial = ref([]);

const editing = ref(false);
const editId = ref(null);

const formData = ref({
    animal: null,
    fecha: new Date().toISOString().substring(0, 10),
    litros: 0,
});

// FUNCIONES
const buscarAnimal = async () => {
    if (!codigoAnimal.value.trim()) return alert('Ingrese un código de animal.');

    try {
        const res = await axios.get(`${API_ANIMALES}?codigoAnimal=${codigoAnimal.value.trim()}`);
        if (!res.data.length) {
            alert('Animal no encontrado.');
            animalSeleccionado.value = null;
            formData.value.animal = null;
            historial.value = [];
            return;
        }

        const animal = res.data[0];

        if (animal.sexo !== 'Hembra') {
            alert('Solo se puede registrar leche para hembras.');
            animalSeleccionado.value = null;
            formData.value.animal = null;
            historial.value = [];
            return;
        }

        animalSeleccionado.value = animal;
        formData.value.animal = animal.id;

        // Cargar historial de producción
        const his = await axios.get(`${API_PRODUCCION}?animal=${animal.id}`);
        historial.value = his.data;

    } catch (err) {
        console.error('Error buscando animal:', err);
        alert('Error al buscar el animal.');
    }
};

const guardarRegistro = async () => {
    if (!formData.value.animal) return alert('Debe seleccionar un animal.');

    try {
        if (editing.value) {
            await axios.put(`${API_PRODUCCION}${editId.value}/`, formData.value);
            editing.value = false;
            editId.value = null;
        } else {
            await axios.post(API_PRODUCCION, formData.value);
        }

        alert('Registro guardado correctamente.');
        buscarAnimal();
        resetForm();

    } catch (err) {
        console.error('Error guardando registro:', err.response?.data || err);
        alert('Error al guardar el registro.');
    }
};

const editarRegistro = (registro) => {
    formData.value = { ...registro };
    editing.value = true;
    editId.value = registro.id;
};

const eliminarRegistro = async (id) => {
    if (!confirm('¿Está seguro de eliminar este registro?')) return;
    try {
        await axios.delete(`${API_PRODUCCION}${id}/`);
        alert('Registro eliminado.');
        buscarAnimal();
    } catch (err) {
        console.error('Error eliminando registro:', err.response?.data || err);
        alert('Error al eliminar el registro.');
    }
};

const cancelarEdicion = () => {
    editing.value = false;
    editId.value = null;
    resetForm();
};

const resetForm = () => {
    formData.value = {
        animal: animalSeleccionado.value?.id || null,
        fecha: new Date().toISOString().substring(0, 10),
        litros: 0,
    };
};
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