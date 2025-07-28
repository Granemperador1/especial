// Variables globales
let currentUser = null;
let currentView = 'welcome';

// Base de datos simulada con profesores pre-registrados
const teachers = [
    { id: 1, email: 'prof1@mindschool.com', password: 'prof123', name: 'Dr. María González', subject: 'Matemáticas' },
    { id: 2, email: 'prof2@mindschool.com', password: 'prof123', name: 'Lic. Carlos Rodríguez', subject: 'Español' },
    { id: 3, email: 'prof3@mindschool.com', password: 'prof123', name: 'Ing. Ana López', subject: 'Ciencias' },
    { id: 4, email: 'prof4@mindschool.com', password: 'prof123', name: 'Mtro. Pedro Martínez', subject: 'Historia' },
    { id: 5, email: 'prof5@mindschool.com', password: 'prof123', name: 'Lic. Laura Sánchez', subject: 'Inglés' },
    { id: 6, email: 'prof6@mindschool.com', password: 'prof123', name: 'Dr. Roberto Torres', subject: 'Física' },
    { id: 7, email: 'prof7@mindschool.com', password: 'prof123', name: 'Lic. Carmen Ruiz', subject: 'Química' },
    { id: 8, email: 'prof8@mindschool.com', password: 'prof123', name: 'Mtro. José Herrera', subject: 'Biología' },
    { id: 9, email: 'prof9@mindschool.com', password: 'prof123', name: 'Lic. Patricia Vega', subject: 'Geografía' },
    { id: 10, email: 'prof10@mindschool.com', password: 'prof123', name: 'Dr. Fernando Silva', subject: 'Filosofía' },
    { id: 11, email: 'prof11@mindschool.com', password: 'prof123', name: 'Lic. Isabel Morales', subject: 'Literatura' },
    { id: 12, email: 'prof12@mindschool.com', password: 'prof123', name: 'Mtro. Ricardo Castro', subject: 'Arte' },
    { id: 13, email: 'prof13@mindschool.com', password: 'prof123', name: 'Lic. Gabriela Luna', subject: 'Música' },
    { id: 14, email: 'prof14@mindschool.com', password: 'prof123', name: 'Dr. Alejandro Paredes', subject: 'Informática' },
    { id: 15, email: 'prof15@mindschool.com', password: 'prof123', name: 'Lic. Rosa Mendoza', subject: 'Economía' },
    { id: 16, email: 'prof16@mindschool.com', password: 'prof123', name: 'Mtro. Hugo Ríos', subject: 'Psicología' },
    { id: 17, email: 'prof17@mindschool.com', password: 'prof123', name: 'Lic. Diana Flores', subject: 'Sociología' },
    { id: 18, email: 'prof18@mindschool.com', password: 'prof123', name: 'Dr. Ernesto Vargas', subject: 'Derecho' },
    { id: 19, email: 'prof19@mindschool.com', password: 'prof123', name: 'Lic. Beatriz Ortega', subject: 'Administración' },
    { id: 20, email: 'prof20@mindschool.com', password: 'prof123', name: 'Mtro. Sergio Jiménez', subject: 'Contabilidad' },
    { id: 21, email: 'prof21@mindschool.com', password: 'prof123', name: 'Lic. Adriana Reyes', subject: 'Marketing' },
    { id: 22, email: 'prof22@mindschool.com', password: 'prof123', name: 'Dr. Manuel Acosta', subject: 'Finanzas' },
    { id: 23, email: 'prof23@mindschool.com', password: 'prof123', name: 'Lic. Claudia Soto', subject: 'Recursos Humanos' },
    { id: 24, email: 'prof24@mindschool.com', password: 'prof123', name: 'Mtro. Francisco León', subject: 'Logística' },
    { id: 25, email: 'prof25@mindschool.com', password: 'prof123', name: 'Lic. Elena Cruz', subject: 'Turismo' },
    { id: 26, email: 'prof26@mindschool.com', password: 'prof123', name: 'Dr. Raúl Méndez', subject: 'Medicina' },
    { id: 27, email: 'prof27@mindschool.com', password: 'prof123', name: 'Lic. Norma Aguilar', subject: 'Enfermería' },
    { id: 28, email: 'prof28@mindschool.com', password: 'prof123', name: 'Mtro. Víctor Moreno', subject: 'Odontología' },
    { id: 29, email: 'prof29@mindschool.com', password: 'prof123', name: 'Lic. Lucía Guerrero', subject: 'Farmacia' },
    { id: 30, email: 'prof30@mindschool.com', password: 'prof123', name: 'Dr. Arturo Delgado', subject: 'Veterinaria' }
];

