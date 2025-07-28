#!/usr/bin/env python3
"""
Script de pruebas simple para MindSchool
Ejecuta tests básicos de funcionalidad
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
TEST_USER = {
    'email': 'estudiante@mindschool.com',
    'password': 'password123',
    'userType': 'student'
}

def print_test_header(test_name):
    """Imprime el encabezado de un test"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*60}")

def print_test_result(test_name, success, message=""):
    """Imprime el resultado de un test"""
    status = "✅ PASÓ" if success else "❌ FALLÓ"
    print(f"{status} - {test_name}")
    if message:
        print(f"   📝 {message}")

def test_server_running():
    """Test 1: Verificar que el servidor esté ejecutándose"""
    print_test_header("SERVIDOR EJECUTÁNDOSE")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        success = response.status_code == 200
        print_test_result("Servidor respondiendo", success, f"Status: {response.status_code}")
        return success
    except requests.exceptions.ConnectionError:
        print_test_result("Servidor respondiendo", False, "No se puede conectar al servidor")
        return False
    except Exception as e:
        print_test_result("Servidor respondiendo", False, f"Error: {str(e)}")
        return False

def test_home_page_content():
    """Test 2: Verificar contenido de la página principal"""
    print_test_header("CONTENIDO DE LA PÁGINA PRINCIPAL")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        content = response.text.lower()
        
        # Verificar elementos clave
        tests = [
            ("Título MindSchool", "mindschool" in content),
            ("Academia Digital", "academia digital" in content),
            ("Formulario de login", "iniciar sesión" in content),
            ("Sección de pagos", "pagos" in content),
            ("Sección de foro", "foro" in content),
            ("Sección de mensajes", "mensajes" in content),
            ("Sección de tareas", "tareas" in content),
            ("Sección de videos", "videos" in content)
        ]
        
        all_passed = True
        for test_name, passed in tests:
            print_test_result(test_name, passed)
            if not passed:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print_test_result("Contenido de página", False, f"Error: {str(e)}")
        return False

