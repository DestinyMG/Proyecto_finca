<template>
    <BaseAdmin>
        <template #default>
            <div class="sanidad-container">
                <div class="sanidad-header">
                    <h2>Gestión de Vacunas</h2>
                    <button class="toggle-form-btn" @click="toggleForm">
                        {{ isFormVisible ? 'Ocultar Formulario' : 'Añadir Vacuna' }}
                    </button>
                </div>

                <!-- FORMULARIO -->
                <Transition name="slide-fade">
                    <div v-if="isFormVisible" class="form-wrapper">
                        <div class="form-card">
                            <h3>{{ isEditing ? 'Editar Vacuna' : 'Registrar Vacuna' }}</h3>
                            <p>Registra o modifica una vacuna disponible para el ganado.</p>

                            <form @submit.prevent="guardarVacuna">
                                <div class="form-group">
                                    <label for="nombre">Nombre de la Vacuna</label>
                                    <input id="nombre" type="text" v-model="formData.nombre" required />
                                </div>

                                <div class="form-group">
                                    <label for="descripcion">Descripción (Opcional)</label>
                                    <textarea id="descripcion" v-model="formData.descripcion" rows="3"></textarea>
                                </div>

                                <div class="form-actions">
                                    <button v-if="isEditing" type="button" class="cancel-btn" @click="cancelarEdicion">
                                        Cancelar
                                    </button>
                                    <button type="submit" class="submit-btn">
                                        {{ isEditing ? 'Guardar Cambios' : 'Registrar Vacuna' }}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </Transition>

                <!-- LISTADO -->
                <div class="listado">
                    <h3>Listado de Vacunas</h3>
                    <div v-if="vacunas.length === 0" class="empty-state">No hay registros.</div>
                    <div v-else class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Nombre</th>
                                    <th>Descripción</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="v in vacunas" :key="v.id">
                                    <td>{{ v.nombre }}</td>
                                    <td>{{ v.descripcion || '—' }}</td>
                                    <td class="action-cell">
                                        <button @click="iniciarEdicion(v)" class="edit-btn">✏️</button>
                                        <button @click="eliminarVacuna(v.id)" class="delete-btn">🗑️</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </template>
    </BaseAdmin>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import BaseAdmin from '../components/BaseAdmin.vue';

const API_URL = 'http://localhost:8000/api2/vacunas/';

const vacunas = ref([]);
const isFormVisible = ref(false);
const isEditing = ref(false);
const formData = ref({ nombre: '', descripcion: '' });

const cargarVacunas = async () => {
    try {
        const res = await axios.get(API_URL);
        vacunas.value = res.data;
    } catch (err) {
        console.error(err);
        alert('Error al cargar las vacunas.');
    }
};

onMounted(cargarVacunas);

const toggleForm = () => {
    if (isFormVisible.value && isEditing.value) cancelarEdicion();
    isFormVisible.value = !isFormVisible.value;
};

const resetForm = () => {
    formData.value = { nombre: '', descripcion: '' };
    isEditing.value = false;
};

const cancelarEdicion = () => {
    resetForm();
    isFormVisible.value = false;
};

const guardarVacuna = async () => {
    try {
        if (isEditing.value) {
            await axios.put(`${API_URL}${formData.value.id}/`, formData.value);
            alert('Vacuna actualizada correctamente.');
        } else {
            await axios.post(API_URL, formData.value);
            alert('Vacuna registrada correctamente.');
        }
        await cargarVacunas();
        resetForm();
        isFormVisible.value = false;
    } catch (err) {
        console.error(err.response?.data || err);
        alert('Error al guardar la vacuna.');
    }
};

const iniciarEdicion = (v) => {
    formData.value = { ...v };
    isEditing.value = true;
    isFormVisible.value = true;
};

const eliminarVacuna = async (id) => {
    if (confirm('¿Seguro que deseas eliminar esta vacuna?')) {
        try {
            await axios.delete(`${API_URL}${id}/`);
            await cargarVacunas();
            alert('Vacuna eliminada.');
        } catch (err) {
            console.error(err);
            alert('Error al eliminar la vacuna.');
        }
    }
};
</script>

<style scoped>
.sanidad-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    min-height: calc(100vh - 70px);
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

/* Header Styles */
.sanidad-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, #ffffff 0%, #f8f6f2 100%);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(45, 90, 58, 0.1);
    border: 1px solid #e8d9c5;
    position: relative;
    overflow: hidden;
}

.sanidad-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #2d5a3a, #4a9e64);
}