// Base de datos de estudiantes
let students = [
    {
        id: 1,
        email: 'alumno1@mindschool.com',
        password: 'alumno123',
        name: 'Juan Carlos Pérez García',
        semester: 3,
        group: 'A',
        subjects: [
            { id: 'MAT301', name: 'Matemáticas III', teacher: 'Dr. María González', code: 'MAT301-3A' },
            { id: 'ESP301', name: 'Español III', teacher: 'Lic. Carlos Rodríguez', code: 'ESP301-3A' },
            { id: 'CIE301', name: 'Ciencias III', teacher: 'Ing. Ana López', code: 'CIE301-3A' }
        ]
    }
];

// Base de datos de materias por semestre
const subjectsBySemester = {
    1: [
        { id: 'MAT101', name: 'Matemáticas I', teacher: 'Dr. María González' },
        { id: 'ESP101', name: 'Español I', teacher: 'Lic. Carlos Rodríguez' },
        { id: 'CIE101', name: 'Ciencias I', teacher: 'Ing. Ana López' },
        { id: 'HIS101', name: 'Historia I', teacher: 'Mtro. Pedro Martínez' },
        { id: 'ING101', name: 'Inglés I', teacher: 'Lic. Laura Sánchez' }
    ],
    2: [
        { id: 'MAT102', name: 'Matemáticas II', teacher: 'Dr. María González' },
        { id: 'ESP102', name: 'Español II', teacher: 'Lic. Carlos Rodríguez' },
        { id: 'CIE102', name: 'Ciencias II', teacher: 'Ing. Ana López' },
        { id: 'HIS102', name: 'Historia II', teacher: 'Mtro. Pedro Martínez' },
        { id: 'ING102', name: 'Inglés II', teacher: 'Lic. Laura Sánchez' }
    ],
    3: [
        { id: 'MAT301', name: 'Matemáticas III', teacher: 'Dr. María González' },
        { id: 'ESP301', name: 'Español III', teacher: 'Lic. Carlos Rodríguez' },
        { id: 'CIE301', name: 'Ciencias III', teacher: 'Ing. Ana López' },
        { id: 'FIS301', name: 'Física I', teacher: 'Dr. Roberto Torres' },
        { id: 'GEO301', name: 'Geografía', teacher: 'Lic. Patricia Vega' }
    ],
    4: [
        { id: 'MAT302', name: 'Matemáticas IV', teacher: 'Dr. María González' },
        { id: 'ESP302', name: 'Español IV', teacher: 'Lic. Carlos Rodríguez' },
        { id: 'FIS302', name: 'Física II', teacher: 'Dr. Roberto Torres' },
        { id: 'QUI301', name: 'Química I', teacher: 'Lic. Carmen Ruiz' },
        { id: 'BIO301', name: 'Biología I', teacher: 'Mtro. José Herrera' }
    ],
    5: [
        { id: 'MAT501', name: 'Matemáticas V', teacher: 'Dr. María González' },
        { id: 'QUI302', name: 'Química II', teacher: 'Lic. Carmen Ruiz' },
        { id: 'BIO302', name: 'Biología II', teacher: 'Mtro. José Herrera' },
        { id: 'FIL301', name: 'Filosofía', teacher: 'Dr. Fernando Silva' },
        { id: 'LIT301', name: 'Literatura', teacher: 'Lic. Isabel Morales' }
    ],
    6: [
        { id: 'MAT502', name: 'Matemáticas VI', teacher: 'Dr. María González' },
        { id: 'FIS501', name: 'Física III', teacher: 'Dr. Roberto Torres' },
        { id: 'QUI501', name: 'Química III', teacher: 'Lic. Carmen Ruiz' },
        { id: 'ART301', name: 'Arte', teacher: 'Mtro. Ricardo Castro' },
        { id: 'MUS301', name: 'Música', teacher: 'Lic. Gabriela Luna' }
    ],
    7: [
        { id: 'MAT701', name: 'Matemáticas VII', teacher: 'Dr. María González' },
        { id: 'INF301', name: 'Informática', teacher: 'Dr. Alejandro Paredes' },
        { id: 'ECO301', name: 'Economía', teacher: 'Lic. Rosa Mendoza' },
        { id: 'PSI301', name: 'Psicología', teacher: 'Mtro. Hugo Ríos' },
        { id: 'SOC301', name: 'Sociología', teacher: 'Lic. Diana Flores' }
    ],
    8: [
        { id: 'MAT702', name: 'Matemáticas VIII', teacher: 'Dr. María González' },
        { id: 'DER301', name: 'Derecho', teacher: 'Dr. Ernesto Vargas' },
        { id: 'ADM301', name: 'Administración', teacher: 'Lic. Beatriz Ortega' },
        { id: 'CON301', name: 'Contabilidad', teacher: 'Mtro. Sergio Jiménez' },
        { id: 'MAR301', name: 'Marketing', teacher: 'Lic. Adriana Reyes' }
    ]
};

