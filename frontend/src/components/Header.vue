<template>
    <header class="admin-header">
        <button class="hamburger-btn" @click="emitToggleSidebar">
            <span class="hamburger-icon">☰</span>
        </button>

        <div class="header-title">
            <span class="title-icon">🌾</span>
            <span class="title-text">Gestión de Finca</span>
        </div>

        <div class="spacer"></div>

        <div class="header-actions">
            <div class="farm-status">
                <span class="status-icon">🌤️</span>
                <span class="status-text">Buen día para trabajar</span>
            </div>

            <button class="notification-btn">
                <span class="notification-icon">🔔</span>
                <span class="notification-badge">3</span>
            </button>

            <div class="user-info">
                <div class="user-avatar">
                    <span class="avatar-icon">👨‍🌾</span>
                </div>
                <div class="user-details">
                    <span class="user-name">ADMIN ADMIN</span>
                    <span class="user-role">Administrador de Finca</span>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
// Define el evento que se va a emitir
const emit = defineEmits(['toggle-sidebar']);

// Función para emitir el evento al componente padre (BaseAdmin)
const emitToggleSidebar = () => {
    emit('toggle-sidebar');
};
</script>

<style scoped>
.admin-header {
    height: 70px;
    background: linear-gradient(135deg, #ffffff 0%, #f8f6f2 100%);
    border-bottom: 2px solid #e8d9c5;
    box-shadow: 0 2px 8px rgba(45, 90, 58, 0.1);
    display: flex;
    align-items: center;
    padding: 0 2rem;
    width: 100%;
    flex-shrink: 0;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
}

/* Efecto de fondo sutil con patrón agrícola */
.admin-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23d4a574' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.3;
    z-index: 0;
}

.hamburger-btn {
    display: none;
    background: #d4a574;
    border: none;
    border-radius: 8px;
    width: 45px;
    height: 45px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(212, 165, 116, 0.3);
    position: relative;
    z-index: 1;
}

.hamburger-btn:hover {
    background: #c19564;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(212, 165, 116, 0.4);
}

.hamburger-icon {
    font-size: 1.4rem;
    color: #2d5a3a;
    font-weight: bold;
}

.header-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    position: relative;
    z-index: 1;
}

.title-icon {
    font-size: 1.8rem;
    animation: gentle-sway 3s ease-in-out infinite;
}

@keyframes gentle-sway {

    0%,
    100% {
        transform: rotate(-5deg);
    }

    50% {
        transform: rotate(5deg);
    }
}

.title-text {
    font-size: 1.4rem;
    font-weight: 700;
    color: #2d5a3a;
    font-family: 'Georgia', serif;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 2px rgba(45, 90, 58, 0.1);
}

.spacer {
    flex-grow: 1;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    position: relative;
    z-index: 1;
}

.farm-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(212, 165, 116, 0.1);
    border-radius: 20px;
    border: 1px solid rgba(212, 165, 116, 0.3);
}

.status-icon {
    font-size: 1.2rem;
}

.status-text {
    font-size: 0.9rem;
    color: #2d5a3a;
    font-weight: 500;
}

.notification-btn {
    position: relative;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    transition: background-color 0.3s ease;
}

.notification-btn:hover {
    background: rgba(212, 165, 116, 0.1);
}

.notification-icon {
    font-size: 1.4rem;
    color: #d4a574;
}

.notification-badge {
    position: absolute;
    top: 0;
    right: 0;
    background: #e74c3c;
    color: white;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    font-size: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 1rem;
    background: rgba(45, 90, 58, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(45, 90, 58, 0.1);
    transition: all 0.3s ease;
}

.user-info:hover {
    background: rgba(45, 90, 58, 0.1);
    transform: translateY(-1px);
}

.user-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #d4a574, #c19564);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(212, 165, 116, 0.3);
}

.avatar-icon {
    font-size: 1.4rem;
}

.user-details {
    display: flex;
    flex-direction: column;
}

.user-name {
    font-weight: 700;
    color: #2d5a3a;
    font-size: 0.95rem;
}

.user-role {
    font-size: 0.8rem;
    color: #7a8c7d;
    font-weight: 500;
}

/* --- Estilos Responsivos --- */
@media (max-width: 768px) {
    .admin-header {
        height: 65px;
        padding: 0 1rem;
    }

    .hamburger-btn {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .header-title {
        margin-left: 1rem;
    }

    .title-text {
        font-size: 1.2rem;
    }

    .farm-status {
        display: none;
    }

    .user-details {
        display: none;
    }

    .user-info {
        padding: 0.5rem;
        background: none;
        border: none;
    }

    .user-info:hover {
        background: rgba(45, 90, 58, 0.05);
    }
}

@media (max-width: 480px) {
    .header-title .title-text {
        display: none;
    }

    .notification-btn .notification-icon {
        font-size: 1.2rem;
    }

    .user-avatar {
        width: 38px;
        height: 38px;
    }
}
</style>