import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <h1>Hola mundo! (esta es la pantalla de inicio)</h1>
      <h2>Aqui se pueden ir creando componentes</h2>
      <h3>Cada componente jsx y css será una pantalla</h3>
      <h4>
        Para no complicarnos, los estilos se manejan en el CSS y el JSX se
        encargará de hacer el "html" del componente
      </h4>
      <h5>
        Necesitamos por ejemplo, pagina1.css/pagina1.jsx,pagina2.css/pagina2.jsx
        y luego las conectamos
      </h5>
      <h6>
        Se esta usando Vite+React con JavaScript JWC, yo empezaré a hacer
        algunas pantallas y componentes en otro lado
      </h6>
    </>

    /*
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>*/
  );
}

export default App;
