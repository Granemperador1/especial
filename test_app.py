import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from app import app, get_db_connection, init_database, execute_query, call_stored_procedure
from config import DatabaseConfig

class TestMindSchoolApp(unittest.TestCase):
    """Clase principal para tests de la aplicación MindSchool"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Crear archivo temporal para uploads
        self.temp_dir = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.temp_dir
    
    def tearDown(self):
        """Limpieza después de cada test"""
        self.app_context.pop()
        # Limpiar archivos temporales
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_index_page(self):
        """Test: Página principal se carga correctamente"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MindSchool', response.data)
        self.assertIn(b'Academia Digital', response.data)
    
    def test_login_page_accessible(self):
        """Test: Página de login es accesible"""
        response = self.app.get('/')
        # Simular click en login
        self.assertIn(b'Iniciar Sesion', response.data)
    
    @patch('app.get_db_connection')
    def test_login_success(self, mock_db):
        """Test: Login exitoso"""
        # Mock de la conexión a la base de datos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular usuario encontrado
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'email': 'estudiante@mindschool.com',
            'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.Ge',  # password123
            'name': 'Juan Pérez',
            'user_type': 'student'
        }
        mock_db.return_value = mock_conn
        
        response = self.app.post('/login', data={
            'email': 'estudiante@mindschool.com',
            'password': 'password123',
            'userType': 'student'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['name'], 'Juan Pérez')
    
    @patch('app.get_db_connection')
    def test_login_failure(self, mock_db):
        """Test: Login fallido"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_db.return_value = mock_conn
        
        response = self.app.post('/login', data={
            'email': 'usuario@incorrecto.com',
            'password': 'password_incorrecto',
            'userType': 'student'
        })
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('app.get_db_connection')
    def test_payment_processing(self, mock_db):
        """Test: Procesamiento de pagos"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        response = self.app.post('/payment', data={
            'user_id': '1',
            'paymentType': 'tuition',
            'amount': '1500.00'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('Pago procesado exitosamente', data['message'])
    
    @patch('app.get_db_connection')
    def test_forum_post_creation(self, mock_db):
        """Test: Creación de posts en el foro"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        response = self.app.post('/forum/post', data={
            'title': 'Test Post',
            'category': 'general',
            'content': 'Este es un post de prueba',
            'author_id': '1'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    @patch('app.get_db_connection')
    def test_get_forum_posts(self, mock_db):
        """Test: Obtener posts del foro"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular posts existentes
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'title': 'Test Post 1',
                'content': 'Contenido 1',
                'category': 'general',
                'author_name': 'Juan Pérez',
                'created_at': '2024-01-01 10:00:00'
            },
            {
                'id': 2,
                'title': 'Test Post 2',
                'content': 'Contenido 2',
                'category': 'homework',
                'author_name': 'María González',
                'created_at': '2024-01-01 11:00:00'
            }
        ]
        mock_db.return_value = mock_conn
        
        response = self.app.get('/forum/posts')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('posts', data)
        self.assertEqual(len(data['posts']), 2)
    
    @patch('app.get_db_connection')
    def test_send_message(self, mock_db):
        """Test: Envío de mensajes"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        response = self.app.post('/message/send', data={
            'sender_id': '1',
            'recipient': '2',
            'subject': 'Test Message',
            'content': 'Este es un mensaje de prueba'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    @patch('app.get_db_connection')
    def test_get_messages(self, mock_db):
        """Test: Obtener mensajes de un usuario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular mensajes existentes
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'sender_id': 1,
                'recipient_id': 2,
                'subject': 'Test Message 1',
                'content': 'Contenido 1',
                'sender_name': 'Juan Pérez',
                'recipient_name': 'María González',
                'read': False,
                'created_at': '2024-01-01 10:00:00'
            }
        ]
        mock_db.return_value = mock_conn
        
        response = self.app.get('/messages/1')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('messages', data)
        self.assertEqual(len(data['messages']), 1)
    
    def test_task_upload(self):
        """Test: Subida de tareas"""
        # Crear archivo temporal para el test
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(b'Test file content')
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as file:
                response = self.app.post('/task/upload', data={
                    'title': 'Test Task',
                    'subject': 'math',
                    'description': 'Descripción de prueba',
                    'student_id': '1'
                }, files={'file': (file, 'test.pdf')})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
        finally:
            os.unlink(temp_file_path)
    
    @patch('app.get_db_connection')
    def test_get_tasks(self, mock_db):
        """Test: Obtener tareas de un usuario"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular tareas existentes
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'title': 'Test Task 1',
                'subject': 'math',
                'description': 'Descripción 1',
                'student_name': 'Juan Pérez',
                'status': 'pending',
                'grade': None,
                'submitted_at': '2024-01-01 10:00:00'
            }
        ]
        mock_db.return_value = mock_conn
        
        response = self.app.get('/tasks/1')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tasks', data)
        self.assertEqual(len(data['tasks']), 1)
    
    @patch('app.get_db_connection')
    def test_get_videos(self, mock_db):
        """Test: Obtener videos"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Simular videos existentes
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'title': 'Introducción al Álgebra',
                'description': 'Conceptos básicos del álgebra',
                'subject': 'Matemáticas',
                'duration': 45,
                'difficulty': 'Básico',
                'video_url': 'https://example.com/video1.mp4',
                'created_at': '2024-01-01 10:00:00'
            }
        ]
        mock_db.return_value = mock_conn
        
        response = self.app.get('/videos')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('videos', data)
        self.assertEqual(len(data['videos']), 1)

