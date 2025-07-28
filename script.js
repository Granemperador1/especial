// Variables globales para simular base de datos
let currentUser = null;
let forumPosts = [];
let messages = [];
let tasks = [];
let videos = [];

// Función para mostrar páginas
function showPage(pageId) {
    // Ocultar todas las páginas
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Mostrar página seleccionada
    document.getElementById(pageId).classList.add('active');
    
    // Actualizar navegación
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    event.target.classList.add('active');
}

// Función para mostrar notificaciones
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');
    
    notificationText.textContent = message;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Simulación de conexión a base de datos PostgreSQL
function connectToDatabase() {
    // Simulación de conexión
    console.log('Conectando a PostgreSQL...');
    
    // Datos simulados
    return {
        users: [
            { id: 1, email: 'estudiante@mindschool.com', type: 'student', name: 'Juan Pérez' },
            { id: 2, email: 'profesor@mindschool.com', type: 'teacher', name: 'María González' },
            { id: 3, email: 'admin@mindschool.com', type: 'admin', name: 'Carlos Admin' }
        ],
        courses: [
            { id: 1, name: 'Matemáticas', teacher_id: 2 },
            { id: 2, name: 'Español', teacher_id: 2 },
            { id: 3, name: 'Ciencias', teacher_id: 2 }
        ],
        assignments: [],
        payments: [],
        forum_posts: [],
        messages: []
    };
}

// Inicializar base de datos simulada
const db = connectToDatabase();

// Bloquea navegación si no hay sesión iniciada
function handleProtectedNav(event, pageId) {
    event.preventDefault();
    if (!currentUser && pageId !== 'login') {
        openLoginModal();
        return;
    }
    showPage(pageId);
}

function openLoginModal() {
    document.getElementById('loginModal').style.display = 'flex';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function openRegisterModal() {
    document.getElementById('registerModal').style.display = 'flex';
}

function closeRegisterModal() {
    document.getElementById('registerModal').style.display = 'none';
}

// Funciones para el modal de subida de videos
function openUploadVideoModal() {
    if (!currentUser) {
        openLoginModal();
        return;
    }
    document.getElementById('uploadVideoModal').style.display = 'flex';
}

function closeUploadVideoModal() {
    document.getElementById('uploadVideoModal').style.display = 'none';
    document.getElementById('uploadVideoForm').reset();
    document.getElementById('videoMessage').textContent = '';
    document.getElementById('videoMessage').className = 'message';
}

// Función para detectar el tipo de plataforma de video
function getVideoPlatform(url) {
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
        return 'youtube';
    } else if (url.includes('vimeo.com')) {
        return 'vimeo';
    } else {
        return 'generic';
    }
}

// Función para extraer el ID del video de YouTube
function getYouTubeVideoId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}

// Función para extraer el ID del video de Vimeo
function getVimeoVideoId(url) {
    const regExp = /vimeo\.com\/([0-9]+)/;
    const match = url.match(regExp);
    return match ? match[1] : null;
}

// Funciones para agregar elementos al DOM
function addForumPostToDOM(post) {
    const forumPosts = document.getElementById('forumPosts');
    const categoryColors = {
        general: '#E0F2FE',
        homework: '#FEF3C7',
        projects: '#D1FAE5',
        doubts: '#DBEAFE'
    };
    
    const postElement = document.createElement('div');
    postElement.className = 'forum-post';
    postElement.innerHTML = `
        <div class="message-header">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="avatar">${post.author.substring(0, 2).toUpperCase()}</div>
                <div>
                    <strong>${post.author}</strong>
                    <div style="font-size: 0.8rem; color: #64748B;">Ahora</div>
                </div>
            </div>
            <span style="background: ${categoryColors[post.category] || '#E0F2FE'}; color: #0284C7; padding: 0.2rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">${post.category}</span>
        </div>
        <h4>${post.title}</h4>
        <p>${post.content}</p>
    `;
    
    forumPosts.insertBefore(postElement, forumPosts.firstChild);
}

function addMessageToDOM(message) {
    const messageThreads = document.getElementById('messageThreads');
    
    const messageElement = document.createElement('div');
    messageElement.className = 'message-thread';
    messageElement.innerHTML = `
        <div class="message-header">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="avatar">${message.sender.substring(0, 2).toUpperCase()}</div>
                <div>
                    <strong>${message.sender}</strong>
                    <div style="font-size: 0.8rem; color: #64748B;">Ahora</div>
                </div>
            </div>
            <span style="background: #DBEAFE; color: #1E40AF; padding: 0.2rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">Nuevo</span>
        </div>
        <h4>${message.subject}</h4>
        <p>${message.content}</p>
    `;
    
    messageThreads.insertBefore(messageElement, messageThreads.firstChild);
}