.sanidad-header h2 {
    color: #2d5a3a;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
    font-family: 'Georgia', serif;
    text-shadow: 1px 1px 2px rgba(45, 90, 58, 0.1);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.sanidad-header h2::before {
    content: "💉";
    font-size: 1.5rem;
}

.toggle-form-btn {
    background: linear-gradient(135deg, #2d5a3a, #4a9e64);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(45, 90, 58, 0.3);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.toggle-form-btn::before {
    content: "➕";
    font-size: 1.1rem;
}

.toggle-form-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(45, 90, 58, 0.4);
    background: linear-gradient(135deg, #4a9e64, #2d5a3a);
}

/* Form Styles */
.form-wrapper {
    margin-bottom: 2rem;
}

.form-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(45, 90, 58, 0.1);
    border: 1px solid #e8d9c5;
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
    background: linear-gradient(180deg, #2d5a3a, #4a9e64);
}

.form-card h3 {
    color: #2d5a3a;
    margin-bottom: 0.5rem;
    font-size: 1.4rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.form-card h3::before {
    content: "💊";
    font-size: 1.2rem;
}

.form-card p {
    color: #6c757d;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
    line-height: 1.5;
    padding-left: 1.75rem;
}

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

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #e8d9c5;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: #faf9f7;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #4a9e64;
    background: white;
    box-shadow: 0 0 0 3px rgba(74, 158, 100, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #e8d9c5;
}

.cancel-btn {
    background: #6c757d;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cancel-btn:hover {
    background: #5a6268;
    transform: translateY(-1px);
}

.submit-btn {
    background: linear-gradient(135deg, #4a9e64, #3a8c54);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(74, 158, 100, 0.3);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.submit-btn::before {
    content: "💾";
    font-size: 1rem;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(74, 158, 100, 0.4);
    background: linear-gradient(135deg, #3a8c54, #4a9e64);
}

/* List Styles */
.listado {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(45, 90, 58, 0.1);
    border: 1px solid #e8d9c5;
    overflow: hidden;
}

.listado h3 {
    background: linear-gradient(135deg, #2d5a3a, #4a9e64);
    color: white;
    margin: 0;
    padding: 1.25rem 2rem;
    font-size: 1.3rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.listado h3::before {
    content: "📋";
    font-size: 1.2rem;
}

.empty-state {
    padding: 3rem 2rem;
    text-align: center;
    color: #6c757d;
    font-style: italic;
    background: #f8f9fa;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.empty-state::before {
    content: "💉";
    font-size: 3rem;
    opacity: 0.5;
}

.table-wrapper {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

thead {
    background: linear-gradient(135deg, #f8f6f2, #e8d9c5);
}

th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: #2d5a3a;
    border-bottom: 2px solid #e8d9c5;
    font-size: 0.95rem;
}

td {
    padding: 1rem;
    border-bottom: 1px solid #e8d9c5;
    color: #555;
}

tbody tr {
    transition: all 0.3s ease;
}

tbody tr:hover {
    background: rgba(74, 158, 100, 0.05);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(45, 90, 58, 0.1);
}

.action-cell {
    display: flex;
    gap: 0.5rem;
    justify-content: flex-start;
}

.edit-btn,
.delete-btn {
    background: none;
    border: none;
    padding: 0.5rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1.1rem;
}

.edit-btn {
    background: rgba(45, 90, 58, 0.1);
    color: #2d5a3a;
}

.edit-btn:hover {
    background: #2d5a3a;
    color: white;
    transform: scale(1.1);
}

.delete-btn {
    background: rgba(220, 53, 69, 0.1);
    color: #dc3545;
}

.delete-btn:hover {
    background: #dc3545;
    color: white;
    transform: scale(1.1);
}

/* Transition Animations */
.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from {
    transform: translateY(-10px);
    opacity: 0;
}

.slide-fade-leave-to {
    transform: translateY(-10px);
    opacity: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
    .sanidad-container {
        padding: 1rem;
    }

    .sanidad-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
        padding: 1rem;
    }

    .sanidad-header h2 {
        font-size: 1.5rem;
    }

    .form-card {
        padding: 1.5rem;
    }

    .form-actions {
        flex-direction: column;
    }

    .form-actions button {
        width: 100%;
    }

    .listado h3 {
        padding: 1rem;
        font-size: 1.2rem;
    }

    th,
    td {
        padding: 0.75rem 0.5rem;
        font-size: 0.9rem;
    }

    .action-cell {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .sanidad-container {
        padding: 0.5rem;
    }

    .form-card {
        padding: 1rem;
    }

    table {
        font-size: 0.85rem;
    }

    th,
    td {
        padding: 0.5rem 0.25rem;
    }

    .sanidad-header h2::before,
    .form-card h3::before,
    .listado h3::before {
        display: none;
    }
}

/* Estado vacío mejorado */
.empty-state {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border: 2px dashed #dee2e6;
    border-radius: 12px;
    margin: 1rem;
}

.empty-state::after {
    content: "Haz clic en 'Añadir Vacuna' para comenzar";
    font-size: 0.9rem;
    color: #6c757d;
    font-style: normal;
}
</style>