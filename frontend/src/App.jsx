import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css';
import Home from "./pages/Dashboard";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Account from "./pages/Account";
import Offers from "./pages/Offers";
import Calendar from "./pages/Calendar";
import ApplicationDetails from "./pages/ApplicationDetails";

export default function App() {
  return (
    <div className="App min-h-screen bg-[#EDF6F9]">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/account" element={<Account />} />
          <Route path="/job-offers" element={<Offers />} />
          <Route path="/calendar" element={<Calendar />} />
          <Route path="/dashboard/application/:applicationId" element={<ApplicationDetails />} />
        </Routes>
      </Router>
    </div>
  )
}