function addTaskToDOM(task) {
    const tasksList = document.getElementById('tasksList');
    
    const taskElement = document.createElement('div');
    taskElement.className = 'task-item';
    taskElement.innerHTML = `
        <div>
            <h4>${task.title}</h4>
            <p style="color: #64748B; margin: 0.5rem 0;">${task.subject} • Subido ahora</p>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span class="task-status status-pending">Pendiente</span>
            <button class="btn" style="padding: 0.5rem 1rem;">Ver</button>
        </div>
    `;
    
    tasksList.insertBefore(taskElement, tasksList.firstChild);
}

function addVideoToDOM(video) {
    const videoGrid = document.getElementById('videoGrid');
    const platform = getVideoPlatform(video.url);
    
    const levelColors = {
        basic: '#DBEAFE',
        intermediate: '#FEF3C7',
        advanced: '#D1FAE5'
    };
    
    const levelText = {
        basic: 'Básico',
        intermediate: 'Intermedio',
        advanced: 'Avanzado'
    };
    
    const videoElement = document.createElement('div');
    videoElement.className = 'video-card new';
    videoElement.innerHTML = `
        <div class="video-thumbnail ${platform}">
            ${platform === 'youtube' ? '📺' : platform === 'vimeo' ? '🎬' : '▶️'}
        </div>
        <div class="video-info">
            <h4>${video.title}</h4>
            <p style="color: #64748B; margin: 0.5rem 0;">${video.subject} • ${video.duration} min</p>
            <div class="video-meta">
                <span style="background: ${levelColors[video.level]}; color: ${video.level === 'basic' ? '#1E40AF' : video.level === 'intermediate' ? '#92400E' : '#065F46'}; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">${levelText[video.level]}</span>
                <div class="video-actions">
                    <button class="btn" onclick="watchVideo('${video.url}')">Ver Video</button>
                    <button class="btn" style="background: #eee; color: var(--blue);" onclick="shareVideo('${video.url}')">Compartir</button>
                </div>
            </div>
        </div>
    `;
    
    videoGrid.insertBefore(videoElement, videoGrid.firstChild);
    
    // Remover la clase 'new' después de 3 segundos
    setTimeout(() => {
        videoElement.classList.remove('new');
    }, 3000);
}

function watchVideo(url) {
    // Abrir el video en una nueva pestaña
    window.open(url, '_blank');
}

function shareVideo(url) {
    // Copiar URL al portapapeles
    navigator.clipboard.writeText(url).then(() => {
        showNotification('¡URL del video copiada al portapapeles!');
    }).catch(() => {
        showNotification('Error al copiar la URL', 'error');
    });
}

function updateUIForUser(user) {
    // Personalizar interfaz según tipo de usuario
    if (user.type === 'teacher') {
        // Mostrar opciones adicionales para profesores
        console.log('Usuario profesor logueado');
    } else if (user.type === 'admin') {
        // Mostrar opciones administrativas
        console.log('Usuario administrador logueado');
    }
}

// Función para simular consultas SQL
function executeQuery(query, params = []) {
    console.log(`Ejecutando query: ${query}`, params);
    
    // Simulación de diferentes tipos de consultas
    if (query.includes('SELECT * FROM users')) {
        return db.users;
    } else if (query.includes('INSERT INTO forum_posts')) {
        return { success: true, insertId: Date.now() };
    } else if (query.includes('INSERT INTO messages')) {
        return { success: true, insertId: Date.now() };
    }
    
    return { success: true };
}

