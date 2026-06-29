import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Agriculture from './pages/Agriculture';
import Health from './pages/Health';
import Education from './pages/Education';
import Water from './pages/Water';
import Infrastructure from './pages/Infrastructure';
import Finance from './pages/Finance';
import Results from './pages/Results';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing page - first page users see */}
        <Route path="/" element={<Landing />} />
        
        {/* Dashboard and all other pages */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/agriculture" element={<Agriculture />} />
        <Route path="/health" element={<Health />} />
        <Route path="/education" element={<Education />} />
        <Route path="/water" element={<Water />} />
        <Route path="/infrastructure" element={<Infrastructure />} />
        <Route path="/finance" element={<Finance />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}
