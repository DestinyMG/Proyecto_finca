<template>
    <BaseAdmin>
        <template #default>
            <div class="sanidad-container">
                <div class="sanidad-header">
                    <h2>Gestión de Medicamentos</h2>
                    <button class="toggle-form-btn" @click="toggleForm">
                        {{ isFormVisible ? 'Ocultar Formulario' : 'Añadir Medicamento' }}
                    </button>
                </div>

                <Transition name="slide-fade">
                    <div v-if="isFormVisible" class="form-wrapper">
                        <div class="form-card">
                            <h3>{{ isEditing ? 'Editar Medicamento' : 'Registrar Medicamento' }}</h3>

                            <form @submit.prevent="guardarMedicamento">
                                <div class="form-group">
                                    <label for="nombre">Nombre</label>
                                    <input id="nombre" type="text" v-model="formData.nombre" required />
                                </div>

                                <div class="form-group">
                                    <label for="dosis">Dosis (Opcional)</label>
                                    <input id="dosis" type="text" v-model="formData.dosis" />
                                </div>

                                <div class="form-group">
                                    <label for="descripcion">Descripción</label>
                                    <textarea id="descripcion" v-model="formData.descripcion" rows="3"></textarea>
                                </div>

                                <div class="form-actions">
                                    <button v-if="isEditing" type="button" class="cancel-btn" @click="cancelarEdicion">
                                        Cancelar
                                    </button>
                                    <button type="submit" class="submit-btn">
                                        {{ isEditing ? 'Guardar Cambios' : 'Registrar' }}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </Transition>

                <div class="listado">
                    <h3>Listado de Medicamentos</h3>
                    <div v-if="medicamentos.length === 0" class="empty-state">No hay registros.</div>
                    <div v-else class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Nombre</th>
                                    <th>Dosis</th>
                                    <th>Descripción</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="m in medicamentos" :key="m.id">
                                    <td>{{ m.nombre }}</td>
                                    <td>{{ m.dosis || '—' }}</td>
                                    <td>{{ m.descripcion || '—' }}</td>
                                    <td class="action-cell">
                                        <button @click="iniciarEdicion(m)" class="edit-btn">✏️</button>
                                        <button @click="eliminarMedicamento(m.id)" class="delete-btn">🗑️</button>
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

const API_URL = 'http://localhost:8000/api2/medicamentos/';

const medicamentos = ref([]);
const isFormVisible = ref(false);
const isEditing = ref(false);
const formData = ref({ nombre: '', dosis: '', descripcion: '' });

const cargarMedicamentos = async () => {
    try {
        const res = await axios.get(API_URL);
        medicamentos.value = res.data;
    } catch (err) {
        console.error(err);
        alert('Error al cargar los medicamentos.');
    }
};

onMounted(cargarMedicamentos);

const toggleForm = () => {
    if (isFormVisible.value && isEditing.value) cancelarEdicion();
    isFormVisible.value = !isFormVisible.value;
};

const resetForm = () => {
    formData.value = { nombre: '', dosis: '', descripcion: '' };
    isEditing.value = false;
};

const cancelarEdicion = () => {
    resetForm();
    isFormVisible.value = false;
};

const guardarMedicamento = async () => {
    try {
        if (isEditing.value) {
            await axios.put(`${API_URL}${formData.value.id}/`, formData.value);
            alert('Medicamento actualizado correctamente.');
        } else {
            await axios.post(API_URL, formData.value);
            alert('Medicamento registrado correctamente.');
        }
        await cargarMedicamentos();
        resetForm();
        isFormVisible.value = false;
    } catch (err) {
        console.error(err.response?.data || err);
        alert('Error al guardar el medicamento.');
    }
};

const iniciarEdicion = (m) => {
    formData.value = { ...m };
    isEditing.value = true;
    isFormVisible.value = true;
};

const eliminarMedicamento = async (id) => {
    if (confirm('¿Seguro que deseas eliminar este medicamento?')) {
        try {
            await axios.delete(`${API_URL}${id}/`);
            await cargarMedicamentos();
            alert('Medicamento eliminado.');
        } catch (err) {
            console.error(err);
            alert('Error al eliminar el medicamento.');
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
    background: linear-gradient(90deg, #2d5a3a, #3498db);
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
    content: "💊";
    font-size: 1.5rem;
}

.toggle-form-btn {
    background: linear-gradient(135deg, #2d5a3a, #3498db);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
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
    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
    background: linear-gradient(135deg, #3498db, #2d5a3a);
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
    background: linear-gradient(180deg, #2d5a3a, #3498db);
}

.form-card h3 {
    color: #2d5a3a;
    margin-bottom: 1.5rem;
    font-size: 1.4rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-bottom: 2px solid #e8d9c5;
    padding-bottom: 0.5rem;
}

.form-card h3::before {
    content: "🧪";
    font-size: 1.2rem;
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
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.form-group label::after {
    content: "";
    font-size: 0.8rem;
    color: #6c757d;
}

.form-group label[for="dosis"]::after {
    content: "(Opcional)";
    margin-left: 0.25rem;
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
    border-color: #3498db;
    background: white;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
}

/* Estilo específico para el campo de dosis */
.form-group:nth-child(2) input {
    border-left: 4px solid #3498db;
    padding-left: 0.875rem;
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
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
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
    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
    background: linear-gradient(135deg, #2980b9, #3498db);
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
    background: linear-gradient(135deg, #2d5a3a, #3498db);
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
    content: "📑";
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
    content: "💊";
    font-size: 3rem;
    opacity: 0.5;
}

.empty-state::after {
    content: "Haz clic en 'Añadir Medicamento' para comenzar";
    font-size: 0.9rem;
    color: #6c757d;
    font-style: normal;
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
    position: relative;
}

th:not(:last-child)::after {
    content: "";
    position: absolute;
    right: 0;
    top: 25%;
    height: 50%;
    width: 1px;
    background: #e8d9c5;
}

td {
    padding: 1rem;
    border-bottom: 1px solid #e8d9c5;
    color: #555;
    vertical-align: top;
}

/* Estilo específico para columna de dosis */
td:nth-child(2) {
    font-family: 'Courier New', monospace;
    font-weight: 600;
    color: #3498db;
}

tbody tr {
    transition: all 0.3s ease;
}

tbody tr:hover {
    background: rgba(52, 152, 219, 0.05);
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
    background: rgba(52, 152, 219, 0.1);
    color: #3498db;
}

.edit-btn:hover {
    background: #3498db;
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
        flex-direction: column;
        gap: 0.25rem;
    }

    /* Ocultar descripción en móviles */
    th:nth-child(3),
    td:nth-child(3) {
        display: none;
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

    /* Ocultar dosis en móviles muy pequeños */
    th:nth-child(2),
    td:nth-child(2) {
        display: none;
    }
}

/* Estados especiales para medicamentos */
.medicamento-destacado {
    background: linear-gradient(135deg, rgba(52, 152, 219, 0.05), rgba(45, 90, 58, 0.05));
    border-left: 4px solid #3498db;
}

/* Tooltip para descripciones largas */
td:nth-child(3) {
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

td:nth-child(3):hover {
    white-space: normal;
    overflow: visible;
    background: white;
    z-index: 10;
    position: relative;
}
</style>