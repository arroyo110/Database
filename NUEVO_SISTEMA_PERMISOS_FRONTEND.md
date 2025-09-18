# 🔐 NUEVO SISTEMA DE PERMISOS POR ACCIONES - GUÍA DE IMPLEMENTACIÓN FRONTEND

## 📋 **RESUMEN DE CAMBIOS**

Se ha implementado un nuevo sistema de permisos basado en **acciones específicas** en lugar de permisos globales por módulo. Ahora cada módulo tiene permisos granulares para:

- ✅ **Crear** - Crear nuevos registros
- ✅ **Listar** - Ver listado de registros  
- ✅ **Ver Detalles** - Ver detalles de un registro específico
- ✅ **Editar** - Editar registros existentes
- ✅ **Eliminar** - Eliminar registros

## 🏗️ **ARQUITECTURA DEL NUEVO SISTEMA**

### **1. Estructura de Permisos**
```
Módulo + Acción = Permiso
Ejemplos:
- usuarios_crear
- usuarios_listar  
- usuarios_ver_detalles
- usuarios_editar
- usuarios_eliminar
- clientes_crear
- citas_listar
```

### **2. Módulos Disponibles**
- `usuarios` - Gestión de usuarios
- `clientes` - Gestión de clientes
- `manicuristas` - Gestión de manicuristas
- `roles` - Gestión de roles y permisos
- `citas` - Gestión de citas
- `servicios` - Gestión de servicios
- `insumos` - Gestión de insumos
- `categoria_insumos` - Gestión de categorías
- `compras` - Gestión de compras
- `proveedores` - Gestión de proveedores
- `abastecimientos` - Gestión de abastecimientos
- `venta_servicios` - Gestión de ventas
- `liquidaciones` - Gestión de liquidaciones
- `novedades` - Gestión de novedades

## 🚀 **IMPLEMENTACIÓN EN FRONTEND**

### **1. Actualizar el Servicio de Permisos**

```javascript
// src/services/permisosService.js
class PermisosService {
    constructor() {
        this.baseURL = 'http://localhost:8000/api';
    }

    // Obtener permisos del usuario actual
    async obtenerPermisosUsuario() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${this.baseURL}/roles/permisos_usuario/?usuario_id=${this.getUserId()}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) throw new Error('Error al obtener permisos');
            
            const data = await response.json();
            return data.permisos.map(permiso => permiso.nombre);
        } catch (error) {
            console.error('Error obteniendo permisos:', error);
            return [];
        }
    }

    // Verificar si el usuario tiene un permiso específico
    async tienePermiso(permiso) {
        const permisos = await this.obtenerPermisosUsuario();
        return permisos.includes(permiso);
    }

    // Verificar si el usuario tiene cualquiera de los permisos
    async tieneAlgunPermiso(permisos) {
        const permisosUsuario = await this.obtenerPermisosUsuario();
        return permisos.some(permiso => permisosUsuario.includes(permiso));
    }

    // Verificar si el usuario tiene todos los permisos
    async tieneTodosLosPermisos(permisos) {
        const permisosUsuario = await this.obtenerPermisosUsuario();
        return permisos.every(permiso => permisosUsuario.includes(permiso));
    }

    // Obtener permisos por módulo
    async obtenerPermisosPorModulo(modulo) {
        const permisos = await this.obtenerPermisosUsuario();
        return permisos.filter(permiso => permiso.startsWith(`${modulo}_`));
    }

    // Verificar acceso a una ruta específica
    async puedeAccederARuta(ruta, metodo = 'GET') {
        const mapeoRutas = {
            '/usuarios': 'usuarios',
            '/clientes': 'clientes',
            '/manicuristas': 'manicuristas',
            '/roles': 'roles',
            '/citas': 'citas',
            '/servicios': 'servicios',
            '/insumos': 'insumos',
            '/categoria-insumos': 'categoria_insumos',
            '/compras': 'compras',
            '/proveedores': 'proveedores',
            '/abastecimientos': 'abastecimientos',
            '/venta-servicios': 'venta_servicios',
            '/liquidaciones': 'liquidaciones',
            '/novedades': 'novedades'
        };

        const mapeoMetodos = {
            'GET': ruta.endsWith('/') ? 'listar' : 'ver_detalles',
            'POST': 'crear',
            'PUT': 'editar',
            'PATCH': 'editar',
            'DELETE': 'eliminar'
        };

        const modulo = mapeoRutas[ruta];
        const accion = mapeoMetodos[metodo] || 'listar';
        
        if (!modulo) return true; // Ruta no protegida
        
        const permiso = `${modulo}_${accion}`;
        return await this.tienePermiso(permiso);
    }

    getUserId() {
        // Implementar lógica para obtener el ID del usuario actual
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return user.id;
    }
}

export default new PermisosService();
```

