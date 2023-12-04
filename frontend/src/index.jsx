//import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { BrowserRouter } from 'react-router-dom';
import {CookiesProvider} from "react-cookie";
import TopMenu from "./components/TopMenu.jsx";
import Background from "./components/Background.jsx";

export const app_colors = () => {
    return {
        "primary": "#ee7744",
        "secondary": "#ffcc00",
        "background": "#1c1c1c",
        "text": "#ffffff",
    }
}

function page_layout() {
    return(
    <CookiesProvider>
        <Background />
        <TopMenu />
        <div style={{textAlign: "center"}}>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </div>
    </CookiesProvider>
    )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(page_layout());