// Simulación de procedimientos almacenados
function callStoredProcedure(procedureName, params) {
    console.log(`Llamando procedimiento: ${procedureName}`, params);
    
    switch (procedureName) {
        case 'sp_authenticate_user':
            return db.users.find(u => u.email === params.email);
        case 'sp_process_payment':
            return { success: true, transactionId: Date.now() };
        case 'sp_grade_assignment':
            return { success: true, graded: true };
        default:
            return { success: false, error: 'Procedimiento no encontrado' };
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Login Form
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const userType = document.getElementById('userType').value;
        
        // Simulación de autenticación
        const user = db.users.find(u => u.email === email && u.type === userType);
        
        if (user) {
            currentUser = user;
            showNotification(`¡Bienvenido ${user.name}!`);
            showPage('home');
            
            // Actualizar interfaz según tipo de usuario
            updateUIForUser(user);
        } else {
            showNotification('Credenciales incorrectas', 'error');
        }
    });

    // Payment Form
    document.getElementById('paymentForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const paymentData = {
            type: document.getElementById('paymentType').value,
            amount: document.getElementById('amount').value,
            cardNumber: document.getElementById('cardNumber').value,
            expiry: document.getElementById('expiry').value,
            cvv: document.getElementById('cvv').value,
            userId: currentUser?.id,
            date: new Date().toISOString()
        };
        
        // Simulación de procesamiento de pago
        db.payments.push(paymentData);
        
        showNotification('¡Pago procesado exitosamente!');
        document.getElementById('paymentForm').reset();
    });

    // Forum Form
    document.getElementById('forumForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const postData = {
            id: Date.now(),
            title: document.getElementById('forumTitle').value,
            category: document.getElementById('forumCategory').value,
            content: document.getElementById('forumContent').value,
            author: currentUser?.name || 'Usuario Anónimo',
            authorId: currentUser?.id,
            date: new Date().toISOString(),
            replies: []
        };
        
        db.forum_posts.push(postData);
        addForumPostToDOM(postData);
        
        showNotification('¡Publicación creada exitosamente!');
        document.getElementById('forumForm').reset();
    });

    // Message Form
    document.getElementById('messageForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const messageData = {
            id: Date.now(),
            recipient: document.getElementById('recipient').value,
            subject: document.getElementById('messageSubject').value,
            content: document.getElementById('messageContent').value,
            sender: currentUser?.name || 'Usuario Anónimo',
            senderId: currentUser?.id,
            date: new Date().toISOString(),
            read: false
        };
        
        db.messages.push(messageData);
        addMessageToDOM(messageData);
        
        showNotification('¡Mensaje enviado exitosamente!');
        document.getElementById('messageForm').reset();
    });

    // Task Form
    document.getElementById('taskForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const taskData = {
            id: Date.now(),
            title: document.getElementById('taskTitle').value,
            subject: document.getElementById('taskSubject').value,
            description: document.getElementById('taskDescription').value,
            file: document.getElementById('taskFile').files[0]?.name,
            student: currentUser?.name || 'Usuario Anónimo',
            studentId: currentUser?.id,
            date: new Date().toISOString(),
            status: 'pending',
            grade: null
        };
        
        db.assignments.push(taskData);
        addTaskToDOM(taskData);
        
        showNotification('¡Tarea subida exitosamente!');
        document.getElementById('taskForm').reset();
    });

    // Register Form
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('registerNames').value.trim();
        const lastNames = document.getElementById('registerLastNames').value.trim();
        const grade = document.getElementById('registerGrade').value;
        const group = document.getElementById('registerGroup').value;
        const type = document.getElementById('registerType').value;
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;

        const newUser = {
            id: Date.now(),
            email,
            type,
            name: `${name} ${lastNames}`,
            grade,
            group
        };
        db.users.push(newUser);
        currentUser = newUser;
        closeRegisterModal();
        showNotification('¡Registro exitoso!');
        showPage('home');
    });

    // Upload Video Form
    document.getElementById('uploadVideoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const videoData = {
            id: Date.now(),
            url: document.getElementById('videoUrl').value.trim(),
            title: document.getElementById('videoTitle').value.trim(),
            subject: document.getElementById('videoSubject').value,
            duration: parseInt(document.getElementById('videoDuration').value),
            level: document.getElementById('videoLevel').value,
            description: document.getElementById('videoDescription').value.trim(),
            uploadedBy: currentUser?.name || 'Usuario Anónimo',
            uploadedById: currentUser?.id,
            date: new Date().toISOString(),
            platform: getVideoPlatform(document.getElementById('videoUrl').value)
        };
        
        // Validar URL
        if (!videoData.url) {
            showVideoMessage('Por favor ingresa una URL válida', 'error');
            return;
        }
        
        // Validar plataforma soportada
        if (videoData.platform === 'generic') {
            showVideoMessage('Solo se soportan videos de YouTube y Vimeo', 'error');
            return;
        }
        
        // Simular subida exitosa
        db.videos = db.videos || [];
        db.videos.push(videoData);
        addVideoToDOM(videoData);
        
        showVideoMessage('¡Video subido exitosamente!', 'success');
        showNotification('¡Video agregado a la biblioteca!');
        
        // Limpiar formulario y cerrar modal después de 2 segundos
        setTimeout(() => {
            closeUploadVideoModal();
        }, 2000);
    });

    function showVideoMessage(message, type) {
        const messageDiv = document.getElementById('videoMessage');
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
    }

    // Formateo automático de campos
    document.getElementById('cardNumber').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s/g, '');
        let formattedValue = value.replace(/(.{4})/g, '$1 ');
        if (formattedValue.endsWith(' ')) {
            formattedValue = formattedValue.slice(0, -1);
        }
        e.target.value = formattedValue;
    });

    document.getElementById('expiry').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
            value = value.substring(0, 2) + '/' + value.substring(2, 4);
        }
        e.target.value = value;
    });

    // Inicialización
    showNotification('¡Bienvenido a MindSchool!');
    
    // Precargar algunos datos de ejemplo
    setTimeout(() => {
        console.log('Sistema MindSchool inicializado');
        console.log('Base de datos PostgreSQL simulada conectada');
    }, 1000);
}); 