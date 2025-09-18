# 🚀 GUÍA DE IMPLEMENTACIÓN - SISTEMA DE AUTENTICACIÓN UNIFICADO

## 📋 **RESUMEN DE CAMBIOS REALIZADOS**

He unificado completamente el sistema de autenticación del backend para resolver todos los problemas identificados:

### ✅ **PROBLEMAS SOLUCIONADOS:**
1. **Sistema fragmentado** → Ahora es UN SOLO sistema unificado
2. **JWT no implementado** → JWT completamente funcional con refresh tokens
3. **Roles no reconocidos** → Roles se envían correctamente en la respuesta
4. **Contraseñas temporales** → Sistema automático de contraseñas temporales
5. **Recuperación de contraseña** → Sistema completo con códigos por email

---

## 🔐 **ENDPOINTS NUEVOS DEL BACKEND**

### **1. LOGIN UNIFICADO**
```
POST /api/auth/login/
```

**Body:**
```json
{
    "correo_electronico": "usuario@email.com",
    "contraseña": "password123"
}
```

**Respuesta exitosa:**
```json
{
    "mensaje": "Login exitoso",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "usuario": {
        "id": 1,
        "nombre": "Juan Pérez",
        "correo_electronico": "juan@email.com",
        "rol": "cliente",
        "is_active": true,
        "debe_cambiar_contraseña": false
    },
    "tipo_usuario": "cliente",
    "debe_cambiar_contraseña": false,
    "nombre_completo": "Juan Pérez",
    "documento": "12345678"
}
```

### **2. REGISTRO UNIFICADO**
```
POST /api/auth/registro/
```

**Body:**
```json
{
    "nombre": "María García",
    "tipo_documento": "CC",
    "documento": "87654321",
    "celular": "3001234567",
    "correo_electronico": "maria@email.com",
    "direccion": "Calle 123 #45-67",
    "tipo_usuario": "manicurista",
    "especialidad": "Uñas acrílicas"
}
```

**Respuesta exitosa:**
```json
{
    "mensaje": "Usuario registrado exitosamente",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "usuario": {
        "id": 2,
        "nombre": "María García",
        "correo_electronico": "maria@email.com",
        "rol": "manicurista",
        "is_active": true,
        "debe_cambiar_contraseña": true
    },
    "tipo_usuario": "manicurista",
    "contraseña_generada": "Ax7Kp9Qw"
}
```

### **3. RECUPERACIÓN DE CONTRASEÑA**
```
POST /api/auth/solicitar-codigo/
POST /api/auth/confirmar-codigo/
```

### **4. CAMBIAR CONTRASEÑA TEMPORAL**
```
POST /api/auth/cambiar-contraseña/
```

---

## 🎯 **IMPLEMENTACIÓN EN EL FRONTEND**

### **PASO 1: Actualizar el AuthContext**

Reemplaza tu `authContext.jsx` actual con este:

```jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth debe ser usado dentro de un AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('access_token'));
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (token) {
            try {
                const decoded = jwtDecode(token);
                const currentTime = Date.now() / 1000;
                
                if (decoded.exp < currentTime) {
                    // Token expirado
                    logout();
                } else {
                    // Token válido, obtener información del usuario
                    const userInfo = JSON.parse(localStorage.getItem('user_info') || '{}');
                    setUser(userInfo);
                }
            } catch (error) {
                console.error('Error decodificando token:', error);
                logout();
            }
        }
        setLoading(false);
    }, [token]);

    const login = async (correo, contraseña) => {
        try {
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    correo_electronico: correo,
                    contraseña: contraseña
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Guardar tokens
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                
                // Guardar información del usuario
                localStorage.setItem('user_info', JSON.stringify(data.usuario));
                
                // Actualizar estado
                setToken(data.access_token);
                setUser(data.usuario);
                
                return {
                    success: true,
                    data: data
                };
            } else {
                return {
                    success: false,
                    error: data.error || 'Error en el login'
                };
            }
        } catch (error) {
            return {
                success: false,
                error: 'Error de conexión'
            };
        }
    };

    const register = async (userData) => {
        try {
            const response = await fetch('http://localhost:8000/api/auth/registro/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                // Guardar tokens
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                
                // Guardar información del usuario
                localStorage.setItem('user_info', JSON.stringify(data.usuario));
                
                // Actualizar estado
                setToken(data.access_token);
                setUser(data.usuario);
                
                return {
                    success: true,
                    data: data
                };
            } else {
                return {
                    success: false,
                    error: data.error || 'Error en el registro'
                };
            }
        } catch (error) {
            return {
                success: false,
                error: 'Error de conexión'
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_info');
        setToken(null);
        setUser(null);
    };

    const refreshToken = async () => {
        try {
            const refresh = localStorage.getItem('refresh_token');
            if (!refresh) {
                logout();
                return false;
            }

            const response = await fetch('http://localhost:8000/api/auth/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refresh
                })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access);
                setToken(data.access);
                return true;
            } else {
                logout();
                return false;
            }
        } catch (error) {
            logout();
            return false;
        }
    };

    const value = {
        user,
        token,
        loading,
        login,
        register,
        logout,
        refreshToken
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
```

### **PASO 2: Actualizar el componente Login**

Reemplaza tu `Login.jsx` actual con este:

```jsx
import React, { useState } from 'react';
import { useAuth } from '../../context/authContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [formData, setFormData] = useState({
        correo_electronico: '',
        contraseña: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const result = await login(formData.correo_electronico, formData.contraseña);

        if (result.success) {
            // Redirigir según el rol
            const user = result.data.usuario;
            
            if (user.debe_cambiar_contraseña) {
                navigate('/cambiar-contraseña');
            } else {
                switch (user.rol?.toLowerCase()) {
                    case 'cliente':
                        navigate('/cliente/dashboard');
                        break;
                    case 'manicurista':
                        navigate('/manicurista/dashboard');
                        break;
                    case 'admin':
                        navigate('/admin/dashboard');
                        break;
                    default:
                        navigate('/dashboard');
                }
            }
        } else {
            setError(result.error);
        }
        
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        Iniciar Sesión
                    </h2>
                </div>
                
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                            {error}
                        </div>
                    )}
                    
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div>
                            <label htmlFor="correo_electronico" className="sr-only">
                                Correo Electrónico
                            </label>
                            <input
                                id="correo_electronico"
                                name="correo_electronico"
                                type="email"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Correo Electrónico"
                                value={formData.correo_electronico}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="contraseña" className="sr-only">
                                Contraseña
                            </label>
                            <input
                                id="contraseña"
                                name="contraseña"
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Contraseña"
                                value={formData.contraseña}
                                onChange={handleChange}
                            />
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                        >
                            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                        </button>
                    </div>

                    <div className="flex items-center justify-between">
                        <div className="text-sm">
                            <a href="/recuperar-contraseña" className="font-medium text-indigo-600 hover:text-indigo-500">
                                ¿Olvidaste tu contraseña?
                            </a>
                        </div>
                        <div className="text-sm">
                            <a href="/registro" className="font-medium text-indigo-600 hover:text-indigo-500">
                                Crear cuenta
                            </a>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
```

### **PASO 3: Crear componente de cambio de contraseña**

```jsx
import React, { useState } from 'react';
import { useAuth } from '../../context/authContext';
import { useNavigate } from 'react-router-dom';

const CambiarContraseña = () => {
    const [formData, setFormData] = useState({
        contraseña_temporal: '',
        nueva_contraseña: '',
        confirmar_contraseña: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    const { user } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        if (formData.nueva_contraseña !== formData.confirmar_contraseña) {
            setError('Las contraseñas no coinciden');
            setLoading(false);
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/api/auth/cambiar-contraseña/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    correo_electronico: user.correo_electronico,
                    contraseña_temporal: formData.contraseña_temporal,
                    nueva_contraseña: formData.nueva_contraseña,
                    confirmar_contraseña: formData.confirmar_contraseña
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Redirigir según el rol
                switch (user.rol?.toLowerCase()) {
                    case 'cliente':
                        navigate('/cliente/dashboard');
                        break;
                    case 'manicurista':
                        navigate('/manicurista/dashboard');
                        break;
                    case 'admin':
                        navigate('/admin/dashboard');
                        break;
                    default:
                        navigate('/dashboard');
                }
            } else {
                setError(data.error || 'Error al cambiar contraseña');
            }
        } catch (error) {
            setError('Error de conexión');
        }
        
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        Cambiar Contraseña Temporal
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-600">
                        Ingresa tu contraseña temporal y crea una nueva
                    </p>
                </div>
                
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                            {error}
                        </div>
                    )}
                    
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div>
                            <input
                                name="contraseña_temporal"
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Contraseña Temporal"
                                value={formData.contraseña_temporal}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <input
                                name="nueva_contraseña"
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Nueva Contraseña"
                                value={formData.nueva_contraseña}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <input
                                name="confirmar_contraseña"
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Confirmar Contraseña"
                                value={formData.confirmar_contraseña}
                                onChange={handleChange}
                            />
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                        >
                            {loading ? 'Cambiando contraseña...' : 'Cambiar Contraseña'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CambiarContraseña;
```

---

## 🔧 **CONFIGURACIÓN ADICIONAL**

### **1. Instalar dependencias**
```bash
npm install jwt-decode
```

### **2. Configurar interceptor para refresh automático**
```jsx
// En tu archivo principal o donde configures axios
import axios from 'axios';

// Interceptor para agregar token a todas las peticiones
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores 401 y refresh automático
axios.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            try {
                const refresh = localStorage.getItem('refresh_token');
                const response = await axios.post('http://localhost:8000/api/auth/refresh/', {
                    refresh: refresh
                });
                
                localStorage.setItem('access_token', response.data.access);
                
                // Reintentar la petición original
                originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // Refresh falló, redirigir al login
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_info');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        
        return Promise.reject(error);
    }
);
```

---

## 🎉 **RESULTADO FINAL**

Con estos cambios tendrás:

✅ **Sistema de autenticación completamente unificado**
✅ **JWT funcional con refresh automático**
✅ **Roles reconocidos correctamente**
✅ **Contraseñas temporales automáticas**
✅ **Recuperación de contraseña por email**
✅ **Frontend limpio y funcional**

El sistema ahora maneja todos los tipos de usuario de manera uniforme y el frontend puede reconocer perfectamente el rol y redirigir según corresponda.