// Función para generar código de materia
function generateSubjectCode(subjectId, semester, group) {
    return `${subjectId}-${semester}${group}`;
}

// Función para mostrar notificaciones
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Función para cambiar entre tabs de login
function switchTab(type) {
    // Actualizar botones
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Ocultar todos los formularios
    document.querySelectorAll('.login-form').forEach(form => {
        form.classList.remove('active');
        form.style.display = 'none';
    });
    
    // Mostrar el formulario correspondiente
    if (type === 'student') {
        document.getElementById('studentLogin').classList.add('active');
        document.getElementById('studentLogin').style.display = 'block';
    } else if (type === 'teacher') {
        document.getElementById('teacherLogin').classList.add('active');
        document.getElementById('teacherLogin').style.display = 'block';
    }
}

// Función para mostrar formulario de registro
function showRegisterForm() {
    document.querySelectorAll('.login-form').forEach(form => {
        form.classList.remove('active');
        form.style.display = 'none';
    });
    
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('registerForm').classList.add('active');
}

// Función para mostrar formulario de login
function showLoginForm() {
    document.querySelectorAll('.login-form').forEach(form => {
        form.classList.remove('active');
        form.style.display = 'none';
    });
    
    document.getElementById('studentLogin').style.display = 'block';
    document.getElementById('studentLogin').classList.add('active');
    
    // Activar tab de estudiante
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('.tab-btn').classList.add('active');
}

// Función para cambiar vista
function changeView(view) {
    currentView = view;
    
    // Ocultar todas las vistas
    document.getElementById('welcomeView').style.display = 'none';
    document.getElementById('studentView').style.display = 'none';
    
    // Mostrar la vista correspondiente
    if (view === 'welcome') {
        document.getElementById('welcomeView').style.display = 'flex';
    } else if (view === 'student') {
        document.getElementById('studentView').style.display = 'block';
        loadStudentDashboard();
    }
}

// Función para cargar dashboard del estudiante
function loadStudentDashboard() {
    if (!currentUser) return;
    
    // Actualizar información del usuario
    document.getElementById('studentUserInfo').textContent = `Bienvenido, ${currentUser.name}`;
    
    // Cargar materias del estudiante
    const subjectsGrid = document.getElementById('subjectsGrid');
    subjectsGrid.innerHTML = '';
    
    currentUser.subjects.forEach(subject => {
        const subjectCard = createSubjectCard(subject);
        subjectsGrid.appendChild(subjectCard);
    });
}

// Función para crear tarjeta de materia
function createSubjectCard(subject) {
    const card = document.createElement('div');
    card.className = 'subject-card';
    
    const subjectIcons = {
        'MAT': '📐',
        'ESP': '📚',
        'CIE': '🔬',
        'HIS': '📜',
        'ING': '🌍',
        'FIS': '⚡',
        'GEO': '🌎',
        'QUI': '🧪',
        'BIO': '🧬',
        'FIL': '🤔',
        'LIT': '📖',
        'ART': '🎨',
        'MUS': '🎵',
        'INF': '💻',
        'ECO': '💰',
        'PSI': '🧠',
        'SOC': '👥',
        'DER': '⚖️',
        'ADM': '📊',
        'CON': '🧮',
        'MAR': '📈'
    };
    
    const icon = subjectIcons[subject.id.substring(0, 3)] || '📚';
    
    card.innerHTML = `
        <div class="subject-header">
            <div class="subject-icon">${icon}</div>
            <div class="subject-info">
                <h3>${subject.name}</h3>
                <div class="subject-code">${subject.code}</div>
            </div>
        </div>
        <div class="subject-details">
            <div class="subject-detail">
                <span class="detail-label">Profesor:</span>
                <span class="detail-value">${subject.teacher}</span>
            </div>
            <div class="subject-detail">
                <span class="detail-label">Semestre:</span>
                <span class="detail-value">${currentUser.semester}°</span>
            </div>
            <div class="subject-detail">
                <span class="detail-label">Grupo:</span>
                <span class="detail-value">${currentUser.group}</span>
            </div>
        </div>
        <div class="subject-actions">
            <button class="btn btn-primary" onclick="enterSubject('${subject.id}')">Entrar a Clase</button>
            <button class="btn btn-secondary" onclick="viewMaterials('${subject.id}')">Materiales</button>
        </div>
    `;
    
    return card;
}

