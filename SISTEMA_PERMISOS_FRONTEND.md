# 🔐 SISTEMA DE PERMISOS Y RUTAS PROTEGIDAS - FRONTEND

## 📋 **RESUMEN DE IMPLEMENTACIÓN**

Se ha implementado un sistema completo de permisos y rutas protegidas que permite:

- ✅ **Clientes**: Solo acceso a login, registro, recuperar contraseña y módulos básicos
- ✅ **Administradores**: Acceso completo a todos los 15 módulos
- ✅ **Otros roles**: Acceso basado en permisos específicos asignados desde el módulo de roles

## 🏗️ **ARQUITECTURA DEL SISTEMA**

### **1. Backend (Django)**
- **Middleware de permisos**: `api/authentication/middleware.py`
- **Endpoints de permisos**: `api/roles/views.py` (nuevos endpoints)
- **Verificación automática**: En cada request a la API

### **2. Frontend (React)**
- **Servicio de permisos**: `src/service/permisosService.js`
- **Hook personalizado**: `src/hooks/usePermisos.js`
- **Componente de ruta protegida**: `src/components/ProtectedRoute.jsx`
- **Componente de acceso denegado**: `src/components/AccessDenied.jsx`

## 🔧 **CONFIGURACIÓN DE RUTAS PROTEGIDAS**

### **Rutas Públicas (Sin Autenticación)**
```jsx
<Route path="/" element={<Home />} />
<Route path="/login" element={<Login />} />
<Route path="/register" element={<Register />} />
<Route path="/recuperar-contrasena" element={<RecuperarContrasena />} />
```

### **Rutas Protegidas por Permisos**
```jsx
// Gestión de usuarios
<Route
  path="/usuarios"
  element={
    <ProtectedRoute requiredPermission="gestionar_usuarios">
      <AdminLayout><Usuarios /></AdminLayout>
    </ProtectedRoute>
  }
/>

// Gestión de roles
<Route
  path="/roles"
  element={
    <ProtectedRoute requiredPermission="gestionar_roles">
      <AdminLayout><Roles /></AdminLayout>
    </ProtectedRoute>
  }
/>

// Gestión de clientes
<Route
  path="/clientes"
  element={
    <ProtectedRoute requiredPermission="gestionar_clientes">
      <AdminLayout><Clientes /></AdminLayout>
    </ProtectedRoute>
  }
/>

// Y así para todos los módulos...
```

## 🎯 **SISTEMA DE PERMISOS IMPLEMENTADO**

### **Permisos por Módulo**
| **MÓDULO** | **PERMISO REQUERIDO** | **DESCRIPCIÓN** |
|-------------|----------------------|------------------|
| Usuarios | `gestionar_usuarios` | Administrar usuarios del sistema |
| Roles | `gestionar_roles` | Gestionar roles y permisos |
| Abastecimientos | `gestionar_abastecimientos` | Control de inventario |
| Categorías | `gestionar_categorias` | Categorías de insumos |
| Citas | `gestionar_citas` | Gestión de citas |
| Clientes | `gestionar_clientes` | Administración de clientes |
| Compras | `gestionar_compras` | Control de compras |
| Insumos | `gestionar_insumos` | Gestión de productos |
| Liquidaciones | `gestionar_liquidaciones` | Liquidaciones de personal |
| Manicuristas | `gestionar_manicuristas` | Administración de manicuristas |
| Novedades | `gestionar_novedades` | Gestión de novedades |
| Proveedores | `gestionar_proveedores` | Control de proveedores |
| Servicios | `gestionar_servicios` | Catálogo de servicios |
| Ventas | `gestionar_ventas` | Control de ventas |

## 🚀 **USO EN COMPONENTES**

### **1. Usando el Hook usePermisos**
```jsx
import usePermisos from '../hooks/usePermisos';

const MiComponente = () => {
    const { 
        tienePermiso, 
        esAdministrador, 
        esCliente,
        renderizarConPermiso 
    } = usePermisos();

    return (
        <div>
            {/* Mostrar botón solo si tiene permiso */}
            {renderizarConPermiso('gestionar_usuarios', 
                <button>Crear Usuario</button>
            )}

            {/* Mostrar contenido solo para administradores */}
            {esAdministrador() && <AdminPanel />}

            {/* Mostrar contenido solo para clientes */}
            {esCliente() && <ClienteInfo />}
        </div>
    );
};
```

### **2. Verificación Directa de Permisos**
```jsx
const { tienePermiso } = usePermisos();

if (tienePermiso('gestionar_roles')) {
    // Mostrar funcionalidad de roles
}
```

### **3. Verificación de Acceso a Rutas**
```jsx
const { puedeAccederARuta } = usePermisos();

if (puedeAccederARuta('/usuarios')) {
    // Usuario puede acceder a la página de usuarios
}
```

## 🔒 **NIVELES DE ACCESO IMPLEMENTADOS**