### **2. Actualizar el Hook usePermisos**

```javascript
// src/hooks/usePermisos.js
import { useState, useEffect } from 'react';
import permisosService from '../services/permisosService';

const usePermisos = () => {
    const [permisos, setPermisos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        cargarPermisos();
    }, []);

    const cargarPermisos = async () => {
        try {
            setLoading(true);
            const permisosUsuario = await permisosService.obtenerPermisosUsuario();
            setPermisos(permisosUsuario);
            setError(null);
        } catch (err) {
            setError(err.message);
            console.error('Error cargando permisos:', err);
        } finally {
            setLoading(false);
        }
    };

    // Verificar si tiene un permiso específico
    const tienePermiso = (permiso) => {
        return permisos.includes(permiso);
    };

    // Verificar si tiene cualquiera de los permisos
    const tieneAlgunPermiso = (permisosArray) => {
        return permisosArray.some(permiso => permisos.includes(permiso));
    };

    // Verificar si tiene todos los permisos
    const tieneTodosLosPermisos = (permisosArray) => {
        return permisosArray.every(permiso => permisos.includes(permiso));
    };

    // Obtener permisos por módulo
    const obtenerPermisosPorModulo = (modulo) => {
        return permisos.filter(permiso => permiso.startsWith(`${modulo}_`));
    };

    // Verificar acceso a ruta
    const puedeAccederARuta = async (ruta, metodo = 'GET') => {
        return await permisosService.puedeAccederARuta(ruta, metodo);
    };

    // Renderizar condicionalmente basado en permisos
    const renderizarConPermiso = (permiso, componente) => {
        return tienePermiso(permiso) ? componente : null;
    };

    // Renderizar condicionalmente basado en múltiples permisos (OR)
    const renderizarConAlgunPermiso = (permisosArray, componente) => {
        return tieneAlgunPermiso(permisosArray) ? componente : null;
    };

    // Renderizar condicionalmente basado en múltiples permisos (AND)
    const renderizarConTodosLosPermisos = (permisosArray, componente) => {
        return tieneTodosLosPermisos(permisosArray) ? componente : null;
    };

    // Verificar si es administrador
    const esAdministrador = () => {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return user.rol?.nombre?.toLowerCase() === 'administrador';
    };

    // Verificar si es cliente
    const esCliente = () => {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return user.rol?.nombre?.toLowerCase() === 'cliente';
    };

    return {
        permisos,
        loading,
        error,
        tienePermiso,
        tieneAlgunPermiso,
        tieneTodosLosPermisos,
        obtenerPermisosPorModulo,
        puedeAccederARuta,
        renderizarConPermiso,
        renderizarConAlgunPermiso,
        renderizarConTodosLosPermisos,
        esAdministrador,
        esCliente,
        recargarPermisos: cargarPermisos
    };
};

export default usePermisos;
```

### **3. Actualizar el Componente ProtectedRoute**

