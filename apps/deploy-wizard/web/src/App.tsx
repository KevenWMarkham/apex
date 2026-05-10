import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Adapters from "./pages/Adapters";
import Catalog from "./pages/Catalog";
import Deploy from "./pages/Deploy";
import Drift from "./pages/Drift";
import History from "./pages/History";
import HitlConfig from "./pages/HitlConfig";
import Roadmap from "./pages/Roadmap";
import SecurityGate from "./pages/SecurityGate";
import Tenants from "./pages/Tenants";
import Wizard from "./pages/Wizard";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="border-b p-4 flex gap-4 flex-wrap">
        <Link to="/" className="font-bold">APEX Wizard</Link>
        <Link to="/wizard">Deploy Wizard</Link>
        <Link to="/security-gate">Security Gate</Link>
        <Link to="/roadmap">Roadmap</Link>
        <Link to="/catalog">Catalog</Link>
        <Link to="/adapters">Adapters</Link>
        <Link to="/tenants">Tenants</Link>
        <Link to="/history">History</Link>
        <Link to="/drift">Drift</Link>
        <Link to="/hitl">HITL</Link>
      </nav>
      <main className="p-4">
        <Routes>
          <Route path="/" element={<Wizard />} />
          <Route path="/wizard" element={<Wizard />} />
          <Route path="/security-gate" element={<SecurityGate />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/adapters" element={<Adapters />} />
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
