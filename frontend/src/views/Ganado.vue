<template>
    <BaseAdmin>
        <template #default>
            <div class="ganado-container">
                <div class="ganado-header">
                    <h2>Gestión de Ganado</h2>
                    <button class="toggle-form-btn" @click="toggleForm">
                        {{ isFormVisible ? 'Ocultar Formulario' : 'Añadir Nuevo Animal' }}
                    </button>
                </div>

                <!-- FORMULARIO -->
                <Transition name="slide-fade">
                    <div v-if="isFormVisible" class="form-wrapper">
                        <div class="form-card">
                            <h3>{{ isEditing ? 'Editar Animal' : 'Registro de Ganado' }}</h3>
                            <p>Añade o modifica un animal en el inventario.</p>

                            <form @submit.prevent="guardarAnimal">

                                <!-- DATOS GENERALES -->
                                <div class="form-grid">
                                    <div class="form-group">
                                        <label for="codigoAnimal">Código Animal (ID)</label>
                                        <input id="codigoAnimal" type="text" v-model="formData.codigoAnimal"
                                            maxlength="10" placeholder="Ej: F-00123" :disabled="isEditing" required />
                                    </div>

                                    <div class="form-group">
                                        <label for="chip">Chip (Opcional)</label>
                                        <input id="chip" type="text" v-model="formData.chip"
                                            placeholder="Ej: 982123456789" />
                                    </div>
                                    <div class="form-group">
                                        <label for="chip2">Chip 2 (Opcional)</label>
                                        <input id="chip2" type="text" v-model="formData.chip2"
                                            placeholder="Ej: 982123456789" />
                                    </div>

                                    <div class="form-group">
                                        <label for="chip3">Chip 3 (Opcional)</label>
                                        <input id="chip3" type="text" v-model="formData.chip3"
                                            placeholder="Ej: 982123456789" />
                                    </div>


                                    <div class="form-group">
                                        <label for="tipo">Tipo</label>
                                        <select id="tipo" v-model="formData.tipo" required>
                                            <option value="" disabled>Seleccione un tipo</option>
                                            <option value="Bufalo">Búfalo</option>
                                            <option value="Vacuno">Vacuno</option>
                                        </select>
                                    </div>

                                    <div class="form-group">
                                        <label for="sexo">Sexo</label>
                                        <select id="sexo" v-model="formData.sexo" :disabled="isEditing" required>
                                            <option value="" disabled>Seleccione un sexo</option>
                                            <option value="Macho">Macho</option>
                                            <option value="Hembra">Hembra</option>
                                        </select>
                                    </div>

                                    <div class="form-group full-width">
                                        <label for="procedencia">Procedencia</label>
                                        <input id="procedencia" type="text" v-model="formData.procedencia"
                                            placeholder="Ej: Finca El Rosario, Compra local, etc." required />
                                    </div>

                                    <div class="form-group">
                                        <label for="origen">Origen</label>
                                        <select id="origen" v-model="formData.origen">
                                            <option value="" disabled>Seleccione origen</option>
                                            <option value="Compra">Compra</option>
                                            <option value="Nacimiento">Nacimiento</option>
                                        </select>
                                    </div>

                                    <div class="form-group" v-if="formData.sexo === 'Hembra'">
                                        <label>
                                            <input type="checkbox" v-model="formData.embarazada" /> Embarazada
                                        </label>
                                    </div>
                                </div>

                                <!-- DATOS CONDICIONALES -->
                                <!-- DATOS CONDICIONALES -->
                                <div class="form-grid">

                                    <!-- Código Madre y Padre (opcional) -->
                                    <template v-if="formData.origen === 'Nacimiento'">
                                        <div class="form-group">
                                            <label for="codigo_madre">Código Madre (Opcional)</label>
                                            <input id="codigo_madre" type="text" v-model="formData.codigo_madre" />
                                        </div>

                                        <div class="form-group">
                                            <label for="codigo_padre">Código Padre (Opcional)</label>
                                            <input id="codigo_padre" type="text" v-model="formData.codigo_padre" />
                                        </div>

                                        <div class="form-group">
                                            <label for="fecha_nacimiento">Fecha de Nacimiento</label>
                                            <input type="date" id="fecha_nacimiento"
                                                v-model="formData.fecha_nacimiento" />
                                        </div>
                                    </template>

                                    <!-- Fechas y datos para hembras embarazadas -->
                                    <template v-if="formData.sexo === 'Hembra' && formData.embarazada">
                                        <div class="form-group">
                                            <label for="fecha_palpacion">Fecha de Palpación</label>
                                            <input type="date" id="fecha_palpacion"
                                                v-model="formData.fecha_palpacion" />
                                        </div>

                                        <div class="form-group">
                                            <label for="fecha_parto">Fecha de Parto</label>
                                            <input type="date" id="fecha_parto" v-model="formData.fecha_parto" />
                                        </div>
                                    </template>

                                    <!-- Fecha de compra (opcional) -->
                                    <div class="form-group" v-if="formData.origen === 'Compra'">
                                        <label for="fecha_compra">Fecha de Compra (Opcional)</label>
                                        <input type="date" id="fecha_compra" v-model="formData.fecha_compra" />
                                    </div>

                                    <!-- Producción de leche para hembras -->
                                    <div class="form-group" v-if="formData.sexo === 'Hembra'">
                                        <label for="produccionLeche">Producción de Leche (L/día)</label>
                                        <input id="produccionLeche" type="number" step="0.1"
                                            v-model.number="formData.produccionLeche" />
                                    </div>

                                </div>

                                <!-- BOTONES -->
                                <div class="form-actions">
                                    <button type="button" v-if="isEditing" @click="cancelarEdicion" class="cancel-btn">
                                        Cancelar
                                    </button>
                                    <button type="submit" class="submit-btn">
                                        {{ isEditing ? 'Guardar Cambios' : 'Registrar Animal' }}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </Transition>

                <!-- LISTADO DE ANIMALES -->
                <div class="listado-animales">
                    <h3>Listado de Animales</h3>

                    <div v-for="(grupo, index) in gruposAnimales" :key="index">
                        <h4>{{ grupo.titulo }} ({{ grupo.lista.length }})</h4>
                        <div v-if="grupo.lista.length === 0" class="empty-state">No hay registros.</div>
                        <div v-else class="table-wrapper">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Código Animal</th>
                                        <th>Chip</th>
                                        <th>Procedencia</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="animal in grupo.lista" :key="animal.id">
                                        <td>
                                            <router-link :to="{ name: 'detalle-animal', params: { id: animal.id } }">
                                                {{ animal.codigoAnimal }}
                                            </router-link>
                                        </td>


                                        <td>{{ animal.chip || 'N/A' }}</td>
                                        <td>{{ animal.procedencia }}</td>
                                        <td class="action-cell">
                                            <button @click="iniciarEdicion(animal)" class="edit-btn">✏️</button>
                                            <button @click="eliminarAnimal(animal.id)" class="delete-btn">🗑️</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                </div>
            </div>
        </template>
    </BaseAdmin>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import BaseAdmin from '../components/BaseAdmin.vue';

