import React, { useState } from 'react';
import './LoginRegister.css';
import googleIcon from '../assets/googleIcon.svg';
import facebookIcon from '../assets/facebookIcon.svg';

function LoginRegister() {
  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        {/* Botón de cierre */}
        <div className="close-button">
          <button className="close-icon">X</button>
        </div>

        {/* Logo centrado */}
        <div className="logo">
          <img src="path_to_logo" alt="Logo" />
        </div>

        <h2>Te damos la bienvenida!</h2>
        <p>Ingresa tus datos abajo</p>

        {/* Formulario de login */}
        <form>
          <label>Correo electrónico</label>
          <input type="email" placeholder="ejemplo@mail.com" />

          {/* Campo de contraseña con opción de mostrar/ocultar */}
          <label>Contraseña</label>
          <div className="password-container">
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Contraseña"
            />
            <button
              type="button"
              className="toggle-password"
              onClick={togglePasswordVisibility}
            >
              {showPassword ? '👁️' : ''}
            </button>
          </div>

          {/* Enlace para recuperar contraseña */}
          <a href="#" className="forgot-password">
            Olvidé mi contraseña
          </a>

          {/* Botones */}
          <button type="submit" className="login-button">
            Iniciar sesión
          </button>
          <button type="button" className="register-button">
            Registrarme
          </button>
        </form>

        {/* Login social */}
        <div className="social-login">
          <button>
            <img src={googleIcon} alt="Chrome Login" />
          </button>
          <button>
            <img src={facebookIcon} alt="Facebook Login" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginRegister;

