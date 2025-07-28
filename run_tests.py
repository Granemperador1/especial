#!/usr/bin/env python3
"""
Script principal para ejecutar todas las pruebas de MindSchool
"""

import sys
import subprocess
import os
from datetime import datetime

def print_header(title):
    """Imprimir encabezado"""
    print(f"\n{'='*60}")
    print(f"🎓 {title}")
    print(f"{'='*60}")

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔧 {description}")
    print(f"💻 Comando: {command}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("📤 Salida:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errores:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Comando ejecutado exitosamente")
            return True
        else:
            print(f"❌ Comando falló con código: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"💥 Error ejecutando comando: {e}")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    dependencies = [
        ("python3", "Python 3"),
        ("pip", "Pip"),
        ("psql", "PostgreSQL Client")
    ]
    
    all_installed = True
    
    for cmd, name in dependencies:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"✅ {name}: {version}")
            else:
                print(f"❌ {name}: No encontrado")
                all_installed = False
        except FileNotFoundError:
            print(f"❌ {name}: No encontrado")
            all_installed = False
    
    return all_installed

def install_requirements():
    """Instalar dependencias Python"""
    print_header("INSTALANDO DEPENDENCIAS PYTHON")
    
    if os.path.exists("requirements.txt"):
        return run_command("pip install -r requirements.txt", "Instalando dependencias desde requirements.txt")
    else:
        print("❌ Archivo requirements.txt no encontrado")
        return False

def test_database():
    """Probar base de datos"""
    print_header("PROBANDO BASE DE DATOS")
    return run_command("python3 test_db.py", "Ejecutando pruebas de base de datos")

def start_server():
    """Iniciar servidor en segundo plano"""
    print_header("INICIANDO SERVIDOR")
    
    # Verificar si el servidor ya está ejecutándose
    try:
        import requests
        response = requests.get("http://localhost:5000", timeout=2)
        if response.status_code == 200:
            print("✅ Servidor ya está ejecutándose en http://localhost:5000")
            return True
    except:
        pass
    
    # Iniciar servidor en segundo plano
    print("🚀 Iniciando servidor Flask...")
    try:
        # Usar nohup para ejecutar en segundo plano
        subprocess.Popen([
            "nohup", "python3", "app.py", ">", "server.log", "2>&1", "&"
        ], shell=True)
        
        # Esperar un momento para que el servidor inicie
        import time
        time.sleep(3)
        
        # Verificar si el servidor está ejecutándose
        try:
            import requests
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor iniciado exitosamente en http://localhost:5000")
                return True
            else:
                print(f"❌ Servidor respondió con código: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ No se pudo conectar al servidor: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False

def test_application():
    """Probar aplicación completa"""
    print_header("PROBANDO APLICACIÓN COMPLETA")
    return run_command("python3 test_simple.py", "Ejecutando pruebas de funcionalidad")

def show_menu():
    """Mostrar menú de opciones"""
    print_header("MENÚ DE PRUEBAS - MINDSCHOOL")
    print("1. 🔍 Verificar dependencias")
    print("2. 📦 Instalar dependencias Python")
    print("3. 🗄️  Probar base de datos")
    print("4. 🚀 Iniciar servidor")
    print("5. 🧪 Probar aplicación completa")
    print("6. 🎯 Ejecutar todas las pruebas")
    print("7. 📊 Ver logs del servidor")
    print("8. 🛑 Detener servidor")
    print("0. ❌ Salir")
    
    choice = input("\n👉 Selecciona una opción (0-8): ").strip()
    return choice

def show_server_logs():
    """Mostrar logs del servidor"""
    print_header("LOGS DEL SERVIDOR")
    
    if os.path.exists("server.log"):
        with open("server.log", "r") as f:
            logs = f.read()
            if logs:
                print(logs)
            else:
                print("📝 No hay logs disponibles")
    else:
        print("❌ Archivo de logs no encontrado")

def stop_server():
    """Detener servidor"""
    print_header("DETENIENDO SERVIDOR")
    
    try:
        # Buscar proceso de Python ejecutando app.py
        result = subprocess.run([
            "pkill", "-f", "python3 app.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servidor detenido exitosamente")
        else:
            print("ℹ️  No se encontró servidor ejecutándose")
        
        return True
    except Exception as e:
        print(f"❌ Error deteniendo servidor: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas en secuencia"""
    print_header("EJECUTANDO TODAS LAS PRUEBAS")
    
    steps = [
        ("Verificando dependencias", check_dependencies),
        ("Instalando dependencias Python", install_requirements),
        ("Probando base de datos", test_database),
        ("Iniciando servidor", start_server),
        ("Probando aplicación completa", test_application)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        result = step_func()
        results.append((step_name, result))
        
        if not result:
            print(f"❌ {step_name} falló. ¿Continuar? (s/n): ", end="")
            if input().lower() != 's':
                break
    
    # Resumen final
    print_header("RESUMEN DE PRUEBAS")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for step_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {step_name}")
    
    print(f"\n📊 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print("⚠️  Algunas pruebas fallaron")

def main():
    """Función principal"""
    print("🎓 MINDSCHOOL - SISTEMA DE PRUEBAS")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        choice = show_menu()
        
        if choice == "0":
            print("\n👋 ¡Hasta luego!")
            break
        elif choice == "1":
            check_dependencies()
        elif choice == "2":
            install_requirements()
        elif choice == "3":
            test_database()
        elif choice == "4":
            start_server()
        elif choice == "5":
            test_application()
        elif choice == "6":
            run_all_tests()
        elif choice == "7":
            show_server_logs()
        elif choice == "8":
            stop_server()
        else:
            print("❌ Opción inválida")
        
        input("\n⏸️  Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1) 