const API_URL = 'https://proyecto-finca-yxcf.onrender.com/api1/animales/';

const isFormVisible = ref(false);
const isEditing = ref(false);

const initialFormData = {
    codigoAnimal: '',
    chip: '',
    chip2: '',
    chip3: '',
    tipo: '',
    sexo: '',
    procedencia: '',
    origen: '',
    embarazada: false,
    fecha_palpacion: null,
    fecha_parto: null,
    fecha_compra: null,
    codigo_madre: null,
    codigo_padre: null,
    fecha_nacimiento: null,
    produccionLeche: 0,
};


const formData = ref({ ...initialFormData });
const animales = ref([]);

const cargarAnimales = async () => {
    try {
        const res = await axios.get(API_URL);
        animales.value = res.data;
    } catch (error) {
        console.error(error);
        alert('No se pudieron cargar los animales');
    }
};

onMounted(() => {
    cargarAnimales();
});

const bufalosMachos = computed(() => animales.value.filter(a => a.tipo === 'Bufalo' && a.sexo === 'Macho'));
const bufalosHembras = computed(() => animales.value.filter(a => a.tipo === 'Bufalo' && a.sexo === 'Hembra'));
const vacunosMachos = computed(() => animales.value.filter(a => a.tipo === 'Vacuno' && a.sexo === 'Macho'));
const vacunosHembras = computed(() => animales.value.filter(a => a.tipo === 'Vacuno' && a.sexo === 'Hembra'));

const gruposAnimales = computed(() => [
    { titulo: 'Búfalos Machos', lista: bufalosMachos.value },
    { titulo: 'Búfalas Hembras', lista: bufalosHembras.value },
    { titulo: 'Vacunos Machos', lista: vacunosMachos.value },
    { titulo: 'Vacunos Hembras', lista: vacunosHembras.value },
]);

const toggleForm = () => {
    if (isFormVisible.value && isEditing.value) cancelarEdicion();
    isFormVisible.value = !isFormVisible.value;
};

const resetForm = () => {
    formData.value = { ...initialFormData };
    isEditing.value = false;
};

const cancelarEdicion = () => {
    resetForm();
    isFormVisible.value = false;
};

const prepararPayload = data => ({
    codigoAnimal: data.codigoAnimal,
    chip: data.chip || null,
    chip2: data.chip2 || null,
    chip3: data.chip3 || null,
    tipo: data.tipo,
    sexo: data.sexo,
    procedencia: data.procedencia,
    origen: data.origen || 'Nacimiento',
    embarazada: data.embarazada || false,
    fecha_palpacion: data.fecha_palpacion || null,
    fecha_parto: data.fecha_parto || null,
    fecha_compra: data.fecha_compra || null,
    fecha_nacimiento: data.fecha_nacimiento || null,

    codigo_madre: data.codigo_madre || null,
    codigo_padre: data.codigo_padre || null,
    produccionLeche: data.produccionLeche || 0,
});


