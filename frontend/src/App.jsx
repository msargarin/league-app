import { useState } from "react";
import LoginForm from "./pages/LoginPage";
import AppNavbar from "./components/AppNavbar";
import HomePage from "./pages/HomePage";
import TeamPage from "./pages/TeamPage";

import { BrowserRouter } from "react-router-dom";
import { Routes, Route, Outlet } from "react-router";
import PlayerPage from "./pages/PlayerPage";

function App() {
  const [user, setUser] = useState(null);

  return user ? (
    <BrowserRouter>
      <Routes>
        <Route
          element={
            <>
              <AppNavbar user={user} setUser={setUser} />

              <div className="flex items-start">
                <main className="relative h-full w-full overflow-y-auto bg-gray-100 dark:bg-gray-900">
                  <div className="block items-center justify-between border-b border-gray-200 bg-white p-4 m-4 dark:border-gray-700 dark:bg-gray-800 sm:flex rounded-lg shadow">
                    <Outlet />
                  </div>
                </main>
              </div>
            </>
          }
        >
          <Route path="/" element={<HomePage user={user} />} index />
          <Route path="/team/:teamId" element={<TeamPage user={user} />} />
          <Route
            path="/player/:playerId"
            element={<PlayerPage user={user} />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  ) : (
    <LoginForm setUser={setUser} />
  );
}

export default App;
