
#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add project to path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Triplicity.settings')

try:
    print("🔄 Setting up Django...")
    django.setup()
    print("✅ Django setup successful!")
    
    # Import settings to check configuration
    from django.conf import settings
    print(f"✅ Settings loaded from: {settings.SETTINGS_MODULE}")
    
    # Test database connection
    print("🔄 Testing database connection...")
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"✅ Database connection successful! Result: {result}")
    
    # Test apps loading
    from django.apps import apps
    app_configs = apps.get_app_configs()
    print(f"✅ Loaded {len(app_configs)} apps successfully!")
    
    # List all installed apps
    print("\n📋 Installed Apps:")
    for app in app_configs:
        print(f"   - {app.name} ({app.label})")
    
    # Test static files configuration
    print(f"\n✅ Static files configuration: {settings.STATIC_URL}")
    print(f"✅ Media files configuration: {settings.MEDIA_URL}")
    
    # Test custom user model
    print(f"✅ Custom user model: {settings.AUTH_USER_MODEL}")
    
    # Test database configuration
    db_config = settings.DATABASES['default']
    print(f"✅ Database engine: {db_config['ENGINE']}")
    print(f"✅ Database name: {db_config['NAME']}")
    
    print("\n🎉 All tests passed! Your Django setup is working correctly.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
