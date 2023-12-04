import { Route, Routes } from 'react-router-dom';
import SSOExchange from "./pages/api/SSOExchange.jsx";
import MainPage from "./pages/MainPage.jsx";


const Categories = () => (
    <div>
        <h2>Categories</h2>
        <p>Browse items by category.</p>
    </div>
);

const Products = () => (
    <div>
        <h2>Products</h2>
        <p>Browse individual products.</p>
    </div>
);

export default function App() {
    return (
        <div>
            <Routes>
                <Route path="/api" element={<SSOExchange />}/>
                <Route path="/categories" element={<Categories />} />
                <Route path="/products" element={<Products />} />
                <Route path="/" element={<MainPage />} />
            </Routes>
        </div>
    );
}
