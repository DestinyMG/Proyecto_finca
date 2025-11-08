<template>
    <BaseAdmin>
        <div class="registro-sanitario-container">
            <h2>Registro Sanitario del Ganado</h2>

            <!-- FORMULARIO -->
            <div class="form-card">
                <form @submit.prevent="guardarRegistro">

                    <!-- SECCIÓN ANIMAL -->
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

                    <!-- FECHAS -->
                    <div class="form-row">
                        <div class="form-group">
                            <label>Fecha del Registro</label>
                            <input type="date" v-model="formData.fecha_registro" required />
                        </div>

                        <div class="form-group">
                            <label>Próxima Revisión</label>
                            <input type="date" v-model="formData.proxima_revision" />
                        </div>
                    </div>

                    <!-- ESTADO -->
                    <div class="form-group">
                        <label>Estado</label>
                        <select v-model="formData.estado">
                            <option value="Sano">Sano</option>
                            <option value="Enfermo">Enfermo</option>
                            <option value="Recuperado">Recuperado</option>
                        </select>
                    </div>

                    <!-- ENFERMEDAD -->
                    <div v-if="formData.estado === 'Enfermo'" class="form-group">
                        <label>Enfermedad</label>
                        <select v-model="formData.enfermedad">
                            <option value="">Seleccione una enfermedad</option>
                            <option v-for="e in enfermedades" :key="e.id" :value="e.id">{{ e.nombre }}</option>
                        </select>
                    </div>

                    <!-- TRATAMIENTO -->
                    <div v-if="formData.estado === 'Enfermo'" class="form-group">
                        <label>Tratamiento</label>
                        <textarea v-model="formData.tratamiento" rows="2"></textarea>
                    </div>

                    <!-- MEDICAMENTOS -->
                    <div v-if="formData.estado === 'Enfermo'" class="form-group">
                        <label>Medicamentos</label>
                        <div class="checkbox-list">
                            <label v-for="m in medicamentos" :key="m.id">
                                <input type="checkbox" :value="m.id" v-model="formData.medicamentos" />
                                {{ m.nombre }}
                            </label>
                        </div>
                    </div>

                    <!-- VACUNAS -->
                    <div class="form-group">
                        <label>Vacunas Aplicadas</label>
                        <div class="checkbox-list">
                            <label v-for="v in vacunas" :key="v.id">
                                <input type="checkbox" :value="v.id" v-model="formData.vacunas" />
                                {{ v.nombre }}
                            </label>
                        </div>
                    </div>

                    <!-- OBSERVACIONES -->
                    <div class="form-group">
                        <label>Observaciones</label>
                        <textarea v-model="formData.observaciones" rows="3"></textarea>
                    </div>

                    <!-- BOTONES -->
                    <div class="form-actions">
                        <button type="submit" class="submit-btn">{{ editing ? 'Actualizar Registro' : 'Guardar Registro'
                        }}</button>
                        <button v-if="editing" type="button" @click="cancelarEdicion"
                            class="cancel-btn">Cancelar</button>
                    </div>

                </form>
            </div>

            <!-- ==================== -->
            <!-- 🟦 HISTORIAL COMPLETO -->
            <!-- ==================== -->
            <div v-if="historial.length" class="historial-card">
                <h3>Historial Sanitario del Animal</h3>

                <div v-for="r in historial" :key="r.id" class="registro-item">
                    <h4>📅 {{ r.fecha_registro }}</h4>

                    <p><strong>Estado:</strong> {{ r.estado }}</p>

                    <div v-if="r.enfermedad_detalle">
                        <strong>Enfermedad:</strong> {{ r.enfermedad_detalle.nombre }}
                    </div>

                    <div v-if="r.tratamiento">
                        <strong>Tratamiento:</strong> {{ r.tratamiento }}
                    </div>

                    <div v-if="r.medicamentos_detalle && r.medicamentos_detalle.length">
                        <strong>Medicamentos:</strong>
                        <ul>
                            <li v-for="m in r.medicamentos_detalle" :key="m.id">{{ m.nombre }}</li>
                        </ul>
                    </div>

                    <div v-if="r.vacunas_detalle && r.vacunas_detalle.length">
                        <strong>Vacunas:</strong>
                        <ul>
                            <li v-for="v in r.vacunas_detalle" :key="v.id">{{ v.nombre }}</li>
                        </ul>
                    </div>

                    <div v-if="r.observaciones">
                        <strong>Observaciones:</strong>
                        <p>{{ r.observaciones }}</p>
                    </div>

                    <div v-if="r.proxima_revision">
                        <strong>Próxima Revisión:</strong> {{ r.proxima_revision }}
                    </div>

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
import { ref, onMounted } from 'vue';
import axios from 'axios';
import BaseAdmin from '../components/BaseAdmin.vue';