```javascript
// src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import usePermisos from '../hooks/usePermisos';
import LoadingSpinner from './LoadingSpinner';
import AccessDenied from './AccessDenied';

const ProtectedRoute = ({ 
    children, 
    requiredPermission, 
    requiredPermissions = [], 
    requireAll = false,
    redirectTo = '/dashboard' 
}) => {
    const { 
        tienePermiso, 
        tieneAlgunPermiso, 
        tieneTodosLosPermisos, 
        esAdministrador, 
        loading 
    } = usePermisos();

    if (loading) {
        return <LoadingSpinner />;
    }

    // Los administradores tienen acceso a todo
    if (esAdministrador()) {
        return children;
    }

    // Verificar permiso único
    if (requiredPermission && !tienePermiso(requiredPermission)) {
        return <AccessDenied requiredPermission={requiredPermission} />;
    }

    // Verificar múltiples permisos
    if (requiredPermissions.length > 0) {
        const tieneAcceso = requireAll 
            ? tieneTodosLosPermisos(requiredPermissions)
            : tieneAlgunPermiso(requiredPermissions);

        if (!tieneAcceso) {
            return <AccessDenied requiredPermissions={requiredPermissions} requireAll={requireAll} />;
        }
    }

    return children;
};

export default ProtectedRoute;
```

### **4. Actualizar las Rutas**

```javascript
// src/App.jsx o tu archivo de rutas
import ProtectedRoute from './components/ProtectedRoute';

// Rutas con permisos específicos
<Route
    path="/usuarios"
    element={
        <ProtectedRoute requiredPermission="usuarios_listar">
            <AdminLayout><Usuarios /></AdminLayout>
        </ProtectedRoute>
    }
/>

<Route
    path="/clientes"
    element={
        <ProtectedRoute requiredPermission="clientes_listar">
            <AdminLayout><Clientes /></AdminLayout>
        </ProtectedRoute>
    }
/>

<Route
    path="/citas"
    element={
        <ProtectedRoute requiredPermission="citas_listar">
            <AdminLayout><Citas /></AdminLayout>
        </ProtectedRoute>
    }
/>

// Ruta con múltiples permisos (OR)
<Route
    path="/reportes"
    element={
        <ProtectedRoute 
            requiredPermissions={['citas_listar', 'venta_servicios_listar']}
            requireAll={false}
        >
            <AdminLayout><Reportes /></AdminLayout>
        </ProtectedRoute>
    }
/>

// Ruta con múltiples permisos (AND)
<Route
    path="/configuracion-avanzada"
    element={
        <ProtectedRoute 
            requiredPermissions={['usuarios_editar', 'roles_editar']}
            requireAll={true}
        >
            <AdminLayout><ConfiguracionAvanzada /></AdminLayout>
        </ProtectedRoute>
    }
/>
```

### **5. Ejemplos de Uso en Componentes**

```javascript
// src/components/Usuarios.jsx
import React from 'react';
import usePermisos from '../hooks/usePermisos';

const Usuarios = () => {
    const { 
        tienePermiso, 
        renderizarConPermiso, 
        renderizarConAlgunPermiso 
    } = usePermisos();

    return (
        <div>
            <h1>Gestión de Usuarios</h1>
            
            {/* Botón de crear - solo si tiene permiso */}
            {renderizarConPermiso('usuarios_crear', 
                <button className="btn btn-primary">
                    Crear Usuario
                </button>
            )}

            {/* Botón de eliminar - solo si tiene permiso */}
            {renderizarConPermiso('usuarios_eliminar', 
                <button className="btn btn-danger">
                    Eliminar Seleccionados
                </button>
            )}

            {/* Botones de acción - si tiene cualquiera de los permisos */}
            {renderizarConAlgunPermiso(['usuarios_editar', 'usuarios_eliminar'], 
                <div className="action-buttons">
                    <button className="btn btn-warning">Editar</button>
                    <button className="btn btn-danger">Eliminar</button>
                </div>
            )}

            {/* Lista de usuarios - siempre visible si tiene permiso de listar */}
            {tienePermiso('usuarios_listar') && (
                <div className="usuarios-list">
                    {/* Tu componente de lista aquí */}
                </div>
            )}
        </div>
    );
};

export default Usuarios;
```

### **6. Actualizar el Menú de Navegación**