def test_login_functionality():
    """Test 3: Verificar funcionalidad de login"""
    print_test_header("FUNCIONALIDAD DE LOGIN")
    
    try:
        # Test de login exitoso
        response = requests.post(f"{BASE_URL}/login", data=TEST_USER)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print_test_result("Login exitoso", success)
            
            if success:
                user = data.get('user', {})
                print(f"   👤 Usuario: {user.get('name', 'N/A')}")
                print(f"   📧 Email: {user.get('email', 'N/A')}")
                print(f"   🏷️  Tipo: {user.get('type', 'N/A')}")
            
            return success
        else:
            print_test_result("Login exitoso", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Login exitoso", False, f"Error: {str(e)}")
        return False

def test_payment_functionality():
    """Test 4: Verificar funcionalidad de pagos"""
    print_test_header("FUNCIONALIDAD DE PAGOS")
    
    try:
        payment_data = {
            'user_id': '1',
            'paymentType': 'tuition',
            'amount': '1500.00'
        }
        
        response = requests.post(f"{BASE_URL}/payment", data=payment_data)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print_test_result("Procesamiento de pago", success)
            
            if success:
                print(f"   💰 Tipo: {payment_data['paymentType']}")
                print(f"   💵 Monto: ${payment_data['amount']}")
            
            return success
        else:
            print_test_result("Procesamiento de pago", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Procesamiento de pago", False, f"Error: {str(e)}")
        return False

def test_forum_functionality():
    """Test 5: Verificar funcionalidad del foro"""
    print_test_header("FUNCIONALIDAD DEL FORO")
    
    try:
        # Test crear post
        post_data = {
            'title': 'Test Post - ' + datetime.now().strftime('%H:%M:%S'),
            'category': 'general',
            'content': 'Este es un post de prueba automática',
            'author_id': '1'
        }
        
        response = requests.post(f"{BASE_URL}/forum/post", data=post_data)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print_test_result("Crear post en foro", success)
            
            if success:
                print(f"   📝 Título: {post_data['title']}")
                print(f"   🏷️  Categoría: {post_data['category']}")
            
            return success
        else:
            print_test_result("Crear post en foro", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Crear post en foro", False, f"Error: {str(e)}")
        return False

def test_message_functionality():
    """Test 6: Verificar funcionalidad de mensajes"""
    print_test_header("FUNCIONALIDAD DE MENSAJES")
    
    try:
        message_data = {
            'sender_id': '1',
            'recipient': '2',
            'subject': 'Test Message - ' + datetime.now().strftime('%H:%M:%S'),
            'content': 'Este es un mensaje de prueba automática'
        }
        
        response = requests.post(f"{BASE_URL}/message/send", data=message_data)
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print_test_result("Enviar mensaje", success)
            
            if success:
                print(f"   📧 Asunto: {message_data['subject']}")
                print(f"   👤 Destinatario: {message_data['recipient']}")
            
            return success
        else:
            print_test_result("Enviar mensaje", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Enviar mensaje", False, f"Error: {str(e)}")
        return False

def test_task_functionality():
    """Test 7: Verificar funcionalidad de tareas"""
    print_test_header("FUNCIONALIDAD DE TAREAS")
    
    try:
        # Crear archivo temporal para el test
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write('Contenido de prueba para la tarea')
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as file:
                files = {'file': ('test_task.txt', file, 'text/plain')}
                data = {
                    'title': 'Test Task - ' + datetime.now().strftime('%H:%M:%S'),
                    'subject': 'math',
                    'description': 'Descripción de prueba automática',
                    'student_id': '1'
                }
                
                response = requests.post(f"{BASE_URL}/task/upload", data=data, files=files)
            
            if response.status_code == 200:
                response_data = response.json()
                success = response_data.get('success', False)
                print_test_result("Subir tarea", success)
                
                if success:
                    print(f"   📚 Título: {data['title']}")
                    print(f"   📖 Materia: {data['subject']}")
                
                return success
            else:
                print_test_result("Subir tarea", False, f"Status: {response.status_code}")
                return False
                
        finally:
            import os
            os.unlink(temp_file_path)
            
    except Exception as e:
        print_test_result("Subir tarea", False, f"Error: {str(e)}")
        return False

def test_video_functionality():
    """Test 8: Verificar funcionalidad de videos"""
    print_test_header("FUNCIONALIDAD DE VIDEOS")
    
    try:
        response = requests.get(f"{BASE_URL}/videos")
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('videos', [])
            success = isinstance(videos, list)
            
            print_test_result("Obtener videos", success)
            
            if success:
                print(f"   🎥 Videos disponibles: {len(videos)}")
                if videos:
                    print(f"   📺 Primer video: {videos[0].get('title', 'N/A')}")
            
            return success
        else:
            print_test_result("Obtener videos", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Obtener videos", False, f"Error: {str(e)}")
        return False

def test_database_connection():
    """Test 9: Verificar conexión a la base de datos"""
    print_test_header("CONEXIÓN A BASE DE DATOS")
    
    try:
        # Intentar obtener posts del foro (requiere DB)
        response = requests.get(f"{BASE_URL}/forum/posts")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            success = isinstance(posts, list)
            
            print_test_result("Conexión a PostgreSQL", success)
            
            if success:
                print(f"   📊 Posts en foro: {len(posts)}")
            
            return success
        else:
            print_test_result("Conexión a PostgreSQL", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Conexión a PostgreSQL", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("🎓 MINDSCHOOL - SISTEMA DE PRUEBAS")
    print("="*60)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Lista de tests a ejecutar
    tests = [
        ("Servidor ejecutándose", test_server_running),
        ("Contenido de página principal", test_home_page_content),
        ("Funcionalidad de login", test_login_functionality),
        ("Funcionalidad de pagos", test_payment_functionality),
        ("Funcionalidad del foro", test_forum_functionality),
        ("Funcionalidad de mensajes", test_message_functionality),
        ("Funcionalidad de tareas", test_task_functionality),
        ("Funcionalidad de videos", test_video_functionality),
        ("Conexión a base de datos", test_database_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN FINAL DE TESTS")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   Total de tests: {total}")
    print(f"   Tests exitosos: {passed}")
    print(f"   Tests fallidos: {total - passed}")
    print(f"   Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print(f"\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FALLARON")
    
    print(f"\n⏰ Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrumpidos por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Error inesperado: {str(e)}")
        sys.exit(1) 