// ENDPOINTS
const API_ANIMALES = 'https://proyecto-finca-yxcf.onrender.com/api1/animales/';
const API_ENFERMEDADES = 'https://proyecto-finca-yxcf.onrender.com/api2/enfermedades/';
const API_MEDICAMENTOS = 'https://proyecto-finca-yxcf.onrender.com/api2/medicamentos/';
const API_VACUNAS = 'https://proyecto-finca-yxcf.onrender.com/api2/vacunas/';
const API_REGISTROS = 'https://proyecto-finca-yxcf.onrender.com/api2/registros/';

// VARIABLES
const codigoAnimal = ref('');
const animalSeleccionado = ref(null);
const enfermedades = ref([]);
const medicamentos = ref([]);
const vacunas = ref([]);
const historial = ref([]);

const editing = ref(false);
const editId = ref(null);

const formData = ref({
    animal: null,
    fecha_registro: new Date().toISOString().substring(0, 10),
    estado: 'Sano',
    enfermedad: '',
    tratamiento: '',
    medicamentos: [],
    vacunas: [],
    observaciones: '',
    proxima_revision: '',
});

// CARGAR DATOS MAESTROS
onMounted(async () => {
    enfermedades.value = (await axios.get(API_ENFERMEDADES)).data;
    medicamentos.value = (await axios.get(API_MEDICAMENTOS)).data;
    vacunas.value = (await axios.get(API_VACUNAS)).data;
});

// BUSCAR ANIMAL
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

        animalSeleccionado.value = res.data[0];
        formData.value.animal = animalSeleccionado.value.id;

        // CARGAR HISTORIAL
        const his = await axios.get(`${API_REGISTROS}?animal=${animalSeleccionado.value.id}`);
        historial.value = his.data;

    } catch (err) {
        console.error('Error buscando animal:', err);
        alert('Error al buscar el animal.');
    }
};

// GUARDAR / ACTUALIZAR REGISTRO
const guardarRegistro = async () => {
    if (!formData.value.animal) return alert('Debe seleccionar un animal.');

    try {
        if (editing.value) {
            await axios.put(`${API_REGISTROS}${editId.value}/`, formData.value);
            editing.value = false;
            editId.value = null;
        } else {
            await axios.post(API_REGISTROS, formData.value);
        }

        alert('Registro sanitario guardado correctamente.');
        buscarAnimal();
        resetForm();

    } catch (err) {
        console.error('Error guardando registro:', err.response?.data || err);
        alert('Error al guardar el registro sanitario.');
    }
};

// EDITAR REGISTRO
const editarRegistro = (registro) => {
    formData.value = {
        ...registro,
        medicamentos: registro.medicamentos_detalle.map(m => m.id),
        vacunas: registro.vacunas_detalle.map(v => v.id),
    };
    editing.value = true;
    editId.value = registro.id;
};

// ELIMINAR REGISTRO
const eliminarRegistro = async (id) => {
    if (!confirm('¿Está seguro de eliminar este registro?')) return;

    try {
        await axios.delete(`${API_REGISTROS}${id}/`);
        alert('Registro eliminado.');
        buscarAnimal();
    } catch (err) {
        console.error('Error eliminando registro:', err.response?.data || err);
        alert('Error al eliminar el registro.');
    }
};

// CANCELAR EDICIÓN
const cancelarEdicion = () => {
    editing.value = false;
    editId.value = null;
    resetForm();
};

// REINICIAR FORMULARIO
const resetForm = () => {
    formData.value = {
        animal: animalSeleccionado.value?.id || null,
        fecha_registro: new Date().toISOString().substring(0, 10),
        estado: 'Sano',
        enfermedad: '',
        tratamiento: '',
        medicamentos: [],
        vacunas: [],
        observaciones: '',
        proxima_revision: '',
    };
};
</script>


<style scoped>
.registro-sanitario-container {
    padding: 2rem;
    max-width: 1000px;
    margin: 0 auto;
    min-height: calc(100vh - 70px);
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.registro-sanitario-container h2 {
    color: #2d5a3a;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
    font-family: 'Georgia', serif;
    text-shadow: 1px 1px 2px rgba(45, 90, 58, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
}

.registro-sanitario-container h2::before {
    content: "🏥";
    font-size: 1.8rem;
}

/* FORM CARD */
.form-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(45, 90, 58, 0.1);
    border: 1px solid #e8d9c5;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.form-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #2d5a3a, #3498db);
}

/* FORM GROUP */
.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #2d5a3a;
    font-weight: 600;
    font-size: 0.95rem;
}

/* ANIMAL SEARCH */
.animal-search {
    display: flex;
    gap: 0.75rem;
    align-items: center;
}

.animal-search input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: 2px solid #e8d9c5;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: #faf9f7;
}