```javascript
// src/components/Navigation.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import usePermisos from '../hooks/usePermisos';

const Navigation = () => {
    const { tienePermiso, esAdministrador } = usePermisos();

    const menuItems = [
        { 
            path: '/dashboard', 
            label: 'Dashboard', 
            permiso: 'dashboard_acceder' 
        },
        { 
            path: '/usuarios', 
            label: 'Usuarios', 
            permiso: 'usuarios_listar' 
        },
        { 
            path: '/clientes', 
            label: 'Clientes', 
            permiso: 'clientes_listar' 
        },
        { 
            path: '/citas', 
            label: 'Citas', 
            permiso: 'citas_listar' 
        },
        { 
            path: '/servicios', 
            label: 'Servicios', 
            permiso: 'servicios_listar' 
        },
        { 
            path: '/roles', 
            label: 'Roles', 
            permiso: 'roles_listar' 
        }
    ];

    return (
        <nav>
            {menuItems.map(item => (
                <div key={item.path}>
                    {(esAdministrador() || tienePermiso(item.permiso)) && (
                        <Link to={item.path} className="nav-link">
                            {item.label}
                        </Link>
                    )}
                </div>
            ))}
        </nav>
    );
};

export default Navigation;
```

## 🔧 **MIGRACIÓN DESDE EL SISTEMA ANTERIOR**

### **Cambios Necesarios en el Frontend**

1. **Actualizar el servicio de permisos** para usar los nuevos nombres de permisos
2. **Modificar las rutas protegidas** para usar permisos específicos
3. **Actualizar los componentes** para verificar permisos granulares
4. **Cambiar el menú de navegación** para usar el nuevo sistema

### **Mapeo de Permisos Anteriores a Nuevos**

| **SISTEMA ANTERIOR** | **NUEVO SISTEMA** |
|---------------------|-------------------|
| `gestionar_usuarios` | `usuarios_crear`, `usuarios_listar`, `usuarios_ver_detalles`, `usuarios_editar`, `usuarios_eliminar` |
| `gestionar_clientes` | `clientes_crear`, `clientes_listar`, `clientes_ver_detalles`, `clientes_editar`, `clientes_eliminar` |
| `gestionar_citas` | `citas_crear`, `citas_listar`, `citas_ver_detalles`, `citas_editar`, `citas_eliminar` |
| `ver_reportes` | `dashboard_acceder` |

## 🎯 **VENTAJAS DEL NUEVO SISTEMA**

1. **Granularidad**: Control fino sobre cada acción
2. **Flexibilidad**: Diferentes permisos para diferentes acciones
3. **Escalabilidad**: Fácil agregar nuevos módulos y acciones
4. **Seguridad**: Verificación específica por operación
5. **UX**: Contenido adaptativo según permisos

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

### **Backend ✅**
- [x] Modelos actualizados (Modulo, Accion, Permiso)
- [x] Middleware actualizado
- [x] Decoradores de permisos creados
- [x] Endpoints de permisos implementados
- [x] Comando de población creado

### **Frontend (Por Implementar)**
- [ ] Servicio de permisos actualizado
- [ ] Hook usePermisos actualizado
- [ ] ProtectedRoute actualizado
- [ ] Rutas actualizadas con nuevos permisos
- [ ] Componentes actualizados
- [ ] Menú de navegación actualizado

## 🚀 **PASOS PARA IMPLEMENTAR**

1. **Ejecutar migraciones** en el backend
2. **Poblar permisos** con el comando `python manage.py populate_permissions`
3. **Actualizar el frontend** siguiendo los ejemplos
4. **Probar los permisos** en diferentes roles
5. **Configurar roles** con permisos específicos

## 🎉 **RESULTADO FINAL**

El nuevo sistema proporciona:

- ✅ **Control granular** sobre cada acción
- ✅ **Mejor experiencia de usuario** con contenido adaptativo
- ✅ **Mayor seguridad** con verificación específica
- ✅ **Fácil mantenimiento** y escalabilidad
- ✅ **Flexibilidad** para diferentes tipos de usuarios

Los usuarios ahora solo pueden realizar las acciones para las que tienen permisos específicos, y el sistema se adapta dinámicamente a sus capacidades.