// Función para entrar a una materia
function enterSubject(subjectId) {
    showNotification(`Entrando a la materia ${subjectId}...`);
    // Aquí se implementaría la lógica para entrar a la clase
}

// Función para ver materiales
function viewMaterials(subjectId) {
    showNotification(`Abriendo materiales de ${subjectId}...`);
    // Aquí se implementaría la lógica para ver materiales
}

// Función para cerrar sesión
function logout() {
    currentUser = null;
    currentView = 'welcome';
    changeView('welcome');
    showNotification('Sesión cerrada exitosamente');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Login de Estudiante
    document.getElementById('studentLoginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('studentEmail').value.trim();
        const password = document.getElementById('studentPassword').value;
        
        if (!email || !password) {
            showNotification('Por favor completa todos los campos', 'error');
            return;
        }
        
        const student = students.find(s => s.email === email && s.password === password);
        
        if (student) {
            currentUser = student;
            changeView('student');
            showNotification(`¡Bienvenido ${student.name}!`);
        } else {
            showNotification('Credenciales incorrectas', 'error');
        }
    });
    
    // Login de Profesor
    document.getElementById('teacherLoginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('teacherEmail').value.trim();
        const password = document.getElementById('teacherPassword').value;
        
        if (!email || !password) {
            showNotification('Por favor completa todos los campos', 'error');
            return;
        }
        
        const teacher = teachers.find(t => t.email === email && t.password === password);
        
        if (teacher) {
            showNotification(`¡Bienvenido Profesor ${teacher.name}!`, 'success');
            // Aquí se implementaría la vista del profesor
        } else {
            showNotification('Credenciales incorrectas', 'error');
        }
    });
    
    // Registro de Estudiante
    document.getElementById('studentRegisterForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const names = document.getElementById('regNames').value.trim();
        const lastNames = document.getElementById('regLastNames').value.trim();
        const semester = document.getElementById('regSemester').value;
        const group = document.getElementById('regGroup').value;
        const email = document.getElementById('regEmail').value.trim();
        const password = document.getElementById('regPassword').value;
        const confirmPassword = document.getElementById('regConfirmPassword').value;
        
        // Validaciones
        if (!names || !lastNames || !semester || !group || !email || !password || !confirmPassword) {
            showNotification('Por favor completa todos los campos', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            showNotification('Las contraseñas no coinciden', 'error');
            return;
        }
        
        if (password.length < 6) {
            showNotification('La contraseña debe tener al menos 6 caracteres', 'error');
            return;
        }
        
        // Verificar si el email ya existe
        const existingStudent = students.find(s => s.email === email);
        if (existingStudent) {
            showNotification('Este email ya está registrado', 'error');
            return;
        }
        
        // Crear nuevo estudiante
        const newStudent = {
            id: students.length + 1,
            email,
            password,
            name: `${names} ${lastNames}`,
            semester: parseInt(semester),
            group,
            subjects: subjectsBySemester[semester] ? subjectsBySemester[semester].map(subject => ({
                ...subject,
                code: generateSubjectCode(subject.id, semester, group)
            })) : []
        };
        
        students.push(newStudent);
        currentUser = newStudent;
        
        showNotification('¡Registro exitoso! Bienvenido a MindSchool');
        changeView('student');
        
        // Limpiar formulario
        document.getElementById('studentRegisterForm').reset();
    });
    
    // Inicializar vista de bienvenida
    changeView('welcome');
}); 