const guardarAnimal = async () => {
    const payload = prepararPayload(formData.value);
    try {
        if (isEditing.value) {
            await axios.put(`${API_URL}${formData.value.id}/`, payload);
            alert('Animal actualizado con éxito!');
        } else {
            await axios.post(API_URL, payload);
            alert('Animal registrado con éxito!');
        }
        await cargarAnimales();
        resetForm();
        isFormVisible.value = false;
    } catch (error) {
        console.error(error.response?.data || error);
        alert('Error al guardar el animal');
    }
};

const iniciarEdicion = animal => {
    formData.value = { ...animal };
    isEditing.value = true;
    isFormVisible.value = true;
};

const eliminarAnimal = async id => {
    if (confirm(`¿Deseas eliminar el animal con ID ${id}?`)) {
        try {
            await axios.delete(`${API_URL}${id}/`);
            alert('Animal eliminado.');
            await cargarAnimales();
            if (isEditing.value && formData.value.id === id) cancelarEdicion();
        } catch (error) {
            console.error(error);
            alert('Error al eliminar el animal');
        }
    }
};
</script>



<style scoped>
/* --- Estilos Adicionales para los Botones de Acción --- */

/* Celda que contiene los botones */
.action-cell {
    width: 120px;
    /* Ancho fijo para las acciones */
    text-align: center;
}

.edit-btn,
.delete-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    margin: 0 0.25rem;
    font-size: 1.1rem;
    transition: transform 0.1s;
    border-radius: 4px;
}

.edit-btn {
    color: #007bff;
    /* Azul para editar */
}

.delete-btn {
    color: #dc3545;
    /* Rojo para eliminar */
}

.edit-btn:hover,
.delete-btn:hover {
    transform: scale(1.1);
    background-color: #f0f0f0;
}

/* Botón de Cancelar en el formulario de edición */
.cancel-btn {
    background-color: #6c757d;
    /* Gris para cancelar */
    color: white;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.85rem 1.75rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
    margin-right: 1rem;
}

.cancel-btn:hover {
    background-color: #5a6268;
}

/* Reaplicamos los estilos de la respuesta anterior para que el código sea completo */
.ganado-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #eee;
}

.ganado-header h2 {
    margin: 0;
    color: #2a4a3a;
}

.toggle-form-btn {
    background-color: #28a745;
    color: white;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s, transform 0.2s;
}

.toggle-form-btn:hover {
    background-color: #218838;
    transform: translateY(-2px);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.3s ease-out;
    max-height: 1000px;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-20px);
    max-height: 0px;
}

.form-wrapper {
    margin-bottom: 2.5rem;
}

.form-card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    max-width: 900px;
    margin: 0 auto;
}

.form-card h3 {
    font-size: 1.75rem;
    font-weight: 600;
    color: #2a4a3a;
    margin-top: 0;
    margin-bottom: 0.5rem;
}

.form-card p {
    font-size: 1rem;
    color: #666;
    margin-bottom: 2rem;
    border-bottom: 1px solid #eee;
    padding-bottom: 1rem;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.form-group input[type="text"]:disabled,
.form-group select:disabled {
    background-color: #f0f0f0;
    /* Color para campos deshabilitados */
    cursor: not-allowed;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group input[type="date"],
.form-group select {
    width: 100%;
    padding: 0.85rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: #28a745;
    box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.2);
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.female-options-section {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 2px dashed #e0e0e0;
}

.female-options-section h4 {
    font-size: 1.25rem;
    color: #28a745;
    margin-top: 0;
    margin-bottom: 1.5rem;
}

.form-actions {
    margin-top: 2rem;
    text-align: right;
}

.submit-btn {
    background-color: #28a745;
    color: white;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.85rem 1.75rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.submit-btn:hover {
    background-color: #218838;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.listado-animales {
    background-color: #fff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.listado-animales h3 {
    font-size: 1.75rem;
    color: #2a4a3a;
    margin-top: 0;
    border-bottom: 1px solid #eee;
    padding-bottom: 1rem;
}

.listado-animales h4 {
    font-size: 1.3rem;
    color: #333;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.female-title {
    color: #d9534f;
}

.empty-state {
    background-color: #f9f9f9;
    padding: 1rem;
    border-radius: 6px;
    text-align: center;
    color: #777;
    border: 1px dashed #ddd;
}

.table-wrapper {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
}

thead tr {
    background-color: #f4f7f6;
}

th,
td {
    padding: 0.85rem 1rem;
    border: 1px solid #e0e0e0;
    text-align: left;
    font-size: 0.95rem;
    vertical-align: middle;
}

th {
    font-weight: 600;
    color: #333;
}

tbody tr:nth-child(even) {
    background-color: #fcfcfc;
}

tbody tr:hover {
    background-color: #f0f4f8;
}

@media (max-width: 768px) {
    .form-grid {
        grid-template-columns: 1fr;
    }

    .form-card {
        padding: 1.5rem;
    }

    .ganado-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
}
</style>