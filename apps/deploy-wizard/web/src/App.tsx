import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Catalog from "./pages/Catalog";
import Deploy from "./pages/Deploy";
import Drift from "./pages/Drift";
import History from "./pages/History";
import HitlConfig from "./pages/HitlConfig";
import Tenants from "./pages/Tenants";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="border-b p-4 flex gap-4">
        <Link to="/">APEX Wizard</Link>
        <Link to="/catalog">Catalog</Link>
        <Link to="/tenants">Tenants</Link>
        <Link to="/deploy">Deploy</Link>
        <Link to="/history">History</Link>
        <Link to="/drift">Drift</Link>
        <Link to="/hitl">HITL</Link>
      </nav>
      <main className="p-4">
        <Routes>
          <Route path="/" element={<Catalog />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/tenants" element={<Tenants />} />
          <Route path="/deploy" element={<Deploy />} />
          <Route path="/history" element={<History />} />
          <Route path="/drift" element={<Drift />} />
          <Route path="/hitl" element={<HitlConfig />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