.animal-search input:focus {
    outline: none;
    border-color: #3498db;
    background: white;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.animal-search button {
    background: linear-gradient(135deg, #2d5a3a, #3498db);
    color: white;
    border: none;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.animal-search button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
}

/* ANIMAL INFO */
.animal-info {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border: 1px solid #c8e6c9;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 0.75rem;
    animation: slideIn 0.3s ease;
}

.animal-info p {
    margin: 0.25rem 0;
    color: #2d5a3a;
    font-size: 0.9rem;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* FORM ROW */
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

/* INPUTS GENERALES */
.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #e8d9c5;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: #faf9f7;
    box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #3498db;
    background: white;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
    font-family: inherit;
}

/* CHECKBOX LIST */
.checkbox-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
    max-height: 200px;
    overflow-y: auto;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e8d9c5;
}

.checkbox-list label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    border-radius: 6px;
    transition: all 0.2s ease;
    cursor: pointer;
    margin: 0;
    font-weight: normal;
}

.checkbox-list label:hover {
    background: rgba(52, 152, 219, 0.1);
}

.checkbox-list input[type="checkbox"] {
    width: auto;
    margin: 0;
    transform: scale(1.2);
}

/* FORM ACTIONS */
.form-actions {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e8d9c5;
}

.submit-btn {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.submit-btn::before {
    content: "💾";
    font-size: 1.2rem;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(39, 174, 96, 0.4);
    background: linear-gradient(135deg, #2ecc71, #27ae60);
}

/* HISTORIAL CARD */
.historial-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(45, 90, 58, 0.1);
    border: 1px solid #e8d9c5;
    position: relative;
    overflow: hidden;
}

.historial-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #e67e22, #f39c12);
}

.historial-card h3 {
    color: #2d5a3a;
    margin-bottom: 1.5rem;
    font-size: 1.4rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.historial-card h3::before {
    content: "📋";
    font-size: 1.2rem;
}

/* REGISTRO ITEM */
.registro-item {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #e8d9c5;
    transition: all 0.3s ease;
    position: relative;
}

.registro-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(45, 90, 58, 0.1);
    background: white;
}

.registro-item h4 {
    color: #2d5a3a;
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 600;
}

.registro-item p {
    margin: 0.5rem 0;
    color: #555;
    line-height: 1.5;
}

.registro-item strong {
    color: #2d5a3a;
}

.registro-item ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.registro-item li {
    color: #555;
    margin: 0.25rem 0;
}

.registro-item hr {
    border: none;
    border-top: 1px solid #e8d9c5;
    margin: 1.5rem 0 0 0;
}

/* ESTADOS DE COLOR */
.registro-item[data-estado="Sano"] {
    border-left: 4px solid #27ae60;
}

.registro-item[data-estado="Enfermo"] {
    border-left: 4px solid #e74c3c;
}

.registro-item[data-estado="Recuperado"] {
    border-left: 4px solid #3498db;
}

/* RESPONSIVE DESIGN */
@media (max-width: 768px) {
    .registro-sanitario-container {
        padding: 1rem;
    }

    .registro-sanitario-container h2 {
        font-size: 1.6rem;
    }

    .form-card,
    .historial-card {
        padding: 1.5rem;
    }

    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .animal-search {
        flex-direction: column;
        align-items: stretch;
    }

    .animal-search button {
        margin-top: 0.5rem;
    }

    .checkbox-list {
        grid-template-columns: 1fr;
        max-height: 150px;
    }

    .form-actions {
        justify-content: stretch;
    }

    .submit-btn {
        width: 100%;
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .registro-sanitario-container {
        padding: 0.5rem;
    }

    .form-card,
    .historial-card {
        padding: 1rem;
    }

    .registro-sanitario-container h2::before,
    .historial-card h3::before,
    .submit-btn::before {
        display: none;
    }

    .checkbox-list {
        grid-template-columns: 1fr;
        max-height: 120px;
    }
}

/* SCROLLBAR PERSONALIZADO */
.checkbox-list::-webkit-scrollbar {
    width: 6px;
}

.checkbox-list::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.checkbox-list::-webkit-scrollbar-thumb {
    background: #3498db;
    border-radius: 3px;
}

.checkbox-list::-webkit-scrollbar-thumb:hover {
    background: #2980b9;
}

/* ANIMACIONES */
.registro-item {
    animation: fadeInUp 0.5s ease;
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

/* ESTADOS VISUALES PARA SELECT */
.form-group select option[value=""] {
    color: #6c757d;
}

/* MEJORA VISUAL PARA FECHAS */
input[type="date"] {
    font-family: inherit;
}

input[type="date"]::-webkit-calendar-picker-indicator {
    cursor: pointer;
    border-radius: 4px;
    padding: 4px;
}

input[type="date"]::-webkit-calendar-picker-indicator:hover {
    background: #3498db;
}
</style>