class TestDatabaseConnection(unittest.TestCase):
    """Tests para la conexión a la base de datos"""
    
    @patch('psycopg2.connect')
    def test_database_connection_success(self, mock_connect):
        """Test: Conexión exitosa a la base de datos"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        from app import get_db_connection
        conn = get_db_connection()
        
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once()
    
    @patch('psycopg2.connect')
    def test_database_connection_failure(self, mock_connect):
        """Test: Fallo en la conexión a la base de datos"""
        mock_connect.side_effect = Exception("Connection failed")
        
        from app import get_db_connection
        conn = get_db_connection()
        
        self.assertIsNone(conn)
    
    def test_database_config(self):
        """Test: Configuración de la base de datos"""
        config = DatabaseConfig.get_config()
        
        self.assertIn('host', config)
        self.assertIn('database', config)
        self.assertIn('user', config)
        self.assertIn('password', config)
        self.assertIn('port', config)
        
        self.assertEqual(config['database'], 'mindschool')
        self.assertEqual(config['port'], '5432')

class TestUtilityFunctions(unittest.TestCase):
    """Tests para funciones utilitarias"""
    
    @patch('app.get_db_connection')
    def test_execute_query_select(self, mock_db):
        """Test: Ejecutar query SELECT"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Test'}]
        mock_db.return_value = mock_conn
        
        result = execute_query("SELECT * FROM users")
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test')
    
    @patch('app.get_db_connection')
    def test_execute_query_insert(self, mock_db):
        """Test: Ejecutar query INSERT"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        mock_db.return_value = mock_conn
        
        result = execute_query("INSERT INTO users (name) VALUES (%s)", ('Test User',))
        
        self.assertIsNotNone(result)
        self.assertEqual(result['affected_rows'], 1)
    
    @patch('app.get_db_connection')
    def test_call_stored_procedure(self, mock_db):
        """Test: Llamar procedimiento almacenado"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        result = call_stored_procedure('sp_test_procedure', ['param1', 'param2'])
        
        self.assertIsNotNone(result)
        self.assertTrue(result['success'])

class TestFormValidation(unittest.TestCase):
    """Tests para validación de formularios"""
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_login_form_validation(self):
        """Test: Validación del formulario de login"""
        # Test sin datos
        response = self.app.post('/login', data={})
        self.assertEqual(response.status_code, 400)
        
        # Test con datos incompletos
        response = self.app.post('/login', data={
            'email': 'test@example.com'
            # Falta password y userType
        })
        self.assertEqual(response.status_code, 400)
    
    def test_payment_form_validation(self):
        """Test: Validación del formulario de pago"""
        # Test sin datos
        response = self.app.post('/payment', data={})
        self.assertEqual(response.status_code, 400)
        
        # Test con datos incompletos
        response = self.app.post('/payment', data={
            'paymentType': 'tuition'
            # Falta amount
        })
        self.assertEqual(response.status_code, 400)

def run_tests():
    """Función para ejecutar todos los tests"""
    # Crear suite de tests
    test_suite = unittest.TestSuite()
    
    # Agregar tests
    test_suite.addTest(unittest.makeSuite(TestMindSchoolApp))
    test_suite.addTest(unittest.makeSuite(TestDatabaseConnection))
    test_suite.addTest(unittest.makeSuite(TestUtilityFunctions))
    test_suite.addTest(unittest.makeSuite(TestFormValidation))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print(f"RESUMEN DE TESTS")
    print(f"{'='*50}")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests fallidos: {len(result.failures)}")
    print(f"Tests con errores: {len(result.errors)}")
    
    if result.failures:
        print(f"\nFALLOS:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORES:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 INICIANDO TESTS DE MINDSCHOOL")
    print("="*50)
    
    success = run_tests()
    
    if success:
        print("\n✅ TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
    
    print("\n🎓 MindSchool - Sistema de Pruebas Completado") 