### **Nivel 1: Clientes**
- **Acceso**: Solo módulos básicos
- **Rutas permitidas**: `/`, `/usuarios`, `/clientes`, `/citas`, `/servicios`, `/venta-servicios`
- **Restricciones**: No puede acceder a módulos administrativos

### **Nivel 2: Manicuristas**
- **Acceso**: Basado en permisos asignados
- **Rutas permitidas**: Según permisos específicos
- **Restricciones**: Solo módulos para los que tenga permisos

### **Nivel 3: Administradores**
- **Acceso**: Completo a todos los módulos
- **Rutas permitidas**: Todas las rutas del sistema
- **Restricciones**: Ninguna

## 📱 **EJEMPLOS PRÁCTICOS**

### **Ejemplo 1: Botón Condicional**
```jsx
const { renderizarConPermiso } = usePermisos();

return (
    <div>
        <h1>Gestión de Usuarios</h1>
        
        {/* Botón solo visible para usuarios con permiso */}
        {renderizarConPermiso('gestionar_usuarios',
            <button className="btn btn-primary">
                Crear Nuevo Usuario
            </button>
        )}
        
        {/* Lista de usuarios siempre visible */}
        <UserList />
    </div>
);
```

### **Ejemplo 2: Menú Dinámico**
```jsx
const { permisos, esAdministrador } = usePermisos();

const menuItems = [
    { path: '/usuarios', label: 'Usuarios', permiso: 'gestionar_usuarios' },
    { path: '/roles', label: 'Roles', permiso: 'gestionar_roles' },
    { path: '/clientes', label: 'Clientes', permiso: 'gestionar_clientes' },
    // ... más items
];

return (
    <nav>
        {menuItems.map(item => (
            <div key={item.path}>
                {(esAdministrador() || tienePermiso(item.permiso)) && (
                    <Link to={item.path}>{item.label}</Link>
                )}
            </div>
        ))}
    </nav>
);
```

### **Ejemplo 3: Formulario Condicional**
```jsx
const { renderizarConPermiso } = usePermisos();

return (
    <div>
        <h2>Información del Cliente</h2>
        
        {/* Campos básicos siempre visibles */}
        <input type="text" placeholder="Nombre" />
        <input type="email" placeholder="Email" />
        
        {/* Campos avanzados solo para usuarios con permiso */}
        {renderizarConPermiso('gestionar_clientes',
            <div>
                <input type="text" placeholder="Documento" />
                <input type="text" placeholder="Dirección" />
                <select>
                    <option>Seleccionar Rol</option>
                    <option>Cliente</option>
                    <option>Manicurista</option>
                </select>
            </div>
        )}
    </div>
);
```

## 🛡️ **SEGURIDAD IMPLEMENTADA**

### **Frontend**
- ✅ Verificación de permisos en cada ruta
- ✅ Renderizado condicional de contenido
- ✅ Redirección automática según permisos
- ✅ Hook personalizado para gestión de permisos

### **Backend**
- ✅ Middleware de verificación de permisos
- ✅ Endpoints protegidos por permisos
- ✅ Verificación de roles y permisos en cada request
- ✅ Respuestas de error apropiadas para acceso denegado

## 🔍 **DEBUGGING Y LOGS**

### **Verificar Permisos en Consola**
```javascript
// En la consola del navegador
const permisos = await permisosService.obtenerRutasPermitidas();
console.log('Rutas permitidas:', permisos);

const tienePermiso = await permisosService.usuarioTienePermiso('gestionar_usuarios');
console.log('Tiene permiso usuarios:', tienePermiso);
```

### **Verificar Estado del Hook**
```jsx
const { permisos, rutasPermitidas, loading, error } = usePermisos();

useEffect(() => {
    console.log('Permisos cargados:', permisos);
    console.log('Rutas permitidas:', rutasPermitidas);
}, [permisos, rutasPermitidas]);
```

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

### **Backend ✅**
- [x] Middleware de permisos creado
- [x] Endpoints de permisos implementados
- [x] Verificación automática en todas las APIs
- [x] Configuración en settings.py

### **Frontend ✅**
- [x] Servicio de permisos implementado
- [x] Hook usePermisos creado
- [x] ProtectedRoute mejorado
- [x] Todas las rutas protegidas por permisos
- [x] Componente AccessDenied creado

### **Configuración ✅**
- [x] Rutas públicas definidas
- [x] Rutas protegidas por permisos específicos
- [x] Redirección inteligente según rol
- [x] Sistema de permisos por módulo

## 🎉 **RESULTADO FINAL**

El sistema ahora proporciona:

1. **Seguridad robusta**: Verificación de permisos en frontend y backend
2. **Flexibilidad**: Permisos granulares por módulo
3. **Experiencia de usuario**: Contenido adaptativo según permisos
4. **Mantenibilidad**: Código centralizado y reutilizable
5. **Escalabilidad**: Fácil agregar nuevos permisos y módulos

Los usuarios solo pueden acceder a las funcionalidades para las que tienen permisos, y el sistema redirige automáticamente a páginas apropiadas según su rol y permisos.
